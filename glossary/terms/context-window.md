---
id: context-window
term: Context window
aliases: ["model context window", "context limit"]
category: foundations
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "large-language-model"},
  {"type": "related", "target": "prompt"},
  {"type": "related", "target": "session"},
  {"type": "related", "target": "skill"}
]
sources: [
  {
    "title": "Understand and count tokens",
    "url": "https://ai.google.dev/gemini-api/docs/tokens",
    "note": "Defines a model's context window as the token limit covering the input it can receive and the output it can generate."
  },
  {
    "title": "Long context",
    "url": "https://ai.google.dev/gemini-api/docs/long-context",
    "note": "Explains how finite context affects use cases, cost, latency, and strategies for providing relevant information."
  }
]
---

## Simple definition

The limited token space containing the input a model can consider and the output it can generate in one request.

## Working definition

The context window is the maximum token budget a model can process for one generation, typically accounting for the supplied input and generated output. Agent frameworks decide which instructions, messages, tool schemas, tool results, and retrieved material occupy that limited space.

## Why it matters

Context determines what information is available to the model at a given step. Larger or poorly managed context can increase cost and latency, exceed model limits, or bury relevant instructions among unnecessary material.

## Example

An agent includes its system prompt, recent conversation events, a product-search result, and the newest user message in the next request while omitting an unrelated old transcript.

## Common confusion

The context window is not durable memory. Information must be selected and placed into a model request each time; a session or memory service stores information outside the model and helps the application decide what to include.

## Study-group notes

Week 1 emphasized the engineering tradeoff: give the model everything it needs while keeping the request focused enough to control cost, latency, and distraction.
