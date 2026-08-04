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

Memory, subagents, and plugins remain short planned sections. The chapter does
not yet teach long-term memory, controls, broad multi-agent orchestration, MCP
server implementation, or Skill authoring.

## Teaching sequence

| Section | Teaching job | Primary sources | Boundary |
|---|---|---|---|
| Introduction | Reconnect to Chapter 1 and separate the three jobs | OpenAI Customization; Anthropic Extend Claude Code | Product maps are orientation, not a universal taxonomy |
| 1. Instruction files | Teach durable content selection; Codex global, project, merge, fallback, and size behavior; Claude scopes and writing guidance; Claude and GitHub path rules; a complete example; interoperability; and the memory/Skills boundaries | OpenAI AGENTS.md (tutorial spine); Claude memory; AGENTS.md; GitHub custom instructions | Markdown can travel; loading behavior belongs to the host; memory is deferred |
| 2. MCP | Use the USB-C analogy and M×N problem to motivate a shared boundary; teach participants, layers, primitives, a complete exchange, one host implementation, fit and non-goals; then statelessness, code execution, Apps, and Registry | Hugging Face MCP Course Unit 1 (teaching spine); versioned MCP Architecture (current authority); OpenAI MCP; Anthropic launch; Simon Willison; Anthropic code execution; MCP Apps; Registry | MCP is not the agentic loop, a trust guarantee, or a reusable method |
| 3. Skills | Teach package anatomy, discovery, activation, progressive disclosure, an end-to-end workflow, component roles, portability, product implementations, selection guidance, and two frontier shifts: installable distribution and agent-assisted workflow capture | Anthropic Agent Skills (teaching spine); Agent Skills Overview (format); OpenAI (host implementation); Claude; Google ADK; Vercel; skills.sh | Client activation differs; detailed authoring belongs to Chapter 4 |
| 4. How the pieces relate | Combine the mechanisms around one neutral Week 3 task and identify live boundary questions | Vercel evaluation; Skills Over MCP Working Group | MCP and Skills stay optional |
| 5–7. Planned | Mark memory, subagents, and plugins without pretending the teaching is ready | None assigned | No cross-product definition or reading is frozen |

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

- Hugging Face — MCP Course, Unit 1
  https://huggingface.co/learn/mcp-course/en/unit1/introduction
  - Key Concepts and Terminology
    https://huggingface.co/learn/mcp-course/unit1/key-concepts
  - Architectural Components
    https://huggingface.co/learn/mcp-course/unit1/architectural-components
  - The Communication Protocol
    https://huggingface.co/learn/mcp-course/en/unit1/communication-protocol
  - Understanding MCP Capabilities
    https://huggingface.co/learn/mcp-course/en/unit1/capabilities
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
- The Hugging Face MCP Course is the beginner teaching spine for motivation,
  terminology, communication concepts, and source visuals; version-sensitive
  claims are filtered against the current official architecture.
- The three Hugging Face visuals are exact copies of course-linked dataset files
  `unit1/1a.png`, `unit1/2.png`, and `unit1/8.png`. The course repository
  and the image dataset declare Apache License 2.0; this provenance does not
  generalize to unrelated Hugging Face-hosted images.
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

## Tutorial coverage audit

### Instruction files

- Problem: durable repository knowledge should not be repeated in each prompt.
- Stable mechanism: a compatible host discovers, selects, composes, and loads
  file-based guidance into active context.
- Walkthrough: root and `book/` guidance apply to the Chapter 2 path while
  frontend and backend sibling guidance does not.
- Content: project overview, commands, standards, security, review requirements,
  deployment and data handling, and repository gotchas are curated as examples
  rather than a mandatory schema.
- Product detail: Codex global and project discovery, override and fallback
  order, root-to-working-directory concatenation, and the Codex-specific 32 KiB
  default cap; Claude managed, user, project, local, imported, nested, and
  path-scoped guidance; GitHub `applyTo` path-specific instructions and
  `excludeAgent`.
- Writing: Claude's under-200-lines recommendation is labeled product-specific
  and separated from the Codex byte cap; structure, specificity, conflict
  removal, and lack of hard enforcement are explicit.
- Example: the official sample `AGENTS.md` is available in a collapsed,
  JavaScript-free disclosure with source attribution.
- Boundary: Claude auto memory is distinguished from team-authored instructions
  and deferred to the planned Memory section; path rules sit between broadly
  loaded instructions and on-demand Skills.
- Close: distinguish instruction files from Skills, then transition directly
  from durable guidance to MCP's shared connection problem.

### MCP

- Problem: a repeated Tool definition is not a complete integration; without a
  shared boundary, M applications and N providers may require up to M×N
  pairwise adapters. The course's M+N framing is labeled an architectural
  simplification rather than a literal cost guarantee.
- Stable mechanism: host, one client per server, local or remote server, data
  and transport layers, discovery, tools, resources, prompts, and notifications.
- Teaching devices: the course's USB-C analogy is bounded at the connection
  layer; exact source images `unit1/1a.png` and `unit1/2.png` compare the
  pairwise and shared-boundary models, while `unit1/8.png` distinguishes Tools,
  Resources, and Prompts.
- Version filter: the basic tutorial uses stdio and Streamable HTTP, avoids the
  retired initialization/session lifecycle, and omits Sampling from the current
  core primitives because it is deprecated in protocol version `2026-07-28`.
- Walkthrough: configuration through selected result entering the next Chapter
  1 loop, with protocol actions separated from host policy.
- Product detail: OpenAI remote configuration, tool import, `allowed_tools`,
  approvals, OAuth, and server trust as one implementation.
- Frontier: 2026-07-28 stateless requests, bounded code composition, MCP Apps,
  and the preview Registry.

### Skills

- Problem: broad capabilities do not supply a consistent domain procedure, and
  permanent playbooks do not scale in context.
- Stable mechanism: `SKILL.md`, references, scripts, assets, discovery,
  implicit or explicit activation, and progressive disclosure.
- Walkthrough: documentation review from metadata match through selective
  references, deterministic validation, template-based evidence, and the normal
  Chapter 1 loop.
- Product detail: portable package center plus OpenAI, Claude Code, and
  experimental Google ADK runtime differences.
- Frontier: two shifts only—local folders becoming discoverable, installable,
  updateable packages through one emerging Vercel ecosystem; and successful
  work becoming evidence for agent-assisted draft Skills that remain subject to
  human review, testing, versioning, and ownership.
