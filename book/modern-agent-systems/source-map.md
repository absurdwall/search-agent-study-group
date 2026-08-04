# Chapter 2 source map: A Map of Modern Agent Systems

Status: internal drafting map. The chapter remains **Work in progress**.

Current-state documentation checked: 2026-08-04.

## Chapter contract

Chapter 1 owns the minimal LLM–tool–result loop and working context. Chapter 2
asks how three surrounding mechanisms make that system fit repeatable project
work:

- instruction files provide durable project and path guidance;
- MCP provides a shared connection protocol for external capabilities and
  information; and
- Skills package reusable procedural knowledge and supporting resources.

Subagents and plugins remain short planned sections. The chapter does not teach
memory, controls, broad multi-agent orchestration, MCP server implementation, or
Skill authoring.

## Teaching sequence

| Section | Teaching job | Primary sources | Boundary |
|---|---|---|---|
| Introduction | Reconnect to Chapter 1 and separate the three jobs | OpenAI Customization; Anthropic Extend Claude Code | Product maps are orientation, not a universal taxonomy |
| 1. Instruction files | Explain known locations, host discovery, scoping, composition, and product-specific loading | AGENTS.md; OpenAI AGENTS.md; Claude memory; GitHub custom instructions | Markdown can travel; loading behavior belongs to the host |
| 2. MCP | Explain why the protocol appeared, the host–client–server boundary, a concrete exchange, limits, and the evolving frontier | Versioned MCP Architecture; OpenAI MCP; Anthropic launch; Simon Willison; Anthropic code execution; MCP Apps; Registry | MCP is not the agentic loop, a trust guarantee, or a reusable method |
| 3. Skills | Explain why capability is insufficient, progressive disclosure, one reusable workflow, implementations, and distribution | Anthropic Agent Skills; Agent Skills Overview; OpenAI; Claude; Google ADK; Vercel; skills.sh | Client activation differs; authoring belongs to Chapter 4 |
| 4. How the pieces relate | Combine the mechanisms around one neutral Week 3 task and identify live boundary questions | Vercel evaluation; Skills Over MCP Working Group | MCP and Skills stay optional |
| 5–6. Planned | Mark subagents and plugins without pretending the teaching is ready | None assigned | No definition or reading is frozen |

## Approved reference architecture

### Must read

- OpenAI — Customization
  https://learn.chatgpt.com/docs/customization/overview
- Anthropic — Extend Claude Code
  https://code.claude.com/docs/en/features-overview

### Instruction files

- OpenAI — Custom instructions with AGENTS.md
  https://learn.chatgpt.com/docs/agent-configuration/agents-md
- Anthropic — How Claude remembers your project
  https://code.claude.com/docs/en/memory
- AGENTS.md — Official format site
  https://agents.md/
- GitHub — Adding repository custom instructions
  https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions

### MCP

- MCP — Architecture overview, version 2026-07-28
  https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
- OpenAI — MCP and Connectors
  https://developers.openai.com/api/docs/guides/tools-connectors-mcp
- Anthropic — Introducing the Model Context Protocol
  https://www.anthropic.com/news/model-context-protocol

### Skills

- Anthropic — Equipping agents for the real world with Agent Skills
  https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Agent Skills — Overview
  https://agentskills.io/home
- OpenAI — Build Skills
  https://learn.chatgpt.com/docs/build-skills
- Claude Code — Extend Claude with Skills
  https://code.claude.com/docs/en/slash-commands
- Google ADK — Skills for ADK agents
  https://adk.dev/skills/

### Frontier and emerging directions

- Simon Willison — Stateless MCP has recaptured my interest
  https://simonwillison.net/2026/Jul/31/stateless-mcp/
- Anthropic — Code execution with MCP
  https://www.anthropic.com/engineering/code-execution-with-mcp
- MCP Apps — Bringing UI capabilities to MCP clients
  https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/
- Official MCP Registry
  https://modelcontextprotocol.io/registry/about
- Vercel — Agent Skills explained: An FAQ
  https://vercel.com/blog/agent-skills-explained-an-faq
- skills.sh
  https://skills.sh/
- Vercel — AGENTS.md outperforms Skills in our agent evals
  https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
- Skills Over MCP Working Group
  https://modelcontextprotocol.io/community/working-groups/skills-over-mcp

## Source-role guardrails

- The versioned MCP Architecture page is the protocol source of record.
- OpenAI, Claude Code, GitHub, and Google ADK documentation describe their own
  implementations.
- Simon Willison and Vercel supply practitioner interpretation, not standards.
- Google ADK Skills are labeled experimental.
- MCP Apps is labeled an extension.
- The official MCP Registry is labeled preview infrastructure.
- skills.sh is a directory, not the Agent Skills specification or a universal
  registry.
- The Vercel evaluation is not generalized beyond its tested task and harness.
- The Skills Over MCP Working Group is active work, not settled behavior.
