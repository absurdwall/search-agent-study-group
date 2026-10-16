---
id: session
term: Session
aliases: ["conversation session"]
category: frameworks-and-protocols
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "context-window"}, {"type": "related", "target": "runner"}]
sources: [{"title": "Chapter 1 · Context", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/minimal-agentic-system/#context", "note": "Distinguishes records stored by the application from model-visible information."}]
---

## Simple definition

A stored record of an interaction that the system can use to continue work across model calls.

## Working definition

A session tracks an ongoing interaction, often including messages, execution events, and application state. The runtime selects relevant parts for each model call; what is persisted and how it is resumed depends on the product.

## Why it matters

The model itself does not retain application history between calls. Sessions give the runtime a durable record from which it can reconstruct relevant context, continue a conversation, and track state changes.

## Example

A resumed coding session supplies relevant earlier decisions and recent tool results without placing every stored event in the next context window.

## Common confusion

A session record is not the active context window or cross-session memory. Ending a turn also need not end the session.

## Study-group notes

Chapter 1 distinguishes stored history from selected context; Chapter 3 discusses fresh sessions, compaction, and resuming work. Chapter 2’s full memory treatment is still planned.
