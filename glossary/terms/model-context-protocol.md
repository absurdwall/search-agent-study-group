---
id: model-context-protocol
term: Model Context Protocol (MCP)
aliases: ["MCP", "Model Context Protocol"]
category: frameworks-and-protocols
status: published
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "google-adk"},
  {"type": "related", "target": "tool"}
]
sources: [
  {
    "title": "Model Context Protocol specification overview",
    "url": "https://modelcontextprotocol.io/specification/2025-06-18/basic/index",
    "note": "Defines the protocol's JSON-RPC base, lifecycle, capabilities, and client-server responsibilities."
  },
  {
    "title": "MCP server features",
    "url": "https://modelcontextprotocol.io/specification/2025-06-18/server/index",
    "note": "Documents the tools, resources, and prompts that MCP servers can expose to clients."
  }
]
---

## Simple definition

An open protocol connecting AI applications to tools, resources, and prompt templates through client-server interfaces.

## Working definition

Model Context Protocol is an open client-server protocol for exposing capabilities and context to AI applications through standardized messages. MCP servers can offer tools, resources, and prompt templates; MCP clients negotiate capabilities and make those primitives available to the host application or agent.

## Why it matters

MCP separates capability providers from agent frameworks. A compatible server can expose the same integration to multiple clients, reducing one-off adapter code and giving applications a consistent discovery and invocation model.

## Example

An inventory MCP server exposes `search_products` and `get_stock` tools. ADK connects as an MCP client and presents their schemas to an agent alongside local tools.

## Common confusion

MCP is a protocol, not an agent framework or a tool by itself. It defines how clients and servers communicate; the server implements capabilities, the host manages connections, and the model may decide when to request an exposed tool.

## Study-group notes

Week 1 used the “standard plug shape” analogy: an MCP client such as ADK connects to a server and makes its remote capabilities available in the agent's tool set.
