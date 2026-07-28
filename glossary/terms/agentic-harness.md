---
id: agentic-harness
term: Agentic harness
aliases: ["agent harness", "AI agent harness"]
category: agent-systems
status: published
last_reviewed: 2026-07-27
relations: [
  {"type": "related", "target": "agentic-loop"},
  {"type": "related", "target": "context-window"},
  {"type": "related", "target": "runtime"},
  {"type": "uses", "target": "large-language-model"},
  {"type": "uses", "target": "tool"}
]
sources: [
  {
    "title": "Claude Code Glossary — Agentic harness",
    "url": "https://code.claude.com/docs/en/glossary#agentic-harness",
    "note": "Defines the Claude Code harness as the tools, context management, and execution environment around the model."
  },
  {
    "title": "Claude Code — How Claude Code works",
    "url": "https://code.claude.com/docs/en/how-claude-code-works",
    "note": "Explains how Claude Code surrounds the Claude model with tools, context handling, and a recurring agentic loop."
  }
]
---

## Simple definition

The complete system around a model that supplies tools, manages context, provides an execution environment, and keeps work moving.

## Working definition

An agentic harness is this book's term for the complete surrounding system that turns a language model into a usable agent. It can include tools, context assembly, the execution environment, persistence, permissions, and the machinery that invokes the model and keeps a run moving. Claude Code uses the same term for the product surrounding the Claude model.

## Why it matters

Separating the harness from the model makes responsibility visible. Model output can propose an action, but the harness decides what capabilities are available, supplies relevant information, executes or routes operations, carries results forward, and manages the larger run.

## Example

In a coding agent, the harness may expose file and shell tools, load project instructions, invoke the model, execute approved commands, return command output, and keep the task running until it stops.

## Common confusion

The harness is not the model, and it is broader than the runtime. In this book, runtime names the active execution-coordination layer inside the complete harness. Other products may divide or name these responsibilities differently.

## Study-group notes

Chapter 1 uses agentic harness as a teaching convention and notes that Claude Code independently uses the same product term.
