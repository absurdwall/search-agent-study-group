---
id: context
term: Context
aliases: ["model context", "working context"]
category: foundations
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "context-window"}, {"type": "related", "target": "prompt"}, {"type": "related", "target": "agentic-harness"}]
sources: [{"title": "Chapter 1 · Context", "url": "https://absurdwall.github.io/search-agent-study-group/book/minimal-agentic-system/#context", "note": "Current chapter treatment and teaching distinctions."}]
---

## Simple definition

The information available to the model while it produces the current output.

## Working definition

Context is the model-visible material supplied for a call: instructions, the current request, selected history, tool definitions, observations, and retrieved references. The harness chooses what is included.

## Why it matters

A fact stored by the application cannot guide the current response unless the model receives it. Selecting useful context matters as much as storing information.

## Example

After a file-search tool returns matching paths, those paths enter the next call as context and can change the next action.

## Common confusion

Context is the information; the context window is its finite capacity. Neither is the complete session record or permanent memory.

## Study-group notes

Chapters 1 and 3 distinguish assembled context from the current prompt and from information stored elsewhere.
