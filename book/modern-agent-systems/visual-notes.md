# Chapter 2 visual notes: A Map of Modern Agent Systems

Status: internal visual planning notes. No asset in this file has been searched,
selected, generated, or embedded.

## C2-V01 — Agentic loop with verification and user steering

### VISUAL PLACEHOLDER

**Purpose**

Give the broad map a concrete runtime sequence without claiming that any one
framework implements the only valid loop.

**Preferred medium**

A short step-through animation with a static accessible fallback.

**Scene or sequence**

Show the repeating path `gather context → decide → act → observe → verify`.
After verification, branch to `continue`, `finish`, `ask a focused question`,
or `user redirects work`. A failed verification returns to gather context; a
successful verification may finish. Keep the runtime as the enclosing owner of
the cycle.

**Required concepts**

Context, action, observation, verification, stopping conditions, and user
steering.

**Avoid**

Do not use an infinite circular arrow without exits, show verification as merely
a successful tool response, or imply every agent must use a fixed number of
steps.

**Teaching payoff**

Readers should understand why a loop is a behavior pattern and why verification
and stopping are part of reliable operation.

**Placement**

Replace the non-rendered `C2-V01` comment at the end of the Chapter 2 agentic
loop section.

**Source strategy**

Evaluate current official runtime/agent-loop documentation first, including the
existing Claude Code and Google ADK references, then choose only a source that
is accurate, reusable, and does not imply a universal stack.

**Reuse requirements**

Record creator, source URL, license, required attribution, local-copy rights,
and a full text alternative before embedding.

## C2-V02 — Context is assembled from distinct layers

### VISUAL PLACEHOLDER

**Purpose**

Make the difference between active context and adjacent mechanisms scannable at
a glance.

**Preferred medium**

An interactive layered diagram or a two-state static comparison.

**Scene or sequence**

Center a bounded `context for this decision` area. Feed it with separate labeled
inputs: instructions, recent conversation, prior tool results, and retrieved
documents. Place `memory store` outside the boundary with a conditional
retrieval arrow, and `Skill` outside the boundary with a conditional load arrow.
Mark history as a candidate input rather than an always-complete transcript.

**Required concepts**

Per-call context, instructions, history, tool results, retrieval, memory, and
Skills; finite selection by a host.

**Avoid**

Do not draw memory as automatically resident in context, make a Skill synonymous
with context, or imply every source is always loaded.

**Teaching payoff**

Readers can diagnose “the agent knows this” by asking whether information was
stored, retrieved, loaded, or actually present for the current decision.

**Placement**

Replace the non-rendered `C2-V02` comment after the Chapter 2 context section.

**Source strategy**

Seek a source-backed reusable visual only if it preserves these distinctions;
otherwise create a neutral diagram after validating terminology against the
chapter’s cited documentation.

**Reuse requirements**

Record creator, source URL, license, attribution, embedding constraints, and
alt text before use.

## C2-V03 — MCP host, client, and server boundary

### VISUAL PLACEHOLDER

**Purpose**

Explain the MCP connection shape without presenting MCP as the agent itself.

**Preferred medium**

A source-linked architecture figure, with animation only if connection and
discovery sequencing add material teaching value.

**Scene or sequence**

Show one Host containing separate Client connections to two Servers. Each
Server exposes a distinct set of tools, resources, and prompts. Draw the agent
runtime inside or adjacent to the Host, with a label that the Host selects what
to expose and how results enter context.

**Required concepts**

Host, client, server, one client per server connection, tools/resources/prompts,
trust boundary, and runtime ownership.

**Avoid**

Do not make servers part of the model, show MCP as a universal tool requirement,
or hide approval, authentication, and capability filtering responsibilities.

**Teaching payoff**

Readers should see what MCP standardizes and what operational work remains with
the host application.

**Placement**

Replace the non-rendered `C2-V03` comment at the end of the MCP section.

**Source strategy**

Search the official MCP architecture documentation first; verify that any chosen
diagram is current and explicitly reusable before copying or embedding it.

**Reuse requirements**

Record creator, source URL, license, attribution, reproduction permission, and
accessible caption requirements before use.

## C2-V04 — Skill progressive disclosure

### VISUAL PLACEHOLDER

**Purpose**

Show a Skill as a reusable method that may be discovered and loaded, rather than
a single executable tool or an always-loaded instruction block.

**Preferred medium**

A compact sequence illustration or a click-through interaction.

**Scene or sequence**

Show `task cue` matching a short Skill description, then loading `SKILL.md`,
then selectively opening references or running deterministic helper scripts.
Place tool calls as possible actions within the method, not as the Skill itself.

**Required concepts**

Discovery, staged loading, reusable instructions, supporting references,
scripts, and the tool-versus-Skill distinction.

**Avoid**

Do not depict every Skill as automatically loaded, every script as agentic
reasoning, or every product as having the same activation rules.

**Teaching payoff**

Readers should understand why progressive disclosure keeps useful procedure
available without crowding the working context.

**Placement**

Replace the non-rendered `C2-V04` comment at the end of the Skills section.

**Source strategy**

Start with the Agent Skills specification and product documentation; use a
source only if its license and its product-specific loading assumptions are
clear.

**Reuse requirements**

Record creator, source URL, license, attribution, embedding rights, and a text
equivalent before use.

## C2-V05 — One request across the whole system map

### VISUAL PLACEHOLDER

**Purpose**

Synthesize the chapter’s layers around one ordinary maintenance request without
turning the map into a required product stack.

**Preferred medium**

An annotated static flow with optional progressive reveal.

**Scene or sequence**

Use the existing request, “Update the Week 3 page, verify its links, and
summarize what changed.” Trace: project instructions and request become context;
a relevant Skill supplies method; an approved capability may arrive through MCP;
the runtime executes an edit and verification; tool results return to context;
permissions/guardrails/hooks constrain steps; the loop ends with a report.
Show MCP and Skill as optional dashed branches, not mandatory steps.

**Required concepts**

Loop, context, reusable guidance, tools, optional MCP, controls, verification,
and termination.

**Avoid**

Do not imply all systems have subagents, MCP, Skills, hooks, or the same control
order. Do not turn the guide into a vendor-specific architecture.

**Teaching payoff**

Readers can connect the separate vocabulary to one real task while preserving
the difference between core behavior and optional extensions.

**Placement**

Replace the non-rendered `C2-V05` comment at the end of “How the pieces work
together.”

**Source strategy**

Evaluate cited official documentation and the chapter’s own verified sequence
first. If no reusable source explains this neutral cross-product view, create an
original diagram only after the relationship labels are reviewed.

**Reuse requirements**

Record creator, source URL, license, attribution, embedding permissions, and
accessible narrative before use.
