---
id: guardrail
term: Guardrail
aliases: ["agent guardrail", "safety guardrail", "action gate"]
category: control-and-quality
status: published
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "callback"},
  {"type": "related", "target": "llm-agent"},
  {"type": "related", "target": "tool"}
]
sources: [
  {
    "title": "A practical guide to building agents",
    "url": "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/",
    "note": "Describes layered model-based and rules-based guardrails for managing privacy, safety, relevance, and tool risk."
  },
  {
    "title": "Callbacks: Observe, Customize, and Control Agent Behavior",
    "url": "https://adk.dev/callbacks/",
    "note": "Shows how ADK callbacks can enforce safety rules, validate data, and prevent disallowed operations."
  }
]
---

## Simple definition

A check or control that keeps an agent's inputs, outputs, and actions within defined boundaries.

## Working definition

A guardrail is a policy-enforcing check or control applied to an agent's inputs, outputs, tool requests, state, or execution. Guardrails can use deterministic rules, model-based checks, permissions, approvals, or callback code to keep behavior within safety, policy, quality, and scope boundaries.

## Why it matters

Agents can follow variable paths and may affect external systems. Layered guardrails help reject unsafe requests, constrain risky actions, validate results, limit runaway behavior, and escalate work when automation should stop.

## Example

Before an order tool runs, a code-level guardrail verifies that the cart is valid, the user explicitly confirmed the purchase, and the proposed amount is within the agent's authorization limit.

## Common confusion

Prompt instructions alone are not strong enforcement, and guardrails do not replace authentication, authorization, least privilege, secure software design, or human oversight. They are one layer in a broader control system.

## Study-group notes

Week 1 used callbacks to implement guardrails. The callback is the lifecycle hook; the guardrail is the boundary or policy enforced through that hook.
