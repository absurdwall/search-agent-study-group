---
id: runner
term: Runner
aliases: ["ADK Runner", "agent runner"]
category: frameworks-and-protocols
status: published
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "callback"},
  {"type": "related", "target": "google-adk"},
  {"type": "uses", "target": "llm-agent"},
  {"type": "uses", "target": "session"}
]
sources: [
  {
    "title": "ADK Runtime Event Loop",
    "url": "https://adk.dev/runtime/event-loop/",
    "note": "Explains how Runner coordinates agents, callbacks, tools, events, sessions, and runtime services during an invocation."
  },
  {
    "title": "ADK Agent Team tutorial",
    "url": "https://adk.dev/tutorials/agent-team/",
    "note": "Shows Runner as the engine that accepts user input, invokes agent logic, manages session updates, and yields execution events."
  }
]
---

## Simple definition

The ADK runtime component that executes agents and coordinates sessions, tools, callbacks, and emitted events.

## Working definition

A Runner is ADK's entry point for processing user input through an agent application. It creates the invocation context, retrieves the appropriate Session through a service, invokes agent execution logic, coordinates callbacks and tools, persists resulting events and state changes, and yields events to the caller.

## Why it matters

Runner connects a static agent definition to a live application turn. It centralizes runtime concerns that would otherwise need custom orchestration code around every model and tool call.

## Example

An application passes a user ID, session ID, and new message to `runner.run_async(...)`, then consumes streamed events until it receives the final response.

## Common confusion

Runner is not the agent and does not supply the model's task instructions. The `LlmAgent` defines model-driven behavior; Runner executes that behavior within ADK's runtime and service environment.

## Study-group notes

Week 1 called Runner the component that wires agent, session, and I/O together. Its event stream also exposes tool calls and results without requiring access to private model reasoning.
