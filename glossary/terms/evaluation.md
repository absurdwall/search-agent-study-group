---
id: evaluation
term: Evaluation
aliases: ["eval", "evals", "agent evaluation"]
category: control-and-quality
sources: [{"title": "Chapter 5: Evals", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#evals", "note": "Defines the term and its role in the chapter’s examples."}]
relations: [{"type": "related", "target": "test-case"}, {"type": "related", "target": "trial"}, {"type": "related", "target": "trace"}, {"type": "related", "target": "artifact"}, {"type": "related", "target": "grader"}, {"type": "related", "target": "evaluation-suite"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

A repeatable way to give a system a task, record what happens, and assess it against stated criteria.

## Working definition

An evaluation defines cases and success criteria, runs trials from known starting states, captures evidence, and uses graders to assess results. Agent evaluations examine the model together with instructions, tools, runtime, and controls. Results describe the selected cases, environment, evidence, and grading methods.

## Why it matters

One impressive run cannot show whether a system is reliable. Repeatable cases help reveal variation, diagnose failures, compare changes, and catch returning bugs.

## Example

Run an app-creation task in fresh repositories, inspect the generated files, independently test the build, and review the layout against a rubric. Report completion and quality separately.

## Common confusion

A single completion hook is not an eval suite. Passing selected checks does not prove all future tasks will succeed, and a successful test runner does not mean the agent’s task passed.

## Study-group notes

Chapter 5’s sequence is case → trial → evidence → graders → results → improvement. Preserve failing cases for regression tests and keep success criteria comparable when testing revisions.
