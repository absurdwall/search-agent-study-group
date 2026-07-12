---
id: system-prompt
term: System prompt
aliases: ["system instruction", "developer instruction"]
category: foundations
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "broader", "target": "prompt"},
  {"type": "related", "target": "guardrail"},
  {"type": "related", "target": "llm-agent"}
]
sources: [
  {
    "title": "System instructions",
    "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/system-instruction-introduction",
    "note": "Explains system instructions as developer-provided guidance for model role, goals, rules, context, style, and output format."
  },
  {
    "title": "Simple agents with LlmAgent",
    "url": "https://adk.dev/agents/llm-agents/",
    "note": "Documents the ADK instruction field used to guide an LlmAgent's identity, behavior, and tool use."
  }
]
---

## Simple definition

Developer-provided instructions that set a model's role, rules, and behavior for a request or conversation.

## Working definition

A system prompt, also called a system instruction in some APIs, is higher-priority developer guidance supplied alongside user input. It commonly defines the agent's purpose, behavioral rules, tool-routing guidance, tone, constraints, and expected output format.

## Why it matters

System prompts provide a consistent operating frame across many user messages. Clear instructions reduce ambiguity and improve behavior, but they remain model inputs rather than an unbreakable security boundary.

## Example

A shopping agent's system prompt says to use the catalog tool for product facts, never invent prices, request confirmation before purchases, and answer concisely.

## Common confusion

A system prompt can guide behavior but cannot guarantee policy enforcement or keep embedded secrets safe. High-impact constraints should also be enforced through permissions, validation, callbacks, and guardrails.

## Study-group notes

Week 1 described the system prompt as the agent's job description: identity, hard rules, behavioral guidelines, routing logic, and output expectations.
