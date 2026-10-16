---
id: system-prompt
term: System prompt
aliases: ["system instruction"]
category: foundations
status: published
last_reviewed: 2026-10-16
relations: [{"type": "broader", "target": "prompt"}, {"type": "related", "target": "guardrail"}]
sources: [{"title": "Chapter 3 · A prompt is only part of what the model receives", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/prompting-and-context/#useful-context", "note": "Places system guidance alongside the user request and other context."}]
---

## Simple definition

Developer-provided instructions that set a model's role, rules, and behavior for a request or conversation.

## Working definition

Instructions supplied by the application or platform to set the model’s role, behavior, and constraints. APIs can distinguish system and developer messages with different priorities; their names and precedence are product-specific.

## Why it matters

System prompts provide a consistent operating frame across many user messages. Clear instructions reduce ambiguity and improve behavior, but they remain model inputs rather than an unbreakable security boundary.

## Example

A shopping agent's system prompt says to use the catalog tool for product facts, never invent prices, request confirmation before purchases, and answer concisely.

## Common confusion

A system prompt can guide behavior but cannot guarantee policy enforcement or keep embedded secrets safe. High-impact constraints should also be enforced through permissions, validation, callbacks, and guardrails.

## Study-group notes

Chapters 1–3 place persistent instructions inside the assembled model context. Instructions guide behavior; enforcement belongs to the surrounding system.
