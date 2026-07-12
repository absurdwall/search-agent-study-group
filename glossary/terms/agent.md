---
id: agent
term: Agent
aliases: ["AI agent", "LLM agent"]
category: agent-systems
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "uses", "target": "large-language-model"},
  {"type": "uses", "target": "react"},
  {"type": "uses", "target": "tool"},
  {"type": "narrower", "target": "llm-agent"},
  {"type": "narrower", "target": "sub-agent"}
]
sources: [
  {
    "title": "Building effective agents",
    "url": "https://www.anthropic.com/engineering/building-effective-agents",
    "note": "Supports the distinction between model-directed agents and systems that follow predefined code paths."
  },
  {
    "title": "A practical guide to building agents",
    "url": "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/",
    "note": "Describes agents as systems that independently complete tasks by managing workflow execution and selecting tools within guardrails."
  }
]
---

## Simple definition

An LLM-based system that uses tools in a loop, choosing what to do next until it reaches a goal.

## Working definition

An agent is a system in which a model dynamically directs how a goal is pursued. It interprets the current context, selects actions or tools, observes results, and repeats until it can answer, stop, correct course, or return control to a person.

## Why it matters

Agents are useful when a task's path cannot be completely specified in advance. That flexibility enables ambiguous, multi-step work, but it also increases cost, latency, variability, and the need for evaluation and guardrails.

## Example

Given “find organic milk under $4 and add the cheapest,” an agent searches the live catalog, compares the returned products, calls the cart tool with the selected item, and then reports the result.

## Common confusion

Adding an LLM to an application does not automatically make it an agent. The defining property in this glossary is model-directed execution: the model chooses the next step rather than only filling a fixed position in a predefined pipeline.

## Study-group notes

Week 1 shorthand: “Agent = LLM + Tools + Loop.” The formula is a useful architectural map, while the fuller definition emphasizes that the model controls the evolving path.
