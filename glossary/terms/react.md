---
id: react
term: ReAct
aliases: ["ReAct loop", "Reason + Act"]
category: agent-systems
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "agent"}, {"type": "uses", "target": "large-language-model"}, {"type": "uses", "target": "tool"}]
sources: [{"title": "Chapter 1 · ReAct", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/minimal-agentic-system/#beyond-minimal-loop", "note": "Current chapter treatment and teaching distinctions."}]
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

Chapter 1 uses this concept in its provider-neutral map of the minimal agentic system.
