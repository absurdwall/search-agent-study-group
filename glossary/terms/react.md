---
id: react
term: ReAct
aliases: ["ReAct loop", "Reason + Act"]
category: agent-systems
status: published
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "agent"},
  {"type": "uses", "target": "large-language-model"},
  {"type": "related", "target": "llm-agent"},
  {"type": "uses", "target": "tool"}
]
sources: [
  {
    "title": "ReAct: Synergizing Reasoning and Acting in Language Models",
    "url": "https://arxiv.org/abs/2210.03629",
    "note": "Introduces the ReAct paradigm of interleaving reasoning traces with task-specific actions and observations."
  },
  {
    "title": "ReAct: Synergizing Reasoning and Acting in Language Models",
    "url": "https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/",
    "note": "Provides the Google Research explanation of how reasoning, actions, and environmental observations work together."
  }
]
---

## Simple definition

An agent pattern that interleaves reasoning, actions, and observations to choose successive steps.

## Working definition

ReAct is a model-and-tool interaction pattern in which an agent alternates between deciding what to do, taking an action, and using the resulting observation to inform the next step. The cycle continues until the agent reaches an answer or stopping condition.

## Why it matters

ReAct allows the path to adapt to information learned during execution. It is useful when the necessary tools or number of steps cannot be known reliably before the task begins.

## Example

An agent first searches for milk, observes product IDs and prices, selects the cheapest qualifying result, calls the cart tool, and then observes whether the cart update succeeded before responding.

## Common confusion

ReAct names an interaction pattern, not a requirement to expose private model reasoning to users or logs. Production implementations can preserve the action-and-observation loop while keeping internal reasoning private.

## Study-group notes

Week 1 visualized ReAct as Reason → Act → Observe → repeat, with tool results becoming new context for the next model call.
