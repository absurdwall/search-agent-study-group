---
id: workflow
term: Workflow
aliases: ["LLM workflow", "agentic workflow"]
category: agent-systems
status: published
last_reviewed: 2026-07-27
relations: [
  {"type": "contrasts_with", "target": "agentic-loop"},
  {"type": "related", "target": "agent"},
  {"type": "uses", "target": "large-language-model"},
  {"type": "uses", "target": "tool"}
]
sources: [
  {
    "title": "Anthropic — Building effective agents",
    "url": "https://www.anthropic.com/engineering/building-effective-agents",
    "note": "Defines workflows as systems where LLMs and tools are orchestrated through predefined code paths and presents five common workflow patterns."
  }
]
---

## Simple definition

A software-defined arrangement of model calls, tools, stages, branches, roles, or feedback paths.

## Working definition

A workflow arranges LLM calls and tools through an overall control structure defined in software. Individual steps can still ask a model to classify, generate, evaluate, route, or decompose a task; what remains predefined is the larger arrangement of stages, branches, roles, or feedback paths.

## Why it matters

Workflows provide predictable structure for tasks whose overall topology is known in advance. They can combine deterministic code with model judgments and can contain an agentic step, while an agent can also invoke a deterministic workflow as one capability.

## Example

A routing workflow first classifies a customer request, sends it to a billing, technical-support, or general-information path, and then returns the selected path's response.

## Common confusion

Workflow does not mean that every step is fixed or non-intelligent. Anthropic categorizes orchestrator-workers as a workflow even though the orchestrator dynamically chooses subtasks, because the overall delegation-and-synthesis topology is predefined.

## Study-group notes

Chapter 1 compares prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer as five workflow patterns.
