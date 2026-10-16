---
id: lifecycle-event
term: Lifecycle event
aliases: ["hook event", "agent lifecycle event"]
category: control-and-quality
sources: [{"title": "Chapter 5: Where hooks fit in the lifecycle", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#hook-events", "note": "Defines the term and its role in the chapter’s examples."}]
relations: [{"type": "related", "target": "hook"}, {"type": "related", "target": "runtime"}, {"type": "related", "target": "session"}, {"type": "related", "target": "tool"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

A named moment in an agent run, such as session start, a pending tool call, or completion of a turn.

## Working definition

A lifecycle event is a runtime-defined occurrence to which a hook can be attached. Events can surround prompts, tool calls, permission requests, context compression, delegated work, or completion. The specific product defines when an event fires, what data it supplies, and which decisions a handler may return.

## Why it matters

Choosing the right moment determines whether code can prevent an action, react to an effect, or check that work is complete.

## Example

A pre-tool event can inspect a pending file edit before it executes. A post-tool event can inspect or format the resulting file after execution.

## Common confusion

Finishing a turn is different from ending a session. Similar event names in two products do not guarantee identical timing, inputs, or authority.

## Study-group notes

Choose the lifecycle stage before copying an event name. Chapter 5 distinguishes session start, pre-tool, post-tool, stop, interrupt, and session-end behavior.
