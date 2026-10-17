---
id: agent
term: Agent
aliases: ["AI agent", "LLM agent"]
category: agent-systems
status: published
last_reviewed: 2026-10-16
relations: [{"type": "narrower", "target": "sub-agent"}, {"type": "uses", "target": "large-language-model"}, {"type": "uses", "target": "react"}, {"type": "uses", "target": "tool"}]
sources: [{"title": "Chapter 1 · Agent", "url": "https://absurdwall.github.io/search-agent-study-group/book/minimal-agentic-system/#agentic-loop", "note": "Current chapter treatment and teaching distinctions."}]
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

Chapter 1 uses this concept in its provider-neutral map of the minimal agentic system.
