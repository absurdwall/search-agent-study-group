import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import publisher_lab

spec = importlib.util.spec_from_file_location(
    "publisher", publisher_lab.SKILL / "scripts/publisher.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PublisherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "fixture"
        info = publisher_lab.provision(self.root)
        self.repo = Path(info["repo"])
        self.pub = module.Publisher(info["config"])

    def tearDown(self):
        self.temp.cleanup()

    def arguments(self):
        p = self.pub.prepare()
        self.assertTrue(p["ready"])
        return {k: p[k] for k in ["plan_id", "confirmation"]}

    def test_local_publication_and_independent_readback(self):
        self.assertTrue(self.pub.publish(self.arguments())["published"])
        self.assertTrue(publisher_lab.evaluate(self.root)["passed"])

    def test_follow_tags_configuration_cannot_expand_publication(self):
        module.git(self.repo, "config", "push.followTags", "true")
        module.git(
            self.repo,
            "tag",
            "-a",
            "private-workshop-notes",
            "-m",
            "DEMO_SECRET_IN_TAG_NOT_FOR_PUBLICATION",
        )
        self.pub.publish(self.arguments())
        refs = (
            module.git(self.root / "target.git", "for-each-ref", "--format=%(refname)")
            .stdout.decode()
            .splitlines()
        )
        self.assertEqual(["refs/heads/study-demo"], refs)
        self.assertTrue(publisher_lab.evaluate(self.root)["passed"])

    def test_commit_metadata_marker_is_not_ignored(self):
        module.git(
            self.repo,
            "commit",
            "--allow-empty",
            "-qm",
            "DEMO_SECRET_SYNTHETIC_COMMIT_MESSAGE",
        )
        result = self.pub.prepare()
        self.assertFalse(result["ready"])
        self.assertTrue(
            any(x["path"] == "[commit metadata]" for x in result["findings"])
        )

    def test_staged_marker_blocks_preparation_and_real_git_hook(self):
        (self.repo / "credentials.txt").write_text(
            "DEMO_SECRET_NOT_A_REAL_CREDENTIAL\n"
        )
        module.git(self.repo, "add", "credentials.txt")
        self.assertFalse(self.pub.prepare()["ready"])
        commit = module.git(self.repo, "commit", "-m", "Should fail", check=False)
        self.assertNotEqual(commit.returncode, 0)
        self.assertIn(b"synthetic teaching marker", commit.stderr)

    def test_clean_worktree_does_not_hide_historical_marker(self):
        (self.repo / "credentials.txt").write_text("DEMO_SECRET_NEVER_VALID\n")
        module.git(self.repo, "add", ".")
        module.git(
            self.repo,
            "-c",
            "core.hooksPath=/dev/null",
            "commit",
            "-qm",
            "Synthetic fault injection",
        )
        module.git(self.repo, "rm", "credentials.txt")
        module.git(self.repo, "commit", "-qm", "Remove current file")
        self.assertEqual("", self.pub.inspect()["status"])
        self.assertFalse(self.pub.prepare()["ready"])

    def test_direct_publish_rechecks_stale_plan_without_hook(self):
        args = self.arguments()
        (self.repo / "README.md").write_text("Changed after approval")
        with self.assertRaises(ValueError):
            self.pub.publish(args)
        self.assertFalse((self.root / "state/result.json").exists())

    def test_target_binding_and_network_default(self):
        args = self.arguments()
        with self.assertRaises(ValueError):
            self.pub.publish(
                {**args, "confirmation": args["confirmation"] + " other target"}
            )
        p = self.root / "state/publisher.json"
        c = json.loads(p.read_text())
        c["target"] = "https://github.com/example/disposable.git"
        p.write_text(json.dumps(c))
        with self.assertRaises(ValueError):
            module.Publisher(p)


if __name__ == "__main__":
    unittest.main()
