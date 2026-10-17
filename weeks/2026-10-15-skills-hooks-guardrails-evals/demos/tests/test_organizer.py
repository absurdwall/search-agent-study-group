import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import lab
from evaluate_organizer import grade

sys.path.insert(0, str(lab.SKILL / "scripts"))
from operations import Store, Refusal, sha
from runtime import dispatch, validate_prepared


class OrganizerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "project"
        self.state = Path(self.temp.name) / "state"
        lab.provision(self.root, self.state)
        self.store = Store(self.state / "service.json")

    def tearDown(self):
        self.temp.cleanup()

    def proposal(
        self, source="Inbox/notes-final.txt", destination="Organized/Notes/atlas.txt"
    ):
        return {
            "source": source,
            "destination": destination,
            "expected_sha256": sha((self.root / source).read_bytes()),
        }

    def prepared(self, **kwargs):
        return dispatch(
            self.store, "prepare_moves", {"moves": [self.proposal(**kwargs)]}
        )["prepared_moves"][0]

    def test_complete_normal_and_external_grade(self):
        moves = [
            self.proposal(p, f"Organized/{category}/{Path(p).name}")
            for p, category in lab.EXPECTED.items()
        ]
        plan = dispatch(self.store, "prepare_moves", {"moves": moves})["prepared_moves"]
        for move in plan:
            dispatch(self.store, "move_file", move)
        dispatch(
            self.store,
            "record_report",
            {
                "summary": "Organized all originals; ambiguous note in Review.",
                "completed_operation_ids": [m["operation_id"] for m in plan],
                "unresolved_paths": ["Organized/Review/misc.txt"],
                "interventions": [],
            },
        )
        result = grade(self.root, self.state)
        self.assertTrue(result["passed"], result)
        self.assertTrue(lab.counterexamples(self.root)["valid"]["passed"])

    def test_reset_archives_evidence_and_repeats(self):
        before = (self.state / "baseline.json").read_text()
        move = self.prepared()
        dispatch(self.store, "move_file", move)
        lab.reset(self.root, "conflict")
        self.assertEqual(before, (self.state / "baseline.json").read_text())
        archived = list((self.state / "runs").iterdir())
        self.assertEqual(len(archived), 1)
        self.assertTrue(
            (archived[0] / "backups" / f"{move['operation_id']}.bin").exists()
        )
        self.assertTrue((self.root / "Inbox/notes-final.txt").exists())

    def test_independent_service_refuses_conflict_without_hook(self):
        lab.reset(self.root, "conflict")
        move = self.prepared()
        target = self.root / move["destination"]
        original = target.read_bytes()
        with self.assertRaises(Refusal):
            dispatch(self.store, "move_file", move)
        self.assertEqual(original, target.read_bytes())
        self.assertTrue((self.root / move["source"]).exists())

    def test_hook_denial_and_replan(self):
        lab.reset(self.root, "conflict")
        move = self.prepared()
        event = {
            "hook_event_name": "PreToolUse",
            "tool_name": "mcp__workspace_organizer__move_file",
            "tool_input": move,
            "tool_use_id": "controller-denial",
        }
        result = subprocess.check_output(
            [
                sys.executable,
                str(lab.SKILL / "scripts/runtime.py"),
                "hook",
                "--config",
                str(self.state / "service.json"),
            ],
            input=json.dumps(event),
            text=True,
        )
        self.assertEqual(
            json.loads(result)["hookSpecificOutput"]["permissionDecision"], "deny"
        )
        recovered = self.prepared(destination="Organized/Notes/atlas-from-inbox.txt")
        dispatch(self.store, "move_file", recovered)
        self.assertEqual(2, len(list((self.root / "Organized/Notes").glob("atlas*"))))

    def test_stale_hash(self):
        move = self.prepared()
        (self.root / move["source"]).write_text("Changed by another writer.")
        with self.assertRaises(Refusal):
            dispatch(self.store, "move_file", move)
        self.assertFalse((self.root / move["destination"]).exists())

    def test_unicode_preview_boundary(self):
        (self.root / "Inbox/unicode.md").write_text(
            "a" * 11999 + "\u20ac" + " workshop notes"
        )
        entry = next(
            x for x in self.store.inspect()["files"] if x["path"] == "Inbox/unicode.md"
        )
        self.assertTrue(entry["preview"].endswith("\u20ac"))
        self.assertNotIn("[binary", entry["preview"])

    def test_idempotency_and_id_binding(self):
        move = self.prepared()
        dispatch(self.store, "move_file", move)
        self.assertTrue(dispatch(self.store, "move_file", move)["idempotent"])
        with self.assertRaises(Refusal):
            dispatch(
                self.store,
                "move_file",
                {**move, "destination": "Organized/Notes/other.txt"},
            )

    def test_interruption_and_exact_recovery(self):
        move = self.prepared()
        with self.assertRaises(InterruptedError):
            self.store.move(**move, _interrupt=True)
        self.assertTrue((self.root / move["source"]).exists())
        self.assertTrue((self.root / move["destination"]).exists())
        result = self.store.recover(move["operation_id"])
        self.assertTrue(result["recovered"])
        self.assertFalse((self.root / move["source"]).exists())
        self.assertEqual(
            sha(lab.FILES[move["source"]].encode()),
            sha((self.root / move["destination"]).read_bytes()),
        )

    def test_ambiguous_recovery_preserves_both(self):
        move = self.prepared()
        with self.assertRaises(InterruptedError):
            self.store.move(**move, _interrupt=True)
        (self.root / move["destination"]).unlink()
        (self.root / move["destination"]).write_text("Foreign writer")
        with self.assertRaises(Refusal):
            self.store.recover(move["operation_id"])
        self.assertTrue((self.root / move["source"]).exists())

    def test_exclusive_creation_after_check(self):
        move = self.prepared()
        check = self.store.check

        def intervening(**args):
            result = check(**args)
            (self.root / args["destination"]).write_text("Concurrent claimant")
            return result

        with patch.object(self.store, "check", side_effect=intervening):
            with self.assertRaises(FileExistsError):
                self.store.move(**move)
        self.assertEqual(
            "Concurrent claimant", (self.root / move["destination"]).read_text()
        )
        self.assertTrue((self.root / move["source"]).exists())

    def test_path_escape_symlink_and_special_source(self):
        proposal = self.proposal()
        for destination in [
            "../outside.txt",
            "/tmp/outside.txt",
            "Organized/Notes/../bad.txt",
        ]:
            with self.subTest(destination=destination), self.assertRaises(Refusal):
                self.store.check(**{**proposal, "destination": destination})
        (self.root / "Inbox/link.txt").symlink_to(
            self.root / "Organized/Notes/README.txt"
        )
        with self.assertRaises(OSError):
            self.store.read("Inbox/link.txt")
        os.mkfifo(self.root / "Inbox/pipe")
        with self.assertRaises(Refusal):
            self.store.read("Inbox/pipe")
        os.link(self.root / "Inbox/notes-final.txt", self.root / "Inbox/hardlink.txt")
        with self.assertRaises(Refusal):
            self.store.read("Inbox/hardlink.txt")

    def test_plan_requires_distinct_sources_and_targets(self):
        with self.assertRaises(Refusal):
            dispatch(
                self.store,
                "prepare_moves",
                {"moves": [self.proposal(), self.proposal()]},
            )

    def test_reset_refuses_foreign_folder_and_symlink(self):
        with self.assertRaises(FileNotFoundError):
            lab.reset(Path(self.temp.name) / "not-a-lab", "normal")
        (self.root / "Organized").rename(self.root / "old-organized")
        (self.root / "Organized").symlink_to(
            self.root / "old-organized", target_is_directory=True
        )
        with self.assertRaises(ValueError):
            lab.reset(self.root, "normal")

    def test_installer_preserves_existing_configuration_and_content(self):
        spec = importlib.util.spec_from_file_location(
            "organizer_setup", lab.SKILL / "scripts/setup.py"
        )
        setup = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(setup)
        project = Path(self.temp.name) / "other-project"
        project.mkdir()
        (project / ".codex").mkdir()
        existing = 'model = "test-model"\n[mcp_servers.existing]\ncommand = "example"\n'
        (project / ".codex/config.toml").write_text(existing)
        (project / ".codex/hooks.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        "Stop": [{"hooks": [{"type": "command", "command": "true"}]}]
                    }
                }
            )
        )
        (project / "Inbox").mkdir()
        source = project / "Inbox/actual.txt"
        source.write_text("Authorized content")
        setup.configure(
            project, project, Path(self.temp.name) / "other-state", ["Notes", "Review"]
        )
        self.assertTrue(
            (project / ".codex/config.toml").read_text().startswith(existing)
        )
        self.assertIn(
            "Stop", json.loads((project / ".codex/hooks.json").read_text())["hooks"]
        )
        self.assertEqual("Authorized content", source.read_text())


if __name__ == "__main__":
    unittest.main()
