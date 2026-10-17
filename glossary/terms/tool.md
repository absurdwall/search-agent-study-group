---
id: tool
term: Tool
aliases: ["agent tool", "function tool"]
category: agent-systems
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "agent"}, {"type": "related", "target": "callback"}, {"type": "related", "target": "guardrail"}, {"type": "related", "target": "model-context-protocol"}]
sources: [{"title": "Chapter 1 · Tool", "url": "https://absurdwall.github.io/search-agent-study-group/book/minimal-agentic-system/#tools", "note": "Current chapter treatment and teaching distinctions."}]
---

## Simple definition

A defined capability an agent can request to retrieve information, perform an action, or delegate work.

## Working definition

A tool is a named, structured capability exposed to an agent. The model sees a description and input schema and can emit a structured request to use it; the framework validates that request, executes developer-defined logic, and returns the result to the agent.

## Why it matters

Tools connect model reasoning to current data and real effects. Clear names, descriptions, schemas, narrow permissions, predictable outputs, and useful errors strongly affect whether an agent behaves reliably and safely.

## Example

A `lookup_order(order_id)` tool accepts an order identifier and returns structured shipment status. The model chooses whether and how to request it, while application code performs the actual lookup.

## Common confusion

The LLM does not directly execute a Python function or API. It produces a request; the framework or application decides whether to allow the request, runs the tool, and adds the result to the next model context.

## Study-group notes

Chapter 1 uses this concept in its provider-neutral map of the minimal agentic system.
