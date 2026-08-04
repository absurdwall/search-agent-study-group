# Chapter 2 visual notes: A Map of Modern Agent Systems

Status: internal visual and provenance record. The chapter remains **Work in
progress**.

## Visual strategy

The chapter reuses three owner-supplied source visuals. No image was generated,
redrawn, cropped, or adapted. Prose, semantic tables, code blocks, captions, and
alt text carry the complete teaching argument when an image is unavailable.

The approved direct-MCP-calls-versus-code-execution figure is deliberately not
used: the prose contrast is sufficient, and a fourth visual would over-weight an
implementation pattern that is not part of the protocol.

## C2-V01 — Skills progressive disclosure

- **Local file:** `assets/Skills and the context window.webp`
- **Dimensions:** 1650 × 929
- **SHA-256:** `b3c51622c95d4f2a4e0a353f47f3f46d04f563284043dc04919236b9d1d4c9d8`
- **Source:** Anthropic, “Equipping agents for the real world with Agent Skills”
  https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Teaching job:** show metadata present first, `SKILL.md` loaded when the PDF
  task matches, and a supporting forms file loaded only when needed.
- **Qualification:** the caption identifies the sequence as Claude-oriented and
  states that exact activation differs by client.
- **Accessibility:** detailed alt text and the preceding three-stage ordered list
  carry the same mechanism; the full-size local asset is linked.

## C2-V02 — MCP Apps demonstration

- **Local file:** `assets/claude-colorpicker-apps.gif`
- **Dimensions:** 1080 × 836
- **SHA-256:** `8c3fea29797653a3bc53ec224a4d0b272db8a7a9644eae6a0a88f6d8834dbd10`
- **Source:** MCP Apps, “Bringing UI Capabilities To MCP Clients”
  https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/
- **Teaching job:** demonstrate that an MCP extension can return an interactive
  user interface rather than only text or structured data.
- **Qualification:** the prose and caption call MCP Apps an extension, not part
  of the minimal core protocol.
- **Accessibility:** detailed alt and caption explain the full sequence. Under
  reduced motion the GIF is hidden and a static text fallback is shown.

## C2-V03 — MCP Registry ecosystem

- **Local file:** `assets/ecosystem-diagram.excalidraw.svg`
- **Intrinsic SVG size:** 2786.814 × 1810.554; HTML ratio uses 1393 × 905
- **SHA-256:** `5b56d241de1c851ba2fe2c922debec6f7a8e2462f0fb47e12288af13d394ae3a`
- **Source:** Model Context Protocol, “The MCP Registry”
  https://modelcontextprotocol.io/registry/about
- **Teaching job:** distinguish the upstream official metadata registry from
  downstream discovery marketplaces, aggregators, hosts, and clients.
- **Qualification:** the Registry is labeled preview infrastructure, not a
  completed universal marketplace or a trust guarantee.
- **Accessibility:** descriptive alt and caption explain the relationships; the
  full-size local SVG is linked.

## Provenance and reuse note

These exact files were supplied by the owner in the main project checkout and
explicitly approved for this Chapter 2 revision. The chapter attributes each
asset to its direct source page. No separate image-specific reuse license was
asserted because none was established during this revision; this remains an
editorial/provenance item for independent review before publication.

## Convergence gate

Do not add another visual unless review identifies a teaching relationship that
readers cannot reconstruct from the current prose, tables, and three source
figures. Any replacement still needs exact provenance, intrinsic dimensions,
alt text, a visible caption, mobile verification, and reduced-motion handling
when relevant.
