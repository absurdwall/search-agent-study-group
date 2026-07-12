---
id: agent-evaluation
term: Agent evaluation
aliases: ["agent eval", "agent evals"]
category: control-and-quality
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "agent"},
  {"type": "related", "target": "guardrail"},
  {"type": "related", "target": "tool"}
]
sources: [
  {
    "title": "Why evaluate agents",
    "url": "https://adk.dev/evaluate/",
    "note": "Explains why probabilistic agents require evaluation of both final results and the trajectory used to reach them."
  },
  {
    "title": "ADK Evaluation Criteria",
    "url": "https://adk.dev/evaluate/criteria/",
    "note": "Provides concrete criteria for tool trajectory, response quality, groundedness, safety, and multi-turn task success."
  }
]
---

## Simple definition

A repeatable test of whether an agent completes tasks well and behaves acceptably.

## Working definition

Agent evaluation is the systematic testing of whether an agent succeeds on representative tasks and behaves acceptably along the way. It can measure final answers, tool choices and arguments, action trajectories, groundedness, safety, latency, and cost.

## Why it matters

Agent behavior varies across runs and can fail even when the final response looks plausible. Repeatable eval cases and criteria make changes measurable and reveal where the process, not only the answer, breaks down.

## Example

An order-support eval set checks whether the agent selects the correct lookup tool, passes the right order ID, avoids unauthorized actions, and returns a grounded answer across common and edge cases.

## Common confusion

Agent evals complement rather than replace ordinary unit and integration tests. Deterministic code should still be tested deterministically; evals address variable model behavior and end-to-end task quality.

## Study-group notes

Evaluation targets should match the task: an acceptable alternate tool path may need rubric-based scoring rather than exact trajectory matching.
