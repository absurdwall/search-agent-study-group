---
id: grader
term: Grader
aliases: ["eval grader", "evaluation grader"]
category: control-and-quality
sources: [{"title": "Chapter 5: Apply graders that match the question", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#eval-workflow", "note": "Defines the term and its role in the chapter’s examples."}, {"title": "Chapter 5: File presence is a limited check", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#eval-grader-example", "note": "Uses a file-existence grader to illustrate how a passing check can establish much less than task success."}]
relations: [{"type": "related", "target": "rubric"}, {"type": "related", "target": "trial"}, {"type": "related", "target": "trace"}, {"type": "related", "target": "artifact"}, {"type": "related", "target": "evaluation"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

Code, a model, or a human reviewer that assesses evidence from a trial against a criterion.

## Working definition

A grader applies a particular check or judgment to a trial’s evidence. Code can test exact conditions such as valid files or a passing build. A model or human can review quality using an explicit rubric. Several graders can assess different requirements within the same evaluation.

## Why it matters

A score is only useful when its check matches the real requirement. Weak graders can reward missing, incorrect, or incomplete work.

## Example

One grader checks that the app builds; another judges whether its header and cards are understandable. A file-existence check alone would miss an app that cannot run.

## Common confusion

The grader is not the runner that launches the trial, and validly formatted grading output can still be wrong. Test graders on known good and deliberately bad results.

## Study-group notes

Chapter 5 separates exact checks from quality judgments. Compare model grades with human review, require evidence, and investigate disagreements rather than trusting the aggregate score.
