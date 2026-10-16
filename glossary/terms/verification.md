---
id: verification
term: Verification
aliases: ["final check"]
category: control-and-quality
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "guardrail"}, {"type": "related", "target": "completion-criteria"}, {"type": "related", "target": "evaluation"}]
sources: [{"title": "Chapter 3 · Boundaries and verification", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/prompting-and-context/#boundaries-verification", "note": "Current chapter treatment and teaching distinctions."}]
---

## Simple definition

Checking a result against observable evidence that can show it is wrong or incomplete.

## Working definition

Verification compares the delivered work with a relevant signal: tests, source evidence, reconciled figures, required sections, or a rendered reference. The signal should be capable of disagreeing with the agent’s claim of completion.

## Why it matters

Without a checkable result, confident completion can hide missing requirements or errors.

## Example

Reproduce a failing test, apply the fix, and rerun the same test before reporting success.

## Common confusion

Asking “Are you finished?” is another assertion, not independent evidence. Verification of one result is also different from an eval across repeatable tasks and trials.

## Study-group notes

Chapter 3 introduces observable checks; Chapter 5 develops gates and systematic evaluation.
