---
id: agentic-loop
term: Agentic loop
aliases: ["agent loop", "model-tool loop"]
category: agent-systems
status: published
last_reviewed: 2026-07-27
relations: [
  {"type": "related", "target": "context-window"},
  {"type": "related", "target": "react"},
  {"type": "related", "target": "runtime"},
  {"type": "uses", "target": "large-language-model"},
  {"type": "uses", "target": "tool"}
]
sources: [
  {
    "title": "Claude Code Glossary — Agentic loop",
    "url": "https://code.claude.com/docs/en/glossary#agentic-loop",
    "note": "Defines Claude Code's product-specific loop as gathering context, taking action, verifying results, and repeating until done."
  },
  {
    "title": "Claude Agent SDK — How the agent loop works",
    "url": "https://code.claude.com/docs/en/agent-sdk/agent-loop",
    "note": "Shows model evaluation, tool execution, returned results, repetition, and the final-answer exit."
  },
  {
    "title": "OpenAI Agents SDK — Running agents",
    "url": "https://openai.github.io/openai-agents-python/running_agents/",
    "note": "Documents a framework loop that invokes a model, executes tool calls, appends results, and stops at configured final output."
  }
]
---

## Simple definition

The recurring cycle in which a model produces output, tools may run, results return as context, and the system repeats until it stops.

## Working definition

An agentic loop is the conceptual model–tool–result cycle that lets a system adapt across multiple model calls. The model produces text, a proposed tool call, or both; surrounding software executes or routes requested tools, supplies their results to a later call, and continues until a stopping condition is satisfied.

## Why it matters

The loop turns a one-shot model call into an adaptive process. Each new observation can change the model's next action, allowing the system to gather information, act, check results, recover from errors, and decide when to return.

## Example

A weather agent receives a location, requests a weather tool, receives the current conditions in a later call, and then produces a final answer without requesting another tool.

## Common confusion

An agentic loop is not the same as an event loop or ReAct. It describes the conceptual alternation among model output, actions, and observations; software may implement that cycle in different ways, and it does not require explicit reasoning traces.

## Study-group notes

Chapter 1 uses `LLM + tools + agentic loop` as its minimal three-part teaching map.
