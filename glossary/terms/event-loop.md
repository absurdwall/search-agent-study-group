---
id: event-loop
term: Event loop
aliases: ["agent runtime event loop", "execution event loop"]
category: frameworks-and-protocols
status: published
last_reviewed: 2026-07-27
relations: [
  {"type": "related", "target": "agentic-loop"},
  {"type": "related", "target": "runner"},
  {"type": "related", "target": "runtime"}
]
sources: [
  {
    "title": "Google ADK — Runtime event loop",
    "url": "https://adk.dev/runtime/event-loop/",
    "note": "Explains how ADK's Runner processes execution logic, events, state changes, tool activity, callbacks, and resumptions during an invocation."
  }
]
---

## Simple definition

A software mechanism that processes execution events, state changes, and resumptions during an active run.

## Working definition

An event loop is an implementation mechanism that a runtime may use to drive execution. It processes events and state changes, invokes the appropriate logic, and resumes work as model responses, tool calls, tool results, callbacks, or other execution events arrive.

## Why it matters

An event loop turns separate execution events into a continuing software process. It can help a runtime coordinate asynchronous operations, persist state changes, expose intermediate events, and resume a run after a tool or external system responds.

## Example

In Google ADK, a Runner begins an invocation and yields events as agent logic runs, tools are called, state changes are recorded, and execution continues or pauses.

## Common confusion

An event loop is not the same as an agentic loop. The agentic loop describes the conceptual model–tool–result cycle; an event loop is one software mechanism a runtime may use to implement and coordinate execution.

## Study-group notes

Chapter 1 distinguishes the conceptual agentic loop from the implementation-level event loop.
