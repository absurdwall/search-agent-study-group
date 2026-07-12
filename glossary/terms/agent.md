---
id: agent
term: Agent
aliases: ["AI agent", "LLM agent"]
category: agent-systems
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "uses", "target": "augmented-llm"},
  {"type": "uses", "target": "tool"},
  {"type": "contrasts_with", "target": "workflow"},
  {"type": "evaluated_by", "target": "agent-evaluation"}
]
sources: [
  {
    "title": "Building effective agents",
    "url": "https://www.anthropic.com/engineering/building-effective-agents",
    "note": "Supports the distinction between model-directed agents and systems that follow predefined workflow paths."
  },
  {
    "title": "A practical guide to building agents",
    "url": "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/",
    "note": "Describes agents as systems that independently complete tasks by managing workflow execution and selecting tools within guardrails."
  }
]
---

## Simple definition

A system that lets a model choose the next steps and tools needed to reach a goal.

## Working definition

An agent is a system that uses a model to direct how it pursues a goal, choosing actions and tools as the task unfolds and stopping, correcting, or handing back control when appropriate.

## Why it matters

Agent design is useful when the path cannot be fully specified in advance. That flexibility can solve ambiguous, multi-step tasks, but it also increases cost, latency, and the need for evaluation and safeguards.

## Example

Given “investigate why this order is late,” an agent decides which order and carrier tools to call, interprets the results, asks for missing information if needed, and produces a supported answer.

## Common confusion

“Agent” is used broadly across the field. In this glossary, the key test is who controls the path: predefined code indicates a workflow; model-directed action selection indicates an agent.

## Study-group notes

This definition intentionally combines Anthropic's architectural distinction with OpenAI's task-completion framing.
