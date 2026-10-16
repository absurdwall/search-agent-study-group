"""Grader regression tests, not agent-workflow Evals."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))
import test_organizer
from runtime import dispatch
from evaluate_organizer import grade, scan
import lab

spec = importlib.util.spec_from_file_location("eval_runner", lab.HERE / "evals/run.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class EvaluationTests(unittest.TestCase):
    setUp = test_organizer.OrganizerTests.setUp
    tearDown = test_organizer.OrganizerTests.tearDown
    proposal = test_organizer.OrganizerTests.proposal
    def complete(self):
        moves = [self.proposal(p, f"Organized/{c}/{Path(p).name}") for p, c in lab.EXPECTED.items()]
        plan = dispatch(self.store, "prepare_moves", {"moves": moves})["prepared_moves"]
        for move in plan:
            dispatch(self.store, "move_file", move)
        dispatch(self.store, "record_report", {
            "summary": "Synthetic controller result", "completed_operation_ids": [m["operation_id"] for m in plan],
            "unresolved_paths": ["Organized/Review/misc.txt"], "interventions": []})
        return plan

    def test_only_new_exact_regular_metadata_is_excluded(self):
        self.complete()
        metadata = self.root / "Organized/.DS_Store"
        metadata.write_bytes(b"Synthetic Finder metadata")
        result = grade(self.root, self.state)
        self.assertTrue(result["passed"])
        self.assertEqual(["Organized/.DS_Store"], list(result["excluded_platform_metadata"]))
        other = self.root / "Organized/.unexpected"
        other.write_text("Unexpected must fail")
        self.assertFalse(grade(self.root, self.state)["checks"]["preservation"])
        other.unlink()
        metadata.unlink()
        metadata.symlink_to(self.root / "Organized/Notes/README.txt")
        self.assertFalse(grade(self.root, self.state)["checks"]["no_unsupported_paths"])

    def test_baseline_metadata_is_protected(self):
        self.complete()
        path = self.root / "Organized/.DS_Store"
        path.write_bytes(b"Original baseline metadata")
        baseline = json.loads((self.state / "baseline.json").read_text())
        baseline["Organized/.DS_Store"] = scan(self.root / "Organized")[0][".DS_Store"]
        (self.state / "baseline.json").write_text(json.dumps(baseline))
        self.assertTrue(grade(self.root, self.state)["passed"])
        path.write_text("Changed metadata")
        self.assertFalse(grade(self.root, self.state)["checks"]["preservation"])
        path.unlink()
        self.assertFalse(grade(self.root, self.state)["checks"]["existing_references_unchanged"])

    def test_hooks_must_match_each_completed_call(self):
        plan = self.complete()
        events = []
        for i, move in enumerate(plan):
            for event, decision in [("PreToolUse", "allow"), ("PostToolUse", "observed")]:
                events.append({"hook_event_name": event, "decision": decision,
                               "tool_name": "mcp__workspace_organizer__move_file",
                               "tool_use_id": str(i), "arguments": move})
        log = self.state / "hooks.jsonl"
        log.write_text("\n".join(json.dumps(e) for e in events))
        self.assertTrue(grade(self.root, self.state, True)["passed"])
        events[-1]["tool_use_id"] = "unrelated-call"
        log.write_text("\n".join(json.dumps(e) for e in events))
        self.assertFalse(grade(self.root, self.state, True)["checks"]["hook_integration"])

    def test_agent_failure_cannot_pass_on_valid_artifacts(self):
        self.complete()
        case = json.loads((lab.HERE / "evals/cases.json").read_text())["cases"][0]
        outcome = grade(self.root, self.state)
        self.assertFalse(runner.score(case, outcome, [], 1)["agent_process_succeeded"])
        self.assertFalse(runner.score(case, outcome, [], 0)["agent_turn_completed"])
