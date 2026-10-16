"""Minimal stdio MCP service and separate Codex lifecycle adapter."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import uuid

from operations import Store, Refusal, save


MOVE = {
    "type": "object",
    "properties": {
        key: {"type": "string"} for key in ["source", "destination", "expected_sha256"]
    },
    "required": ["source", "destination", "expected_sha256"],
    "additionalProperties": False,
}


def schema(properties, required=None):
    return {
        "type": "object",
        "properties": properties,
        "required": required or list(properties),
        "additionalProperties": False,
    }


TOOLS = [
    (
        "inspect_workspace",
        "Read authorized file previews, hashes and configured categories without making changes.",
        schema({}),
    ),
    (
        "read_file",
        "Read one authorized Inbox/Organized text file, at most 50,000 characters.",
        schema({"path": {"type": "string"}}),
    ),
    (
        "prepare_moves",
        "Record a content-based plan; assign operation IDs without moving user files.",
        schema(
            {"moves": {"type": "array", "items": MOVE, "minItems": 1, "maxItems": 100}}
        ),
    ),
    (
        "move_file",
        "Execute one prepared move, preserving contents and refusing destination replacement.",
        schema({**MOVE["properties"], "operation_id": {"type": "string"}}),
    ),
    (
        "recover_move",
        "Reconcile only the exact recorded interrupted move, preserving ambiguous states for review.",
        schema({"operation_id": {"type": "string"}}),
    ),
    (
        "record_report",
        "Save completion and uncertainty. unresolved_paths includes remaining Inbox files AND all Organized/Review files.",
        schema(
            {
                "summary": {"type": "string"},
                "completed_operation_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "unresolved_paths": {"type": "array", "items": {"type": "string"}},
                "interventions": {"type": "array", "items": {"type": "string"}},
            }
        ),
    ),
]


def validate_prepared(store, args):
    operation_id = args["operation_id"]
    path = store.record_path(operation_id)
    plan = json.loads((store.state / "plans" / f"{operation_id}.json").read_text())
    expected = {k: args[k] for k in ["source", "destination", "expected_sha256"]}
    if plan != expected:
        raise Refusal(
            "Move differs from its recorded plan. Inspect and prepare a new operation."
        )
    if path.exists():
        record = json.loads(path.read_text())
        if record["arguments"] == expected and record["status"] == "completed":
            return
        raise Refusal(
            "An operation is pending. Recover its exact operation ID before continuing."
        )
    store.check(**expected)


def dispatch(store, name, args):
    if name == "inspect_workspace":
        return store.inspect()
    if name == "read_file":
        parts = store.parts(args["path"])
        if parts[0] not in ["Inbox", "Organized"]:
            raise Refusal("Read only Inbox or Organized content.")
        data, _ = store.read(args["path"])
        return {
            "path": args["path"],
            "text": data.decode("utf-8")[:50000],
            "truncated": len(data.decode("utf-8")) > 50000,
        }
    if name == "prepare_moves":
        moves = args["moves"]
        if not 1 <= len(moves) <= 100:
            raise Refusal("Prepare between one and 100 moves.")
        if len({m["source"] for m in moves}) != len(moves) or len(
            {m["destination"] for m in moves}
        ) != len(moves):
            raise Refusal(
                "A plan must give each source and destination one distinct operation."
            )
        with store.locked():
            for move in moves:
                store.check(**move)
            prepared = []
            for move in moves:
                op = uuid.uuid4().hex
                save(store.state / "plans" / f"{op}.json", move)
                prepared.append({"operation_id": op, **move})
            store.log("plans.jsonl", moves=prepared)
        # Optional teaching controller acts as an external writer AFTER plan validation.
        # No fixture mutation exists in the policy handler or default operation service.
        event_command = store.config.get("fixture_event_command")
        if event_command:
            subprocess.run(
                event_command,
                input=json.dumps({"moves": prepared}),
                text=True,
                check=True,
                timeout=5,
                capture_output=True,
            )
        return {
            "prepared_moves": prepared,
            "notice": "Plan recorded. Each move revalidates actual state immediately before execution.",
        }
    if name == "move_file":
        validate_prepared(store, args)
        return store.move(**args)
    if name == "recover_move":
        return store.recover(**args)
    if name == "record_report":
        for op in args["completed_operation_ids"]:
            record = json.loads(store.record_path(op).read_text())
            if record["status"] != "completed":
                raise Refusal("A reported operation is not complete.")
        with store.locked():
            save(store.state / "report.json", args)
        return {"saved_report": str(store.state / "report.json")}
    raise Refusal("Unknown tool.")


def serve(store):
    for line in sys.stdin:
        try:
            req = json.loads(line)
            if "id" not in req:
                continue
            method = req.get("method")
            if method == "initialize":
                result = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "safe-workspace-organizer",
                        "version": "1.0.0",
                    },
                }
            elif method == "tools/list":
                result = {
                    "tools": [
                        {"name": n, "description": d, "inputSchema": s}
                        for n, d, s in TOOLS
                    ]
                }
            elif method == "ping":
                result = {}
            elif method == "tools/call":
                name = req["params"]["name"]
                args = req["params"].get("arguments", {})
                store.log("requests.jsonl", tool=name, arguments=args)
                try:
                    payload = dispatch(store, name, args)
                    result = {
                        "content": [{"type": "text", "text": json.dumps(payload)}]
                    }
                except (
                    OSError,
                    ValueError,
                    KeyError,
                    TypeError,
                    subprocess.SubprocessError,
                ) as error:
                    store.log(
                        "failures.jsonl", tool=name, arguments=args, reason=str(error)
                    )
                    result = {
                        "isError": True,
                        "content": [
                            {"type": "text", "text": f"{type(error).__name__}: {error}"}
                        ],
                    }
            else:
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": req["id"],
                            "error": {"code": -32601, "message": "Unknown method"},
                        }
                    ),
                    flush=True,
                )
                continue
            print(
                json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": result}),
                flush=True,
            )
        except (ValueError, KeyError, TypeError) as error:
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32600, "message": str(error)},
                    }
                ),
                flush=True,
            )


def hook(config):
    # Adapter failure explicitly denies matched mutations; runtime failure still needs service enforcement.
    event = json.load(sys.stdin)
    reason = None
    try:
        store = Store(config)
        args = event.get("tool_input", {})
        if event.get("hook_event_name") == "PreToolUse":
            if event.get("tool_name") == "mcp__workspace_organizer__move_file":
                validate_prepared(store, args)
            elif event.get("tool_name") == "mcp__workspace_organizer__recover_move":
                store.record_path(args["operation_id"])
        store.log(
            "hooks.jsonl",
            **{
                k: event.get(k)
                for k in [
                    "hook_event_name",
                    "tool_name",
                    "tool_use_id",
                    "session_id",
                    "turn_id",
                    "model",
                ]
            },
            arguments=args,
            decision="allow"
            if event.get("hook_event_name") == "PreToolUse"
            else "observed",
        )
    except Exception as error:
        reason = f"{type(error).__name__}: {error}"
        try:
            store.log(
                "hooks.jsonl",
                **{
                    k: event.get(k)
                    for k in [
                        "hook_event_name",
                        "tool_name",
                        "tool_use_id",
                        "session_id",
                        "turn_id",
                        "model",
                    ]
                },
                arguments=event.get("tool_input", {}),
                decision="deny",
                reason=reason,
            )
        except Exception:
            pass
    if reason and event.get("hook_event_name") == "PreToolUse":
        print(
            json.dumps(
                {
                    "systemMessage": "Organizer policy refused this move; preserve both files and inspect again.",
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": reason,
                    },
                }
            )
        )
    else:
        print("{}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["serve", "hook"])
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    if args.mode == "hook":
        hook(args.config)
    else:
        serve(Store(args.config))
