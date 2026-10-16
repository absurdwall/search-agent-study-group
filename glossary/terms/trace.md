---
id: trace
term: Trace
aliases: ["execution trace", "agent trace"]
category: control-and-quality
sources: [{"title": "Chapter 5: Inspect the trace and the artifacts", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#eval-workflow", "note": "Defines the term and its role in the chapter’s examples."}, {"title": "Chapter 5: Read a documented command-start event", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#eval-trace-example", "note": "Explains why an item.started event with in_progress status is evidence of a start, not success."}]
relations: [{"type": "related", "target": "trial"}, {"type": "related", "target": "artifact"}, {"type": "related", "target": "grader"}, {"type": "related", "target": "runtime"}, {"type": "related", "target": "evaluation"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

A captured record of execution events, such as model responses, tool calls, and tool results.

## Working definition

A trace records the events and data an instrumented runtime captures during a run. It can show attempted operations, returned results, and reported statuses, but its coverage is limited by the capture system. Inspect completion events and independent outcome evidence rather than relying on an action’s appearance in the record.

## Why it matters

Traces help locate where an agent diverged from the intended process and distinguish a missing tool, rejected operation, failed command, or misleading final report.

## Example

A saved command-start event says a build is in progress. Find the corresponding completion result and inspect the produced app before grading the build as successful.

## Common confusion

A trace is not proof of external reality and does not reveal all hidden reasoning. A booking claim in a trace does not establish that a reservation exists; missing data remains unknown.

## Study-group notes

Chapter 5 captures Codex events as JSONL and compares them with files and final state. Keep claims, recorded events, and independently verified outcomes distinct.
