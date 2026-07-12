---
id: workflow
term: Workflow
aliases: ["LLM workflow", "agentic workflow"]
category: agent-systems
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "contrasts_with", "target": "agent"},
  {"type": "uses", "target": "large-language-model"},
  {"type": "uses", "target": "tool"}
]
sources: [
  {
    "title": "Building effective agents",
    "url": "https://www.anthropic.com/engineering/building-effective-agents",
    "note": "Defines workflows as systems in which LLMs and tools follow predefined code paths."
  },
  {
    "title": "A practical guide to building agents",
    "url": "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/",
    "note": "Frames a workflow as the sequence of steps required to reach a user's goal and explains when an LLM controls its execution."
  }
]
---

## Simple definition

A predefined sequence of steps used to complete a task.

## Working definition

A workflow is a sequence or graph of steps used to reach a goal. In an LLM workflow, code normally determines the path and invokes models or tools at predefined points.

## Why it matters

Workflows are often easier to predict, test, and operate than agents. They fit tasks whose branches and success conditions can be specified clearly in advance.

## Example

A content pipeline always drafts an outline, checks it against fixed criteria, writes the article, and then runs a final policy check.

## Common confusion

Some teams use “agentic workflow” for any automation containing an LLM. This glossary reserves “agent” for systems where the model dynamically directs the process, while acknowledging that broader usage exists.

## Study-group notes
