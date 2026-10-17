---
id: prompt
term: Prompt
aliases: ["user prompt", "prompting"]
category: foundations
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "context"}, {"type": "related", "target": "system-prompt"}]
sources: [{"title": "Chapter 3 · Start with the result", "url": "https://absurdwall.github.io/search-agent-study-group/book/prompting-and-context/#result-first", "note": "Current chapter treatment and teaching distinctions."}]
---

## Simple definition

A question, instruction, or goal that asks the model or agent for a result.

## Working definition

In this book’s practical prompting chapter, a prompt states what is wanted in the current interaction. Useful details can include the goal, context, intended output, and boundaries; include only the components that change the work.

## Why it matters

An observable result and a meaningful check give the agent clearer direction than a long list of prescribed steps.

## Example

“Draft a one-page project update for leadership from this plan, flag unknowns, and do not publish it.”

## Common confusion

Prompt is sometimes used broadly for all model input. Here the current request is distinguished from the wider assembled context, including system guidance, tools, history, and retrieved material.

## Study-group notes

Chapter 3 replaces the old Week 1 shorthand “everything the model sees” with a practical request-versus-context distinction.
