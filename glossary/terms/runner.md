---
id: runner
term: Runner
aliases: ["agent runner", "ADK Runner"]
category: frameworks-and-protocols
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "runtime"}, {"type": "related", "target": "agentic-harness"}, {"type": "related", "target": "event-loop"}]
sources: [{"title": "Chapter 1 · Harness, runtime, Runner, and event loop", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/minimal-agentic-system/#beyond-minimal-loop", "note": "Current chapter treatment and teaching distinctions."}]
---

## Simple definition

A framework-specific object or entry point that starts and drives an agent run.

## Working definition

A Runner provides an application interface for executing an agent. Its exact duties vary: it may invoke models, route tools, process events, manage session updates, and return final output.

## Why it matters

It connects an agent definition to live execution while exposing the framework’s particular control and state model.

## Example

Application code starts a run through a Runner and consumes its returned result or streamed events.

## Common confusion

Runner is not a universal synonym for runtime, harness, or agentic loop. Those terms describe different scopes, and frameworks divide responsibilities differently.

## Study-group notes

Chapter 1 compares OpenAI Agents SDK and Google ADK without treating either implementation as the universal definition.
