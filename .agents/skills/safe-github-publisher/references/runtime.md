# Runtime and publication boundaries

Register `python3 scripts/publisher.py serve --config /absolute/path/publisher.json`
as the project-local `safe_publisher` MCP server. Config contains `repo`, external
`state`, exact `target`, `ref` (for example `refs/heads/study-demo`), and
`allow_network` (false by default). The teaching lab provisions disposable source
and bare target repositories and copies this Skill into the Desktop project.

PreToolUse and PostToolUse match only `mcp__safe_publisher__publish`, calling
`publisher.py hook --config CONFIG`. Review and trust the exact project definitions.
For a real remote, require native per-call approval for the publish tool; the
confirmation string binds arguments and is not proof of human consent. A project
operator must deliberately enable network mode and choose the precise HTTPS
GitHub repository. Network mode is untested in this teaching implementation.

The push explicitly disables follow-tags and submodule recursion, so local Git
preferences cannot broaden the reviewed ref selection. Commit metadata is scanned
as well as file snapshots. The local evaluator checks the complete target ref set.

The bundled scanner detects a teaching marker, common token shapes, private-key
headers, and tracked environment files. It examines the staged snapshot and up to
200 reachable commit snapshots (bounded by file and byte budgets), rejecting an
incomplete scan. This is a conservative preflight, not a comprehensive secret
scanner. Production repositories should also use a maintained detector, native
GitHub protections, and appropriate branch rules. No synthetic marker establishes
GitHub detector coverage.

Local Git `pre-commit`/`pre-push` hooks can use `publisher.py git-hook --repo REPO
--kind pre-commit|pre-push`. They exit nonzero on failed checks. They are local
controls that other Git clients can bypass; the service independently checks
before its own publication. Host-side GitHub rules and bypass permissions are
separate. Successful local target readback proves only the disposable simulation.
