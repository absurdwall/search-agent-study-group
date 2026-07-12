---
id: session
term: Session
aliases: ["ADK session", "conversation session"]
category: frameworks-and-protocols
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "context-window"},
  {"type": "related", "target": "llm-agent"},
  {"type": "related", "target": "runner"}
]
sources: [
  {
    "title": "Conversational Context: Session, State, and Memory",
    "url": "https://adk.dev/sessions/",
    "note": "Defines Session as one conversation thread containing an event history and temporary State, distinct from cross-session Memory."
  },
  {
    "title": "Session: Tracking Individual Conversations",
    "url": "https://adk.dev/sessions/session/",
    "note": "Documents session lifecycle, SessionService responsibilities, persistence options, events, and state updates."
  }
]
---

## Simple definition

ADK's record of one conversation thread, including its event history and temporary state.

## Working definition

A Session represents one ongoing interaction between a user and an ADK application. It contains the chronological events produced during that conversation and a State dictionary for temporary conversation-specific data; a SessionService manages its lifecycle and persistence.

## Why it matters

The model itself does not retain application history between calls. Sessions give the runtime a durable record from which it can reconstruct relevant context, continue a conversation, and track state changes.

## Example

A shopping session stores events for the original product search and the agent's response, plus temporary state such as an explicit purchase-confirmation flag used by a later callback.

## Common confusion

Session, State, context window, and Memory are different. The Session is the conversation record, State is temporary structured data inside it, the context window is what reaches a model call, and Memory supports information beyond one session.

## Study-group notes

Week 1 described Session as the agent's memory across turns. The precise ADK view is a stored conversation thread whose events and state allow the runtime to assemble later context.
