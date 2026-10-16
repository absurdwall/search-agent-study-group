# Runtime contract

Install the Skill in a project's `.agents/skills/safe-workspace-organizer` folder.
For a real authorized workspace, run `python3 scripts/setup.py --project PROJECT
--workspace WORKSPACE --state NEW_EXTERNAL_STATE_DIRECTORY`. The workspace must
already have an Inbox; setup preserves its files, creates the selected Organized
categories, backs up existing project config, and adds only its namespaced runtime
and hook registrations. It refuses an existing organizer registration. It never
trusts hooks or changes global settings. Python 3.11+ and macOS/Linux are required.

The runtime is a separately registered `workspace_organizer` stdio MCP server:
`python3 scripts/runtime.py serve --config /absolute/path/service.json`.
The config selects an authorized workspace, separate state directory, and category
names. Setup must initialize both before invoking the Skill. The teaching lab's
`lab.py provision` command does this and registers project-local hooks. Copying a
Skill folder alone does not register hooks or authorize a filesystem root.

The source tree is `Inbox/`; destinations are `Organized/<category>/<filename>`.
Sources can be nested regular files. Absolute paths, dot components, symlinks,
hard-linked sources, special files, replacement and stale content hashes are refused.
Binary previews are marked as such; preserve them in Review unless their type and
user context establish a useful category. A preview is bounded, not a full parser.

Each prepared move receives an operation ID. Its durable intent, original bytes,
destination identity and completion are recorded outside the mutable workspace.
An interrupted link/unlink operation can leave both names. `recover_move` finishes
only the recorded operation when identities and hashes match; it refuses ambiguous
states. Backups are recovery evidence, not permission to overwrite an unrelated file.
Cross-filesystem moves are refused. A completed ID is idempotent; reusing it for
different arguments is refused. Serial execution is intentional.

PreToolUse checks proposed structured arguments and returns an explicit denial
with a safe alternative. The operation service checks again without relying on
the hook, including after filesystem changes. PostToolUse records observations;
it is not rollback. Handler errors explicitly deny matched mutations where possible,
but runtime hook errors can fail open: the service remains the action boundary.

This is preservation tooling for cooperative local workflows. Descriptor-based
paths and exclusive creation reduce accidental races, but a hostile process with
the same user privileges can alter data, backups or code. Full Access Codex also
has other tools. Verify the real session permission profile separately; project
defaults do not necessarily override an existing Desktop session. This service
does not claim OS isolation, power-loss durability or comprehensive metadata backup.
