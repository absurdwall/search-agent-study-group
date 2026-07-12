---
id: large-language-model
term: Large language model (LLM)
aliases: ["LLM", "language model"]
category: foundations
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "context-window"},
  {"type": "related", "target": "prompt"}
]
sources: [
  {
    "title": "A practical guide to building agents",
    "url": "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/",
    "note": "Identifies the model as the component that supplies an agent's reasoning and decision-making rather than the whole agent system."
  },
  {
    "title": "Understand and count tokens",
    "url": "https://ai.google.dev/gemini-api/docs/tokens",
    "note": "Explains token-based model inputs and outputs and the finite context window within which a model processes them."
  }
]
---

## Simple definition

A model that takes a token sequence as input and generates output; it has no persistent session memory, tools, or agent loop by itself.

## Working definition

A large language model is a model trained on large collections of language data to generate output from the context supplied to a model call. In an agent system, the LLM interprets instructions, evaluates the available context, and produces text or structured requests, but surrounding software supplies persistence, tool execution, and the repeated execution loop.

## Why it matters

Separating the model from the system around it makes agent architecture easier to understand. Model quality affects reasoning and generation, while the framework determines what context is supplied, which capabilities are available, and what happens after each output.

## Example

Given a customer question and relevant policy text, an LLM can draft an answer. To verify a live order, an agent framework must expose an order tool, execute the requested call, and return the result to the model in a later step.

## Common confusion

An LLM and an agent are not synonyms. A hosted model API may offer convenient features, but the model itself does not maintain an application's durable session history or execute arbitrary business functions.

## Study-group notes

Week 1 shorthand: `f(token_sequence) → output`. “No memory, tools, or loop” describes the bare model call; those capabilities come from the surrounding application or framework.
