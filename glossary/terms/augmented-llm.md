---
id: augmented-llm
term: Augmented LLM
aliases: ["tool-augmented LLM", "LLM with retrieval, tools, and memory"]
category: foundations
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "large-language-model"},
  {"type": "uses", "target": "tool"},
  {"type": "related", "target": "agent"}
]
sources: [
  {
    "title": "Building effective agents",
    "url": "https://www.anthropic.com/engineering/building-effective-agents",
    "note": "Defines the augmented LLM as an LLM enhanced with capabilities such as retrieval, tools, and memory."
  }
]
---

## Simple definition

An LLM connected to extra capabilities such as retrieval, tools, or memory.

## Working definition

An augmented LLM is an LLM connected to added capabilities such as retrieval, tools, and memory. The model can use those capabilities to obtain context or act beyond what a single prompt-and-response call can do.

## Why it matters

It is a useful building block between a bare model call and a larger agentic system. Many valuable applications need augmentation without needing an autonomous agent loop.

## Example

A support assistant retrieves the relevant help article, checks an account through a read-only tool, and uses the returned context to answer a question.

## Common confusion

Adding a tool does not automatically make a system an agent. The surrounding code may still decide every step, which is closer to a predefined workflow.

## Study-group notes

Anthropic uses this term as a foundational building block; other sources may describe the same idea without giving it a separate name.
