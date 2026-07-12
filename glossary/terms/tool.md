---
id: tool
term: Tool
aliases: ["agent tool", "function tool"]
category: agent-systems
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "agent"},
  {"type": "related", "target": "callback"},
  {"type": "related", "target": "guardrail"},
  {"type": "related", "target": "model-context-protocol"}
]
sources: [
  {
    "title": "Custom Tools for ADK",
    "url": "https://adk.dev/tools-custom/",
    "note": "Defines a tool as a specific capability that lets an agent perform developer-defined actions beyond text generation."
  },
  {
    "title": "A practical guide to building agents",
    "url": "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/",
    "note": "Distinguishes data, action, and orchestration tools and explains how tools extend an agent through external systems."
  }
]
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

Week 1 emphasized the full protocol: schema shown to the model → structured tool request → framework execution → result returned as a new observation.
