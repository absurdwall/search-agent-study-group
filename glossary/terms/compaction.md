---
id: compaction
term: Compaction
aliases: ["context compaction", "conversation compaction"]
category: foundations
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "context"}, {"type": "related", "target": "context-window"}, {"type": "related", "target": "session"}]
sources: [{"title": "Chapter 1 · When the context window fills", "url": "https://absurdwall.github.io/search-agent-study-group/book/minimal-agentic-system/#context", "note": "Current chapter treatment and teaching distinctions."}]
---

## Simple definition

Replacing older conversation material with a shorter summary to make room in the context window.

## Working definition

Compaction is a context-management strategy that condenses accumulated history while trying to preserve important decisions and recent work. What is retained, cleared, or reloaded depends on the product.

## Why it matters

Long runs need room for new observations and output, but summaries can lose details needed later.

## Example

A coding assistant summarizes earlier investigation and keeps the latest failure and agreed constraints available for the next call.

## Common confusion

Compaction is lossy, not a perfect archive or model retraining. Persisting a file and loading it later is a separate mechanism.

## Study-group notes

Chapter 1 uses Claude Code as a concrete example; Chapter 3 discusses managing a session during iterative work.
