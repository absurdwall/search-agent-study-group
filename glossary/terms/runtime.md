---
id: runtime
term: Runtime
aliases: ["agent runtime", "execution runtime"]
category: frameworks-and-protocols
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "agentic-harness"}, {"type": "related", "target": "agentic-loop"}, {"type": "related", "target": "context-window"}, {"type": "related", "target": "runner"}, {"type": "uses", "target": "tool"}]
sources: [{"title": "Chapter 1 · Runtime", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/minimal-agentic-system/#beyond-minimal-loop", "note": "Current chapter treatment and teaching distinctions."}]
---

## Simple definition

The part of an agentic harness that coordinates an active run by invoking models, routing tool calls, carrying results forward, and stopping.

## Working definition

Runtime is this book's label for the software inside an agentic harness that coordinates an active run. It invokes the model, routes requested tools, carries observations into later calls, and determines whether execution continues or stops. Frameworks distribute these responsibilities differently and do not share one standardized Runtime interface.

## Why it matters

The runtime connects model output to actual execution. It is where a proposed tool call becomes a routed operation, where returned results become later context, and where framework-specific completion rules determine whether another model call is needed.

## Example

After a model requests `get_weather(location="Boston")`, the runtime routes the request, receives the tool result, adds that observation to the next model call, and returns the later answer when no required tool calls remain.

## Common confusion

Runtime does not mean the complete system around the model in this book; that broader system is the agentic harness. A Runner is a framework-specific entry point or object, and an event loop is one implementation pattern a runtime may use.

## Study-group notes

Chapter 1 explicitly treats runtime, Runner, event loop, and agentic harness as overlapping but non-identical terms.
