---
id: loop-engineering
term: Loop engineering
aliases: ["recurring agent loop"]
category: agent-systems
status: published
last_reviewed: 2026-10-16
relations: [{"type": "related", "target": "agentic-loop"}, {"type": "related", "target": "agentic-harness"}, {"type": "related", "target": "workflow"}]
sources: [{"title": "Chapter 3 · Beyond prompting", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/prompting-and-context/#beyond-prompting", "note": "Current chapter treatment and teaching distinctions."}]
---

## Simple definition

Designing a system that repeatedly finds work, assigns it, checks results, and records what comes next.

## Working definition

An emerging practitioner framing for the recurring system around individual agent runs. It combines work discovery, assignment, checks, durable records, and a decision about the next run.

## Why it matters

Repeated jobs need explicit progress records and stopping rules, not just a longer initial prompt.

## Example

A maintenance process finds an issue, delegates a bounded repair, checks the result, records it, and decides whether another task should run.

## Common confusion

This is not the minimal model–tool–result agentic loop or a standardized architecture. Recurrence adds cost and risk and should be justified by the task.

## Study-group notes

Chapter 3 presents loop engineering as an emerging, deliberately qualified extension beyond direct prompting.
