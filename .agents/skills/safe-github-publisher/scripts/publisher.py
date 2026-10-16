"""Commit-bound publication service. Development uses only disposable local targets."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

PATTERNS = [
    ("synthetic teaching marker", re.compile(rb"DEMO_SECRET_[A-Z0-9_]+")),
    (
        "private key header",
        re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    ("token-shaped value", re.compile(rb"gh[pousr]_[A-Za-z0-9]{20,}")),
]


def git(repo, *args, check=True):
    return subprocess.run(
        ["git", "--no-optional-locks", "-C", str(repo), *args],
        capture_output=True,
        check=check,
        timeout=30,
    )


def snapshots(repo, staged=False):
    if staged:
        entries = git(repo, "ls-files", "--stage", "-z").stdout.split(b"\0")
        return [("index", entries)]
    revisions = (
        git(repo, "rev-list", "--max-count=201", "HEAD").stdout.decode().splitlines()
    )
    if len(revisions) > 200:
        raise ValueError(
            "History exceeds the 200-commit scan budget; use a maintained scanner."
        )
    return [
        (rev, git(repo, "ls-tree", "-rz", rev).stdout.split(b"\0")) for rev in revisions
    ]


def scan(repo, staged=False):
    findings = []
    seen = set()
    total = 0
    count = 0
    for snapshot, entries in snapshots(repo, staged):
        if not staged:
            metadata = git(repo, "cat-file", "commit", snapshot).stdout
            total += len(metadata)
            if total > 32 * 1024 * 1024:
                raise ValueError("Metadata scan budget exceeded; publication refused.")
            for reason, pattern in PATTERNS:
                if pattern.search(metadata):
                    findings.append(
                        {
                            "snapshot": snapshot,
                            "path": "[commit metadata]",
                            "reason": reason,
                        }
                    )
        for entry in entries:
            if not entry:
                continue
            head, name = entry.split(b"\t", 1)
            fields = head.split()
            mode = fields[0]
            oid = fields[1] if staged else fields[2]
            path = name.decode("utf-8", "replace")
            if (oid, path) in seen:
                continue
            seen.add((oid, path))
            count += 1
            if count > 2000:
                raise ValueError("File scan budget exceeded; publication refused.")
            if mode not in [b"100644", b"100755"]:
                findings.append(
                    {
                        "snapshot": snapshot,
                        "path": path,
                        "reason": "non-regular Git entry requires review",
                    }
                )
                continue
            size = int(git(repo, "cat-file", "-s", oid.decode()).stdout)
            total += size
            if size > 10 * 1024 * 1024 or total > 32 * 1024 * 1024:
                raise ValueError("Byte scan budget exceeded; publication refused.")
            data = git(repo, "cat-file", "blob", oid.decode()).stdout
            if Path(path).name.startswith(".env") and Path(path).name != ".env.example":
                findings.append(
                    {
                        "snapshot": snapshot,
                        "path": path,
                        "reason": "tracked environment file",
                    }
                )
            for reason, pattern in PATTERNS:
                if pattern.search(data):
                    findings.append(
                        {"snapshot": snapshot, "path": path, "reason": reason}
                    )
    return findings


class Publisher:
    def __init__(self, config):
        self.config = json.loads(Path(config).read_text())
        self.repo = Path(self.config["repo"]).resolve(strict=True)
        self.state = Path(self.config["state"]).resolve(strict=True)
        if self.state.is_relative_to(self.repo):
            raise ValueError("Keep publication state outside the source repository.")
        self.target = self.config["target"]
        self.ref = self.config["ref"]
        if (
            not re.fullmatch(r"refs/heads/[A-Za-z0-9][A-Za-z0-9_/-]{0,100}", self.ref)
            or ".." in self.ref
        ):
            raise ValueError("Invalid publication ref.")
        if self.target.startswith("https://"):
            if not self.config.get("allow_network") or not re.fullmatch(
                r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?",
                self.target,
            ):
                raise ValueError(
                    "Network publication is disabled or target is not an exact HTTPS GitHub repository."
                )
        else:
            target = Path(self.target)
            if (
                not target.is_absolute()
                or target.is_symlink()
                or target.resolve() == self.repo
            ):
                raise ValueError("Use an exact separate local bare target.")
            if (
                git(target, "rev-parse", "--is-bare-repository").stdout.strip()
                != b"true"
            ):
                raise ValueError("Local target must be a bare repository.")

    def log(self, file, **record):
        with (self.state / file).open("a") as stream:
            stream.write(
                json.dumps({"at": datetime.now(timezone.utc).isoformat(), **record})
                + "\n"
            )

    def inspect(self):
        return {
            "repo": str(self.repo),
            "target": self.target,
            "ref": self.ref,
            "local_simulation": not self.target.startswith("https://"),
            "head": git(self.repo, "rev-parse", "HEAD").stdout.decode().strip(),
            "status": git(
                self.repo, "status", "--porcelain=v1", "--untracked-files=all"
            ).stdout.decode(),
        }

    def prepare(self):
        info = self.inspect()
        findings = scan(self.repo, True) + scan(self.repo)
        if findings or info["status"]:
            return {
                "ready": False,
                "findings": findings,
                "status": info["status"],
                "notice": "No publication. Inspect staged content and history; current-file cleanup does not erase prior commits.",
            }
        plan = {
            k: info[k] for k in ["repo", "target", "ref", "head", "local_simulation"]
        }
        plan_id = hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest()
        plan["plan_id"] = plan_id
        plan["confirmation"] = f"publish {info['head']} to {self.target} {self.ref}"
        (self.state / "plan.json").write_text(json.dumps(plan, indent=2))
        self.log("plans.jsonl", **plan)
        return {"ready": True, **plan}

    def check(self, args):
        plan = json.loads((self.state / "plan.json").read_text())
        if args != {k: plan[k] for k in ["plan_id", "confirmation"]}:
            raise ValueError("Publication arguments differ from the reviewed plan.")
        current = self.prepare()
        if not current["ready"] or current["plan_id"] != plan["plan_id"]:
            raise ValueError(
                "Repository or target changed, or checks failed. Inspect and prepare again before renewed authorization."
            )
        return plan

    def publish(self, args):
        plan = self.check(args)
        result = git(
            self.repo,
            "-c",
            "push.gpgSign=false",
            "push",
            "--porcelain",
            "--no-follow-tags",
            "--recurse-submodules=no",
            self.target,
            f"{plan['head']}:{self.ref}",
        )
        readback = (
            git(self.repo, "ls-remote", self.target, self.ref).stdout.decode().split()
        )
        if not readback or readback[0] != plan["head"]:
            raise ValueError(
                "Push returned but target readback did not confirm the planned commit."
            )
        outcome = {
            "published": True,
            "head": plan["head"],
            "target": self.target,
            "ref": self.ref,
            "readback": readback[0],
            "local_simulation": plan["local_simulation"],
        }
        (self.state / "result.json").write_text(json.dumps(outcome, indent=2))
        self.log("publications.jsonl", **outcome)
        return outcome


TOOLS = [
    ("inspect_repository", "Read source, target, ref, HEAD and worktree state.", {}),
    (
        "prepare_publication",
        "Scan staged snapshot and reachable history; create an exact commit-bound plan.",
        {},
    ),
    (
        "publish",
        "Publish only the checked plan to the configured target, without force.",
        {"plan_id": {"type": "string"}, "confirmation": {"type": "string"}},
    ),
]


def serve(publisher):
    for line in sys.stdin:
        req = json.loads(line)
        if "id" not in req:
            continue
        method = req.get("method")
        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "safe-github-publisher", "version": "1.0.0"},
            }
        elif method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": n,
                        "description": d,
                        "inputSchema": {
                            "type": "object",
                            "properties": props,
                            "required": list(props),
                            "additionalProperties": False,
                        },
                    }
                    for n, d, props in TOOLS
                ]
            }
        elif method == "ping":
            result = {}
        elif method == "tools/call":
            name = req["params"]["name"]
            args = req["params"].get("arguments", {})
            publisher.log("requests.jsonl", tool=name, arguments=args)
            try:
                if name == "inspect_repository":
                    value = publisher.inspect()
                elif name == "prepare_publication":
                    value = publisher.prepare()
                elif name == "publish":
                    value = publisher.publish(args)
                else:
                    raise ValueError("Unknown tool.")
                result = {"content": [{"type": "text", "text": json.dumps(value)}]}
            except Exception as error:
                result = {
                    "isError": True,
                    "content": [{"type": "text", "text": str(error)}],
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


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["serve", "hook", "git-hook"])
    p.add_argument("--config")
    p.add_argument("--repo")
    p.add_argument("--kind", choices=["pre-commit", "pre-push"])
    args = p.parse_args()
    if args.mode == "git-hook":
        try:
            findings = scan(Path(args.repo), args.kind == "pre-commit")
            if findings:
                print(json.dumps(findings), file=sys.stderr)
                sys.exit(2)
        except Exception as error:
            print(str(error), file=sys.stderr)
            sys.exit(2)
    elif args.mode == "serve":
        serve(Publisher(args.config))
    else:
        event = json.load(sys.stdin)
        reason = None
        try:
            pub = Publisher(args.config)
            if event["hook_event_name"] == "PreToolUse":
                pub.check(event["tool_input"])
            pub.log(
                "hooks.jsonl",
                **{
                    k: event.get(k)
                    for k in [
                        "hook_event_name",
                        "tool_name",
                        "tool_use_id",
                        "session_id",
                        "turn_id",
                    ]
                },
                arguments=event.get("tool_input"),
                decision="allow"
                if event["hook_event_name"] == "PreToolUse"
                else "observed",
            )
        except Exception as error:
            reason = str(error)
            try:
                pub.log(
                    "hooks.jsonl",
                    decision="deny",
                    reason=reason,
                    arguments=event.get("tool_input"),
                )
            except Exception:
                pass
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": reason,
                    }
                }
            )
            if reason and event.get("hook_event_name") == "PreToolUse"
            else "{}"
        )
