---
id: prompt
term: Prompt
aliases: ["model prompt", "LLM prompt"]
category: foundations
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "context-window"},
  {"type": "related", "target": "large-language-model"},
  {"type": "narrower", "target": "system-prompt"}
]
sources: [
  {
    "title": "Introduction to prompting",
    "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design",
    "note": "Defines prompts as requests to a language model and describes instructions, context, examples, and system instructions as prompt components."
  },
  {
    "title": "Prompt design strategies",
    "url": "https://ai.google.dev/gemini-api/docs/prompting-strategies",
    "note": "Provides current guidance for structuring instructions and context to elicit useful model responses."
  }
]
---

## Simple definition

The instructions, context, examples, and input supplied to a model for one request.

## Working definition

A prompt is the information presented to a language model to shape one generation. Depending on the API and framework, it can include system instructions, user messages, conversation history, examples, retrieved context, tool results, and the current task.

## Why it matters

The model can only respond to the information and instructions available in its current request. Prompt content and structure therefore affect relevance, reliability, formatting, tool selection, cost, and how much room remains in the context window.

## Example

Before an agent answers “add the cheapest one,” its framework assembles system instructions, earlier product-search results, the prior assistant response, and the newest user message into the information sent to the model.

## Common confusion

A prompt is not necessarily just the sentence typed by the user. In an agent application, the user message is often one component of a larger request assembled by the framework.

## Study-group notes

Week 1 treated the prompt as “everything the LLM sees for this call,” while noting that APIs may transmit some components, such as tool schemas, in separate structured fields.
