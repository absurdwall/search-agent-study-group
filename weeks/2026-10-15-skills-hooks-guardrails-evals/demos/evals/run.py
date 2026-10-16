"""Small Codex CLI trial runner; not a replacement agent or evaluation framework."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import lab
from evaluate_organizer import grade


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def score(case, outcome, events, exit_code):
    """A complete process plus task evidence is required; a tidy tree is insufficient."""
    return {
        "agent_process_succeeded": exit_code == 0,
        "agent_turn_completed": any(e.get("type") == "turn.completed" for e in events)
            and not any(e.get("type") in ("turn.failed", "error") for e in events),
        "outcome_and_hooks": outcome["passed"],
        "case_file_count": outcome["files"] == case["expected_files"],
        "case_move_count": outcome["completed_moves"] == case["expected_moves"],
        "case_intervention": (outcome["hook_evidence"]["denied"] >= case["minimum_denials"]
                              and (case["scenario"] != "conflict" or outcome["scenario"].get("injected", False))),
    }


def run(project, case_id, timeout=600):
    project, state = lab.paths(project)  # Refuse a non-lab folder before reset.
    definitions = json.loads((HERE / "cases.json").read_text())
    case = next(c for c in definitions["cases"] if c["id"] == case_id)
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("Install/authenticate Codex CLI and review project hooks first.")
    # The caller must stop any Desktop turn. Reset archives all previous evidence.
    lab.reset(project, case["scenario"])
    trial = state / "trial"
    trial.mkdir()
    prompt = definitions["prompt"]
    (trial / "prompt.txt").write_text(prompt + "\n")
    shutil.copy2(HERE / "cases.json", trial / "cases.json")
    for name in ("config.toml", "hooks.json"):
        shutil.copy2(project / ".codex" / name, trial / ("project-" + name))
    command = [codex, "--no-daemon", "exec", "--json", "--color", "never",
               "-C", str(project), "-o", str(trial / "final-message.md"), prompt]
    metadata = {"case": case_id, "started_at": datetime.now(timezone.utc).isoformat(),
                "command": command, "runtime": subprocess.check_output([codex, "--version"], text=True).strip(),
                "source_hashes": {str(p.relative_to(project)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in sorted((project / ".agents/skills/safe-workspace-organizer").rglob("*"))
                                  if p.is_file() and "__pycache__" not in p.parts},
                "harness_hashes": {str(p.relative_to(lab.HERE)): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in [HERE / "run.py", HERE / "cases.json", lab.HERE / "lab.py",
                                             lab.HERE / "evaluate_organizer.py", lab.HERE / "fixture_event.py"]},
                "status": "running"}
    save(trial / "run.json", metadata)
    error = None
    with (trial / "trace.jsonl").open("w") as trace, (trial / "stderr.txt").open("w") as stderr:
        try:
            result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=trace, stderr=stderr,
                                    timeout=timeout, check=False)
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            exit_code, error = 124, "Agent timeout; partial evidence retained. Stop/reconcile before retrying."
        except OSError as exc:
            exit_code, error = 127, f"Could not launch Codex: {exc}"
    events = []
    for line in (trial / "trace.jsonl").read_text().splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            error = "Malformed/incomplete JSONL trace; retained for inspection."
    outcome = grade(project, state, require_hooks=True)
    save(state / "evaluation.json", outcome)
    checks = score(case, outcome, events, exit_code)
    if error:
        checks["capture_complete"] = False
    metadata.update(status="finished", finished_at=datetime.now(timezone.utc).isoformat(),
                    exit_code=exit_code, error=error,
                    thread_ids=[e["thread_id"] for e in events if e.get("type") == "thread.started"],
                    usage=[e.get("usage") for e in events if e.get("type") == "turn.completed"])
    save(trial / "run.json", metadata)
    result = {"passed": all(checks.values()), "checks": checks,
              "human_review": {"status": "pending", "rubric": definitions["human_rubric"]},
              "evidence": str(state), "outcome": outcome}
    save(trial / "result.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="An idle disposable lab project; prior evidence is archived.")
    parser.add_argument("--case", choices=["normal", "conflict"], required=True)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    result = run(args.project, args.case, args.timeout)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)
