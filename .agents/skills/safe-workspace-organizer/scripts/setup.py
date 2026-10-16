"""Install project runtime registration for a separately authorized real inbox.

No fixture data, no global changes, no implicit trust. Python >=3.11, POSIX.
"""
import argparse
import json
from pathlib import Path
import shlex
import sys
import tomllib


def configure(project, workspace, state, categories):
    project, workspace, state = (
        Path(p).expanduser().resolve() for p in [project, workspace, state]
    )
    if (
        state.exists()
        or state.is_relative_to(workspace)
        or workspace.is_relative_to(state)
    ):
        raise ValueError("Choose a new external state directory.")
    if not (workspace / "Inbox").is_dir() or (workspace / "Inbox").is_symlink():
        raise ValueError(
            "Authorized workspace must already contain a real Inbox directory."
        )
    if (workspace / "Organized").is_symlink():
        raise ValueError("Organized cannot be a symlink.")
    import re

    if not categories or any(
        not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,40}", c) for c in categories
    ):
        raise ValueError("Use simple category names beginning with a letter.")
    codex = project / ".codex"
    config_path = codex / "config.toml"
    hooks_path = codex / "hooks.json"
    existing = config_path.read_text() if config_path.exists() else ""
    parsed = tomllib.loads(existing)
    if "workspace_organizer" in parsed.get("mcp_servers", {}):
        raise ValueError(
            "Organizer registration exists; preserve it and review changes manually."
        )
    if parsed.get("features", {}).get("hooks") is False:
        raise ValueError(
            "This project disables hooks; review that setting before installing."
        )
    hooks = json.loads(hooks_path.read_text()) if hooks_path.exists() else {"hooks": {}}
    if not isinstance(hooks.get("hooks"), dict):
        raise ValueError("Existing hooks.json has an unexpected shape.")
    runtime = Path(__file__).with_name("runtime.py").resolve()
    service = {
        "workspace": str(workspace),
        "state": str(state),
        "categories": categories,
    }
    args = [str(runtime), "serve", "--config", str(state / "service.json")]
    addition = (
        "\n[mcp_servers.workspace_organizer]\ncommand = "
        + json.dumps(sys.executable)
        + "\nargs = "
        + json.dumps(args)
        + "\nrequired = true\n"
    )
    for tool in [
        "inspect_workspace",
        "read_file",
        "prepare_moves",
        "move_file",
        "recover_move",
        "record_report",
    ]:
        addition += f'\n[mcp_servers.workspace_organizer.tools.{tool}]\napproval_mode = "approve"\n'
    tomllib.loads(existing + addition)
    command = shlex.join(
        [sys.executable, str(runtime), "hook", "--config", str(state / "service.json")]
    )
    for event in ["PreToolUse", "PostToolUse"]:
        hooks["hooks"].setdefault(event, []).append(
            {
                "matcher": "^mcp__workspace_organizer__(move_file|recover_move)$",
                "hooks": [
                    {
                        "type": "command",
                        "command": command,
                        "timeout": 5,
                        "statusMessage": "Organizer move policy",
                    }
                ],
            }
        )
    # Validation completes before writing project registration or creating categories.
    state.mkdir(parents=True)
    for directory in ["operations", "plans", "backups"]:
        (state / directory).mkdir()
    (state / "service.json").write_text(json.dumps(service, indent=2))
    for category in categories:
        (workspace / "Organized" / category).mkdir(parents=True, exist_ok=True)
    codex.mkdir(parents=True, exist_ok=True)
    if config_path.exists():
        (state / "config-before.toml").write_text(existing)
    if hooks_path.exists():
        (state / "hooks-before.json").write_text(hooks_path.read_text())
    config_path.write_text(existing + addition)
    hooks_path.write_text(json.dumps(hooks, indent=2))
    return {
        "config": str(config_path),
        "hooks": str(hooks_path),
        "state": str(state),
        "next": "Review and trust the project and exact hooks through /hooks. Reopen Desktop. Verify actual session permissions separately.",
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project", required=True)
    p.add_argument("--workspace", required=True)
    p.add_argument("--state", required=True)
    p.add_argument(
        "--categories", nargs="+", default=["Notes", "Reports", "Images", "Review"]
    )
    a = p.parse_args()
    print(
        json.dumps(configure(a.project, a.workspace, a.state, a.categories), indent=2)
    )
