---
id: artifact
term: Artifact
aliases: ["output artifact", "generated artifact"]
category: control-and-quality
sources: [{"title": "Chapter 5: Inspect the trace and the artifacts", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#eval-workflow", "note": "Defines the term and its role in the chapter’s examples."}, {"title": "Chapter 5: Three files remain. Did all three originals survive?", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#evidence-lab", "note": "Shows why checking file counts alone misses changed contents or lost duplicate copies."}]
relations: [{"type": "related", "target": "trace"}, {"type": "related", "target": "fixture"}, {"type": "related", "target": "trial"}, {"type": "related", "target": "grader"}, {"type": "related", "target": "evaluation"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

An inspectable output of a run, such as a generated file.

## Working definition

An artifact is a produced output that a reviewer or grader can inspect independently of the agent’s final message. In agent evaluations, artifacts include generated code, documents, and reports. Check that they came from the current trial and assess their contents or behavior against the case’s criteria.

## Why it matters

Inspecting outputs can reveal incomplete or incorrect work even when an agent reports success or its trace contains plausible-looking actions.

## Example

For an app task, inspect the new package.json and components, then run the required build. For an organizer, compare the final files’ contents and copy counts with the originals.

## Common confusion

File presence does not prove a correct result, and an unchanged file count does not prove preservation. Final files also cannot establish that no temporary forbidden effect occurred during execution.

## Study-group notes

Use artifacts together with traces and external state. The chapter’s organizer examples are constructed teaching states, not recorded agent runs.
