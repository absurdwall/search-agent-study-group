---
id: model-context-protocol
term: Model Context Protocol (MCP)
aliases: ["MCP", "Model Context Protocol"]
category: frameworks-and-protocols
sources: [{"title": "Chapter 2: A Map of Modern Agent Systems — Model Context Protocol", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/modern-agent-systems/#mcp", "note": "Provides the definition, integration motivation, participant roles, primitives, connection walkthrough, and host-policy boundary."}, {"title": "Chapter 2: A Map of Modern Agent Systems — How the pieces relate", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/modern-agent-systems/#how-the-pieces-relate", "note": "Places MCP beside instruction files and Skills without making it a required stage of the agentic loop."}]
relations: [{"type": "related", "target": "tool"}, {"type": "contrasts_with", "target": "skill"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

An open protocol for AI applications to discover external capabilities and exchange requests, results, and related messages.

## Working definition

MCP provides a shared client–server boundary between an AI application and capability providers. The host is the application; a client is its protocol component for one server; the server exposes underlying capabilities. Servers can offer Tools (operations), Resources (readable information), and Prompts (reusable interaction templates). The protocol standardizes discovery and message exchange, while the host decides what reaches the model and how results enter the workflow.

## Why it matters

A reusable boundary reduces duplicated integration work when many applications connect to many providers. It is useful when interoperability or discovery matters, but adds little to a simple local function that needs neither.

## Example

A study-group editor connects to an approved issue-tracker server, discovers its issue-query tool, exposes that tool to the model, and brings the returned issue data into the chapter-review loop.

## Common confusion

MCP is neither an agent nor one tool. A server may run locally, and an MCP Prompt is not a packaged Skill. The protocol does not supply the task method, choose trustworthy providers, grant permission for every action, or make every advertised capability model-visible.

## Study-group notes

Chapter 2 separates connection from method and execution. Its M×N-to-M+N analogy describes integration structure, not a guaranteed cost formula. Follow the chapter’s versioned discussion rather than treating every older protocol lifecycle as permanent.
