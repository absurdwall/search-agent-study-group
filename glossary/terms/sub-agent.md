---
id: sub-agent
term: Sub-agent
aliases: ["child agent", "ADK sub-agent"]
category: agent-systems
status: published
last_reviewed: 2026-07-12
relations: [
  {"type": "broader", "target": "agent"},
  {"type": "related", "target": "llm-agent"},
  {"type": "related", "target": "runner"}
]
sources: [
  {
    "title": "Agents in ADK",
    "url": "https://adk.dev/agents/",
    "note": "Describes ADK agents as self-contained execution units that can be composed into multi-agent systems."
  },
  {
    "title": "Function tools: Agent-as-a-Tool",
    "url": "https://adk.dev/tools/function-tools/",
    "note": "Explicitly distinguishes responsibility transfer to a sub-agent from calling another agent through AgentTool and returning control to the parent."
  }
]
---

## Simple definition

A child agent that can receive delegated responsibility from a parent agent inside a multi-agent system.

## Working definition

A sub-agent is an agent composed beneath another agent and available for delegated work. In current ADK terminology, transferring to a sub-agent changes which agent is responsible for answering, while wrapping an agent with `AgentTool` creates an agent-as-a-tool whose result returns to the parent.

## Why it matters

Specialized agents can isolate instructions, tools, models, and responsibilities. Choosing between transfer and call-and-return affects routing, conversational ownership, context, cost, and which agent handles the next user message.

## Example

A shopping agent transfers a returns conversation to a returns sub-agent that continues with the user. By contrast, it may call a research agent through `AgentTool`, receive a product summary, and then retain control of the conversation.

## Common confusion

ADK does not use “sub-agent” and “agent-as-a-tool” as interchangeable terms. A sub-agent receives control through delegation or transfer; an `AgentTool` performs bounded work and returns its answer to the calling agent.

## Study-group notes

Week 1 used “sub-agent called as a tool” as broad shorthand. This glossary keeps the teaching comparison—separate agent versus loaded instructions—but adopts ADK's current, more precise distinction.
