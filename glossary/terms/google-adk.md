---
id: google-adk
term: Google Agent Development Kit (ADK)
aliases: ["Google ADK", "ADK", "Agent Development Kit"]
category: frameworks-and-protocols
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "llm-agent"},
  {"type": "related", "target": "model-context-protocol"},
  {"type": "related", "target": "runner"},
  {"type": "related", "target": "session"}
]
sources: [
  {
    "title": "Agent Development Kit Technical Overview",
    "url": "https://adk.dev/get-started/about/",
    "note": "Describes ADK's core concepts and its support for building, managing, evaluating, and deploying agent applications."
  }
]
---

## Simple definition

Google's open-source framework for building, running, evaluating, and deploying agent systems.

## Working definition

Google Agent Development Kit is a model-agnostic development framework for agent applications. It provides agent types, tools, callbacks, sessions, runtime services, evaluation support, deployment integrations, and orchestration patterns across supported programming languages.

## Why it matters

An agent framework supplies the execution machinery around a model: tool dispatch, events, session persistence, callbacks, streaming, and composition. This lets developers focus on agent behavior without rebuilding the entire runtime loop.

## Example

A developer defines an `LlmAgent` with instructions and catalog tools, creates a `SessionService`, and uses a `Runner` to process user messages and stream execution events.

## Common confusion

ADK is not an LLM and is not limited to Gemini or Python. It coordinates supported models and agent components; model capabilities, external services, and application code remain separate dependencies.

## Study-group notes

Week 1 summarized ADK as `LlmAgent + Tool + Session + Runner + Callbacks`, with the framework owning the execution loop and plumbing.
