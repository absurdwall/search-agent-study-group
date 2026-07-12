---
id: large-language-model
term: Large language model (LLM)
aliases: ["LLM", "language model"]
category: foundations
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "augmented-llm"},
  {"type": "related", "target": "tool"}
]
sources: [
  {
    "title": "A practical guide to building agents",
    "url": "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/",
    "note": "Identifies the model as the component that supplies an agent's reasoning and decision-making."
  }
]
---

## Simple definition

A model that reads language input and generates language output.

## Working definition

A large language model is a model trained on large collections of language data to interpret prompts and generate likely continuations. In an agent system, the LLM is usually the reasoning and decision-making component, not the whole agent.

## Why it matters

The model shapes what the system can understand and generate, but reliability also depends on instructions, context, tools, orchestration, and checks around it.

## Example

Given a customer question and relevant policy text, an LLM can draft an answer. By itself, it cannot verify a live order status unless the surrounding system supplies that information or a tool.

## Common confusion

An LLM and an agent are not synonyms. An LLM produces model outputs; an agent combines a model with a process for pursuing a goal, often including tools and guardrails.

## Study-group notes
