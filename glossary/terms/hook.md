---
id: hook
term: Hook
aliases: ["agent hook", "lifecycle hook"]
category: control-and-quality
sources: [{"title": "Chapter 5: Hooks", "url": "https://absurdwall.github.io/search-agent-study-group/book/guardrails-hooks-and-evals/#hooks", "note": "Defines the term and its role in the chapter’s examples."}]
relations: [{"type": "related", "target": "lifecycle-event"}, {"type": "related", "target": "callback"}, {"type": "related", "target": "runtime"}, {"type": "related", "target": "guardrail"}, {"type": "related", "target": "evaluation"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

A way to run registered code when the agent system reaches a defined event.

## Working definition

A hook connects a supported runtime event to code supplied by a developer. Its event specifies when to run, an optional matcher selects occurrences, and its handler performs the work. The handler may receive event data and return information or a supported decision to the runtime.

## Why it matters

Hooks make jobs such as notifications, formatting, context reminders, and pre-action checks happen at supported moments without relying on the model to remember to request them.

## Example

A notification hook sends a desktop alert when a permission request is waiting. The request remains pending until a separate approval decision is made.

## Common confusion

A hook is a mechanism, not automatically a guardrail. A post-action hook cannot prevent an effect that already happened. Event names, tool coverage, response formats, and failure behavior differ across products.

## Study-group notes

Chapter 5 teaches event → matcher → handler. Verify the observable effect, actual tool input, timing, coverage, and behavior when the handler fails. Related SDKs may expose callbacks instead of command hooks.
