---
id: fixture
term: Fixture
aliases: ["test fixture", "eval fixture"]
category: control-and-quality
sources: [{"title": "Chapter 5: Write a case before running the agent", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#eval-workflow", "note": "Defines the term and its role in the chapter’s examples."}]
relations: [{"type": "related", "target": "test-case"}, {"type": "related", "target": "trial"}, {"type": "related", "target": "artifact"}, {"type": "related", "target": "evaluation"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

Saved starting files or data that let a test run begin from a known state.

## Working definition

A fixture supplies the known input files or data for a test case. Restore the intended starting state before each trial, and keep the original reference outside the agent’s editable output when it is needed to check preservation.

## Why it matters

Leftover outputs or changed inputs can make a failed task appear successful and make two trials incomparable.

## Example

A file-organizer fixture contains three originals with contents A, B, and B. Each trial begins with those same three files; an independent reference records both contents and copy counts.

## Common confusion

The fixture is the starting input, not the generated result. The full test case also includes the request and success criteria; clean files alone do not establish identical tools or permissions.

## Study-group notes

Chapter 5 uses a fresh repository for the app example and preserved originals for the organizer. Record environment and permission differences separately from the fixture.
