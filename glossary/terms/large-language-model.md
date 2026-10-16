---
id: large-language-model
term: Large language model (LLM)
aliases: ["LLM", "language model"]
category: foundations
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "context-window"}, {"type": "related", "target": "prompt"}]
sources: [{"title": "Chapter 1 · Large language model (LLM)", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/minimal-agentic-system/#llm", "note": "Current chapter treatment and teaching distinctions."}]
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

Chapter 1 uses this concept in its provider-neutral map of the minimal agentic system.
