---
id: llm-agent
term: LlmAgent
aliases: ["ADK Agent", "model-driven agent"]
category: frameworks-and-protocols
status: published
last_reviewed: 2026-07-12
relations: [
  {"type": "broader", "target": "agent"},
  {"type": "uses", "target": "callback"},
  {"type": "uses", "target": "react"},
  {"type": "uses", "target": "system-prompt"},
  {"type": "uses", "target": "tool"}
]
sources: [
  {
    "title": "Simple agents with LlmAgent",
    "url": "https://adk.dev/agents/llm-agents/",
    "note": "Documents LlmAgent as ADK's model-driven agent class and explains how instructions, models, and tools shape its behavior."
  },
  {
    "title": "Agent Development Kit Technical Overview",
    "url": "https://adk.dev/get-started/about/",
    "note": "Places LlmAgent within ADK's broader set of agent, runtime, tool, callback, and session primitives."
  }
]
---

## Simple definition

ADK's model-driven agent type, combining a generative model with instructions, tools, and execution behavior.

## Working definition

`LlmAgent` is ADK's core non-deterministic agent class. A developer gives it an identity, model, instructions, tools, callbacks, and optional composition settings; during execution, the model interprets context and dynamically decides what output or tool request to produce.

## Why it matters

`LlmAgent` is the point where the general idea of an agent becomes a concrete ADK component. Understanding its configuration clarifies which concerns belong to the model, the agent definition, and the runtime.

## Example

A shopping `LlmAgent` uses a selected model, a system instruction describing its job, product and cart tools, and a `before_tool` callback that blocks unconfirmed purchases.

## Common confusion

`LlmAgent` defines model-driven behavior but does not execute by itself. A Runner and supporting services provide invocation, session handling, event persistence, and interaction with the surrounding application.

## Study-group notes

Week 1 called `LlmAgent` the orchestrator that wraps a model with instructions, tools, and callbacks. More precisely, it defines the model-driven execution logic that ADK's runtime invokes.
