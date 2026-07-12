---
id: tool
term: Tool
aliases: ["agent tool", "function tool"]
category: agent-systems
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "augmented-llm"},
  {"type": "related", "target": "agent"},
  {"type": "related", "target": "guardrail"}
]
sources: [
  {
    "title": "Custom Tools for ADK",
    "url": "https://adk.dev/tools-custom/",
    "note": "Defines a tool as a specific, structured capability that lets an agent act or interact beyond text generation."
  },
  {
    "title": "A practical guide to building agents",
    "url": "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/",
    "note": "Distinguishes data, action, and orchestration tools and explains how tools extend an agent through external systems."
  }
]
---

## Simple definition

A defined capability an agent can call to get information or take an action.

## Working definition

A tool is a named, structured capability an agent or augmented LLM can invoke to retrieve information, perform a defined action, or delegate work. Its interface tells the model what the capability does and what inputs it accepts.

## Why it matters

Tools connect model reasoning to current data and real effects. Clear descriptions, narrow permissions, predictable outputs, and good error handling strongly affect agent performance and safety.

## Example

A `lookup_order(order_id)` tool accepts an order identifier and returns structured shipment status. The model chooses whether and how to call it; the tool executes developer-defined logic.

## Common confusion

The tool does not usually reason independently. It performs its defined operation; the model or orchestration layer decides when to invoke it and what to do with the result.

## Study-group notes
