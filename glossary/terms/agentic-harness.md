---
id: agentic-harness
term: Agentic harness
aliases: ["harness engineering", "agent harness", "AI agent harness"]
category: agent-systems
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "agentic-loop"}, {"type": "related", "target": "context-window"}, {"type": "related", "target": "runtime"}, {"type": "uses", "target": "large-language-model"}, {"type": "uses", "target": "tool"}]
sources: [{"title": "Chapter 1 · Agentic harness", "url": "https://absurdwall.github.io/search-agent-study-group/book/minimal-agentic-system/#beyond-minimal-loop", "note": "Current chapter treatment and teaching distinctions."}]
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
