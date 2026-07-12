---
id: callback
term: Callback
aliases: ["lifecycle callback", "agent callback"]
category: control-and-quality
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "guardrail"},
  {"type": "related", "target": "tool"},
  {"type": "related", "target": "agent-evaluation"}
]
sources: [
  {
    "title": "Callbacks: Observe, Customize, and Control Agent Behavior",
    "url": "https://adk.dev/callbacks/",
    "note": "Documents callbacks as hooks before or after agent, model, and tool execution for observation and behavior control."
  },
  {
    "title": "ADK Technical Overview",
    "url": "https://adk.dev/get-started/about/",
    "note": "Summarizes callbacks as custom code that runs at specific process points for checks, logging, or modifications."
  }
]
---

## Simple definition

Code that runs automatically at a specific point in an agent's process.

## Working definition

A callback is developer-supplied code that runs at a defined point in an agent's lifecycle, such as before or after an agent, model, or tool executes. It can observe, log, modify, block, or replace behavior at that point.

## Why it matters

Callbacks provide controlled intervention points without rewriting the core agent loop. They are useful for tracing, policy checks, caching, approvals, and adapting requests or results.

## Example

A `before_tool` callback inspects a proposed refund amount and requires human approval before the refund tool runs above a threshold.

## Common confusion

A callback is a mechanism, not a policy. A guardrail can be implemented with a callback, but callbacks can also perform neutral tasks such as logging or metrics collection.

## Study-group notes

The exact callback names and whether they can replace execution are framework-specific; the lifecycle-hook idea is broader.
