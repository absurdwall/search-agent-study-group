---
id: rubric
term: Rubric
aliases: ["grading rubric", "evaluation rubric"]
category: control-and-quality
sources: [{"title": "Chapter 5: Apply graders that match the question", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#eval-workflow", "note": "Defines the term and its role in the chapter’s examples."}]
relations: [{"type": "related", "target": "grader"}, {"type": "related", "target": "artifact"}, {"type": "related", "target": "test-case"}, {"type": "related", "target": "evaluation"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

Written criteria that guide judgments about output quality.

## Working definition

A rubric states the qualities a reviewer should assess and what acceptable or unacceptable work looks like. It helps a model or human grader make judgments against an explicit standard, especially when quality cannot be reduced to a simple exact check.

## Why it matters

Clear criteria make subjective review more consistent and make disagreements easier to inspect and resolve.

## Example

For an app with a header and two cards, ask whether the parts are distinguishable and their order is understandable. Include examples when those requirements are ambiguous.

## Common confusion

A rubric is the review standard, not the grader or its score. A model’s plausible explanation does not prove its judgment is correct, and layout quality does not establish build success.

## Study-group notes

Keep rubric-based quality checks separate from completion and safety checks. Review real outputs and calibrate automated judgments with people before relying on small score differences.
