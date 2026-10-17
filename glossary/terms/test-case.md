---
id: test-case
term: Test case
aliases: ["eval case", "evaluation case"]
category: control-and-quality
sources: [{"title": "Chapter 5: Follow one case through an evaluation", "url": "https://absurdwall.github.io/search-agent-study-group/book/guardrails-hooks-and-evals/#eval-workflow", "note": "Defines the term and its role in the chapter’s examples."}]
relations: [{"type": "related", "target": "fixture"}, {"type": "related", "target": "trial"}, {"type": "related", "target": "grader"}, {"type": "related", "target": "evaluation"}, {"type": "related", "target": "evaluation-suite"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

A defined request, known starting state, and criteria for deciding whether the system succeeds.

## Working definition

A test case specifies the task an agent will receive, the starting files or data, and the checks or quality criteria used to assess it. It should also make relevant permissions and allowed effects clear. The same case can be run repeatedly as separate trials.

## Why it matters

Writing a case before execution prevents success from being redefined to fit the result and makes comparisons more meaningful.

## Example

Start from a fresh disposable repository. Ask for a demo app with a header and two cards. Require expected files, a passing build, an understandable layout, and no publication.

## Common confusion

A prompt alone may leave the starting state and success conditions unspecified. An agent’s statement that it finished is a claim to check, not a sufficient success criterion.

## Study-group notes

For a Skill case, include realistic prompts and necessary inputs. A captured conversation is a useful starting point but must be reviewed before treating it as a correct reference.
