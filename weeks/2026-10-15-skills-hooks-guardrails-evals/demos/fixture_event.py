"""Instructor-only deterministic concurrent writer; never imported by policy code."""
import hashlib
import json
from pathlib import Path
import sys


def main():
    config = json.loads(Path(sys.argv[1]).read_text())
    state = Path(config["state"])
    scenario = json.loads((state / "scenario.json").read_text())
    event = json.load(sys.stdin)
    if scenario["name"] != "conflict" or scenario.get("injected"):
        return
    move = event["moves"][0]
    target = Path(config["workspace"]) / move["destination"]
    data = b"Concurrent writer: separate workshop follow-up. Preserve this file.\n"
    with target.open("xb") as stream:
        stream.write(data)
    scenario.update(
        injected=True, path=move["destination"], sha256=hashlib.sha256(data).hexdigest()
    )
    (state / "scenario.json").write_text(json.dumps(scenario, indent=2))
    with (state / "environment.jsonl").open("a") as stream:
        stream.write(
            json.dumps(
                {
                    "actor": "instructor-fixture",
                    "event": "concurrent-destination-created",
                    "path": move["destination"],
                    "sha256": scenario["sha256"],
                }
            )
            + "\n"
        )


if __name__ == "__main__":
    main()
