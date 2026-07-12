---
id: guardrail
term: Guardrail
aliases: ["agent guardrail", "safety guardrail"]
category: control-and-quality
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "callback"},
  {"type": "related", "target": "tool"},
  {"type": "evaluated_by", "target": "agent-evaluation"}
]
sources: [
  {
    "title": "A practical guide to building agents",
    "url": "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/",
    "note": "Describes layered model-based and rules-based guardrails for managing privacy, safety, relevance, and tool risk."
  }
]
---

## Simple definition

A check or control that keeps an agent within defined boundaries.

## Working definition

A guardrail is a check or control that constrains an agent's inputs, outputs, tool use, or execution so the system stays within defined safety, policy, quality, or scope boundaries.

## Why it matters

Agents can take variable paths and may affect external systems. Layered guardrails help detect unsafe requests, limit risky actions, validate outputs, and escalate to people when automation should stop.

## Example

Before a message is sent, one guardrail removes unnecessary personal data, another verifies the recipient, and a high-impact action requires explicit approval.

## Common confusion

Guardrails are not a substitute for authentication, authorization, least privilege, secure software design, or human oversight. They are one layer in a broader defense.

## Study-group notes
