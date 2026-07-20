---
id: callback
term: Callback
aliases: ["lifecycle callback", "agent callback", "hook"]
category: control-and-quality
status: published
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "guardrail"},
  {"type": "related", "target": "llm-agent"},
  {"type": "related", "target": "runner"},
  {"type": "related", "target": "tool"}
]
sources: [
  {
    "title": "Callbacks: Observe, Customize, and Control Agent Behavior",
    "url": "https://adk.dev/callbacks/",
    "note": "Documents callbacks as functions invoked at predefined points before or after agent, model, and tool execution."
  },
  {
    "title": "ADK Technical Overview",
    "url": "https://adk.dev/get-started/about/",
    "note": "Summarizes callbacks as custom code for checks, logging, and behavior modification at specific process points."
  }
]
---

## Simple definition

Code ADK runs at a defined point in the agent process to observe, modify, block, or replace behavior.

## Working definition

A callback is developer-supplied code registered at a defined point in an ADK agent's lifecycle, such as before or after agent, model, or tool execution. Depending on the hook, it can inspect data, record events, modify requests or results, block an action, or short-circuit a step.

## Why it matters

Callbacks provide controlled intervention points without rewriting the core agent loop. They support tracing, policy enforcement, approvals, caching, state updates, request adaptation, and performance optimizations.

## Example

A `before_tool` callback checks a proposed `place_order` call. If the session lacks explicit customer confirmation, it returns a blocked result and the purchasing function never runs.

## Common confusion

A callback is a mechanism, not automatically a safety policy. The same hook system can implement a guardrail, collect metrics, alter a request, or skip unnecessary model work.

## Study-group notes

Week 1 demonstrated three callback patterns: a tool-round limit, an action gate, and a short-circuit that avoids an extra model call after a tool has already built the response.
