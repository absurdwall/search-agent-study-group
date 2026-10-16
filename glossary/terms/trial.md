---
id: trial
term: Trial
aliases: ["eval trial", "evaluation trial"]
category: control-and-quality
sources: [{"title": "Chapter 5: Run a trial and save the evidence", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#eval-workflow", "note": "Defines the term and its role in the chapter’s examples."}]
relations: [{"type": "related", "target": "test-case"}, {"type": "related", "target": "fixture"}, {"type": "related", "target": "trace"}, {"type": "related", "target": "artifact"}, {"type": "related", "target": "grader"}, {"type": "related", "target": "evaluation"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

One attempt at running a defined test case.

## Working definition

A trial executes a test case once from its intended starting state. Capture its trace, outputs, errors, and outcome, together with model/runtime versions, instructions, tools, and permissions. Repeating a case produces multiple trials that may behave differently.

## Why it matters

Separating cases from attempts makes variability visible and prevents a single successful run from standing in for reliability.

## Example

Run the same app request three times, resetting the repository each time. If two builds pass and one fails, report two of three successful build checks and investigate the failure.

## Common confusion

A case describes what to test; a trial is one execution of it. Retries inside one agent run are not automatically independent trials, and starting a command does not prove it completed.

## Study-group notes

Save command exit status and error output as well as structured events. A blocked or failed trial is still useful evidence and should not silently disappear from the results.
