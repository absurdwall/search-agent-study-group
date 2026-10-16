# Organizer Skill evaluations

An Eval starts with a request, lets Codex run the Skill, records what happened,
and grades the resulting files and operation evidence. `evaluate_organizer.py`
alone is the last step: it reads an existing run and never starts an agent.

## Components and ownership

| File or capability | Role | Owner |
| --- | --- | --- |
| `evals/cases.json` | Two complete-run cases, shared natural prompt, expected counts, human rubric | Project code/data |
| `lab.py: FILES, EXPECTED` | Synthetic seed contents and independent category oracle | Project code/data |
| `lab.py provision/reset` | Install disposable project; restore seed and archive earlier evidence | Project code |
| `fixture_event.py` | In conflict case, create one concurrent destination after planning | Project code; instructor environment |
| `.agents/skills/safe-workspace-organizer/SKILL.md` | Agent's actual instructions; no grader answers | Project Skill |
| Skill `scripts/runtime.py` and `operations.py` | MCP tools, hook adapter and guarded file operations | Project code |
| Project `.codex/config.toml`, `.codex/hooks.json` | Generated server registration and lifecycle subscriptions | Project configuration, consumed by Codex |
| Skill discovery, MCP client, lifecycle dispatch, hook trust | Load instructions, serve tool calls, run reviewed hook commands | Built into compatible Codex runtimes |
| Desktop conversation | Manual agent execution and observable feedback | Codex Desktop |
| `codex exec --json -o ...` | Automated agent execution, JSONL trace, final response | Codex CLI |
| `evals/run.py` | Reset, invoke CLI, capture output, call existing grader, enforce case counts | Project code |
| `evaluate_organizer.py` | Independent deterministic artifact grader, imports no service/hook policy | Project code |
| `tests/` | Operation, installer, publisher and grader regressions, without an LLM | Project tests |
| `lab.py counterexamples` | Copied incorrect outcomes to check grader sensitivity | Project grader controls, not agent trials |

We keep the grader and fixture at their existing paths to preserve imports and
commands. The small `evals/` folder separates case definitions, trial runner and
methodology without relocating the working service or introducing a framework.
The publisher remains a secondary local-only demonstration with its own tests
and `publisher_lab.py evaluate`; it is not part of these organizer cases.

## Desktop classroom trial

Follow the [prepared English classroom Page](https://chatgpt.com/space/page_5c02287fab708191a9bd674ba6751694)
and the six Organizer steps in INSTRUCTOR.md: explain → Run A → grade A → Run B
→ grade B/compare → recorded improvement and recap. The requested combined lesson
then continues with the Page's distinct local-publication Part B in the SAME
worker. Configure both services before it starts. Publisher has its own checks
and does not change the two Organizer cases. Copied-outcome grader controls
remain a separate extension. Announce each grading step visibly in the guide after
the worker finishes; it should never be discoverable only inside a tool trace.
Both live runs use the same Skill version; they differ in the concurrent-writer
condition, not in a before/after improvement.

Use the exact setup and commands in `../INSTRUCTOR.md`:

1. Open a NEW guiding chat for class, separate from the development chat.
   Provision/review the disposable project once and explain the components.
2. With all fixture users idle, reset to normal. The guide creates ONE local
   execution chat in the saved demo project using gpt-6-luna / max and the
   clickable desktop_prompt_template from cases.json. Fill skill_path with the
   installed SKILL.md path, without angle-bracket wrappers. Keep one `$` in the
   label, matching the app's native Skill-reference format. Creation submits the
   initial request. Verify source opening separately from agent Skill loading.
3. Wait for the worker's final response. Explain what happened in the guiding
   chat, then run lab.py evaluate --project "$DEMO_PROJECT" --require-hooks.
4. Archive/reset to conflict only while the worker is idle. Send the next
   natural request to that SAME execution chat, with the short notice that the
   demo folder was reset. Wait, grade and explain again. Keep the execution
   thread ID plus a distinct turn ID and archived evidence per scene.

This is exactly two classroom chats: one guide and one worker. The guide owns
Evals, log inspection and fuller English explanations; the worker performs all
scene actions across successive turns. It receives no step-by-step recovery
coaching. Optional warm-ups remain in the same worker, with a reset before the
full case. The post-run grader itself still does not launch an agent or read the
Desktop conversation. Keep the conversation and turn IDs alongside its evidence.

The older Luna rehearsals used fresh chats per case and remain historical case
evidence. The first two-chat live rehearsal in INSTRUCTOR.md now verifies one
worker reused across four turns. Its normal scene passed automatic checks but
exposed hash-copy errors and an inaccurate explanation. The presenter also
reported a Skill-link click problem; corrected native prompt-link formatting
needs visual confirmation. The classroom sequence remains distinct from the
optional fresh-process CLI regression route below.

## Automated trial using Codex CLI

After the same provision/trust setup, with all Desktop turns in that project idle:

```sh
python3 weeks/2026-10-15-skills-hooks-guardrails-evals/demos/evals/run.py \
  --project "$DEMO_PROJECT" --case normal
python3 weeks/2026-10-15-skills-hooks-guardrails-evals/demos/evals/run.py \
  --project "$DEMO_PROJECT" --case conflict
```

Each invocation resets only the marked disposable lab. Previous artifacts and
resulting files go to `state/runs/<timestamp>/`; the current run lives directly
in `state/`. Do not run these concurrently or reset an active agent. The runner
uses `codex --no-daemon exec --json -C PROJECT -o FINAL PROMPT`. `--no-daemon`
keeps this trial from restarting or reconfiguring a shared Desktop daemon.
It inherits the reviewed project's permissions, model and normal CLI auth.
It does not bypass hook trust, copy credentials or select another model.
Current CLI 0.160.0 supports this command; older article examples use
`--full-auto`, which this installation no longer supports.

Exit 0 means all automatic checks passed. Exit 1 means a process, capture,
case or artifact check failed. Inspect `trial/stderr.txt` and `trial/run.json`
for setup/runtime failures before diagnosing the Skill. A 600 second timeout
retains partial evidence and fails the trial; reconcile any interrupted operation
before retrying. Human review remains explicitly pending in `trial/result.json`.

## Evidence outside the agent's working files

```text
STATE/
  service.json                   # bound workspace, categories and optional fixture callback
  expected.json                  # category oracle generated from lab.EXPECTED
  baseline.json                  # original path → SHA-256, with duplicate multiplicity
  scenario.json                  # normal/conflict and any actual concurrent file
  plans.jsonl, plans/*.json       # planned tool arguments and operation IDs
  requests.jsonl                 # tools/call inputs received by the custom MCP service
  hooks.jsonl                    # events received by our hook adapter, decisions and call IDs
  environment.jsonl              # explicitly labelled fixture writer, conflict only
  operations.jsonl, operations/  # durable movement records
  backups/*.bin                  # original bytes for executed operations
  report.json                    # agent's structured report, not an external grade
  evaluation.json                # deterministic checks of current artifacts
  trial/                         # CLI route only
    cases.json, prompt.txt       # exact case version and actual request
    project-config.toml, project-hooks.json # exact reviewed project registration
    run.json                     # command, version, Skill/harness hashes, timestamps, exit, thread IDs, usage
    trace.jsonl, stderr.txt       # unmodified Codex CLI event stream and diagnostics
    final-message.md             # actual final response
    result.json                  # case/process/outcome checks and pending human rubric
  counterexamples/              # copied grader controls; created only when requested
  runs/<timestamp>/             # archived state plus files/Inbox and files/Organized
```

`hooks.jsonl` and `requests.jsonl` are written by our Python programs; Codex does
not generate those particular files automatically for every project. For two-chat Desktop rehearsals, retain the create-thread receipt and `read_thread` conversation snapshot as well as hook/service records. The CLI's
`trace.jsonl` is Codex's JSON event stream saved by our runner. It captures the
agent trial rather than just the file operations. Backups, hashes and logs are
cooperative local evidence, not tamper-proof records against the same OS user.

## Success criteria and limits

The deterministic grader compares byte-hash multisets, so two identical copies
must remain two copies. It independently checks content categories against the
fixture oracle; empty Inbox; unchanged references and concurrent file; supported
paths; byte backups; completed operations; and the report's operation IDs and
unresolved paths. With `--require-hooks`, each completed move needs a matching
allowed PreToolUse and observed PostToolUse for its arguments and tool-use ID.
Denied move arguments must not occur in service requests. The case runner also
requires a successful CLI process, completed turn, expected file/move counts and,
for conflict, an actual injected destination and denial.

Those are automatic checks, not a score for naming quality or final prose. Use
`cases.json`'s human rubric for Skill loading, meaningful names, plan-before-action,
uncoached recovery and honest explanation. Explicit invocation is covered here;
implicit triggering, negative trigger cases, held-out semantics, latency and
statistical reliability across repeated runs are not claimed.

### Narrow Finder metadata policy

The fixture seeds no `.DS_Store`. Grading excludes only newly observed regular
files whose basename is exactly `.DS_Store`, whose path is absent from baseline,
and whose hash is not an original baseline hash. Every excluded path/hash is
listed under `excluded_platform_metadata`. We never delete these files. The
scanner itself excludes nothing: baseline `.DS_Store` bytes and reference paths
remain protected; other unexpected files still fail preservation; symlinks and
special files still fail supported-path checks. Metadata renamed to a content
filename is not exempt. Folder layout and extended metadata preservation remain
outside the byte-preservation claim.

## Improve from failures and rerun the same cases

A failed check identifies the kind of change to consider; it does not automatically
mean the Skill prompt is wrong. Preserve the failing trace and outcome first.

| Evidence | Likely next step | Rerun |
| --- | --- | --- |
| Wrong-category copy preserves bytes but fails correctness | Inspect actual interpretation. If a real trial sorts only by extension, tighten the Skill's content-reading instruction. | Same normal and conflict cases, unchanged oracle |
| Conflict run stops after denial | Check trace for feedback. If agent does not re-inspect/replan, clarify that instruction in the Skill. | Same conflict case plus normal regression |
| Duplicate disappears | Check agent intent and service logs; reinforce keeping separate copies or repair the responsible tool defect. | Both cases and lost-duplicate grader control |
| Previously successful run fails only on new `.DS_Store` | Repair the grader's task boundary with the narrow, visible metadata policy above. | Metadata regression tests; valid and invalid controls |
| No hooks or runtime fails to initialize | Repair trust/config/runtime setup. | Same case after setup; do not weaken the pass criteria |

The original Sol CLI runs passed the initial Skill. A subsequent real Luna / Max
Desktop conflict run completed every move, preserved all files, and matched its
hooks, but listed all nine final files as unresolved. The unchanged grader failed
report_matches_execution. A narrow Skill clarification now defines that field as
exactly remaining Inbox items, Review items and unsupported paths; a preserved
concurrent destination belongs in interventions. Fresh normal and conflict chats
rerun the same seed and prompt. The failed run and before/after Skill hashes are
retained. This supplies an actual agent-Eval-driven instruction change.

The Finder false failure separately led to a grader correction. The copied
corrupt/no-op/duplicate/category cases demonstrate checker sensitivity; they do
not prove that an earlier Skill version made those mistakes. To compare
Skill versions, provision a new project/state from each version, retain the same
cases and seed, and compare automatic results plus the human rubric. Do not edit
the answers to fit the run.

This follows OpenAI's [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills):
define success, explicitly invoke, capture trace and artifacts, run deterministic
checks, add qualitative judgment, retain regressions and repeat. The official
[non-interactive guide](https://developers.openai.com/codex/noninteractive) documents
`codex exec --json`; our files supply the task-specific cases and checks.
