---
id: callback
term: Callback
aliases: ["lifecycle callback", "agent callback"]
category: control-and-quality
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "guardrail"}, {"type": "related", "target": "runner"}, {"type": "related", "target": "tool"}]
sources: [{"title": "Chapter 5 · Hooks", "url": "https://absurdwall.github.io/search-agent-study-group/book/guardrails-hooks-and-evals/#hooks", "note": "Relates hooks to framework callback mechanisms."}]
---

## Simple definition

A function registered for the runtime to call at a supported point in execution.

## Working definition

A callback is developer code invoked by a framework around a supported operation, such as a model or tool call. It may observe, modify, skip, or reject work only where the framework’s interface permits.

## Why it matters

Callbacks provide controlled intervention points without rewriting the core agent loop. They support tracing, policy enforcement, approvals, caching, state updates, request adaptation, and performance optimizations.

## Example

A `before_tool` callback checks a proposed `place_order` call. If the session lacks explicit customer confirmation, it returns a blocked result and the purchasing function never runs.

## Common confusion

Callback and hook are related implementation terms, not a promise of identical behavior across frameworks. A callback only enforces a guardrail if it runs at the right time and has the required authority.

## Study-group notes

Chapter 5 connects SDK callbacks to the broader lifecycle-hook idea; the runtime determines their exact coverage and effects.
