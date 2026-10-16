---
id: tool-call
term: Tool call
aliases: ["function call", "tool request"]
category: agent-systems
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "tool"}, {"type": "related", "target": "agentic-loop"}, {"type": "related", "target": "runtime"}]
sources: [{"title": "Chapter 1 · Tools", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/minimal-agentic-system/#tools", "note": "Current chapter treatment and teaching distinctions."}]
---

## Simple definition

A structured model request to use a named tool with specific arguments.

## Working definition

A tool call identifies an operation and its inputs. The application or runtime routes the request; tool code or a hosted service executes it and returns a result, which may be data, status, or an error.

## Why it matters

This boundary separates a proposed action from an executed one and explains how new evidence enters the next model call.

## Example

The model requests search_files(query="parser"); software runs the search and returns matching file paths.

## Common confusion

A tool definition describes a capability; a tool call requests one use; a tool result reports what happened. Producing the call does not perform the operation.

## Study-group notes

Chapter 1 follows the complete definition → call → execution → result round trip.
