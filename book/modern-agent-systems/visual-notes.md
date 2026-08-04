# Chapter 2 visual notes: A Map of Modern Agent Systems

Status: internal visual and provenance record. The chapter remains **Work in
progress**.

## Visual strategy

The chapter reuses seven owner-supplied source image files in six visual blocks.
No image was generated, redrawn, cropped, or adapted. Prose, semantic tables,
code blocks, captions, and alt text carry the complete teaching argument when
an image is unavailable.

The MCP tutorial pass adds only the three approved Hugging Face course files:
two paired source images for the M×N/shared-boundary comparison and one source
concept map for Tools, Resources, and Prompts. The available concept map is not
misidentified as a Host/Client/Server architecture diagram.

The approved direct-MCP-calls-versus-code-execution figure is deliberately not
used: the prose contrast is sufficient, and an additional implementation-pattern
visual would over-weight behavior that is not part of the protocol.

The final Skills pass adds one Anthropic source visual beside the package-anatomy
example. It shows installed Skills as filesystem directories and one PDF Skill
containing core instructions, supporting Markdown, and executable code. This is
complementary to the existing context-window visual, which teaches activation
and progressive disclosure rather than package composition.

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

## C2-V04 — Without/with MCP comparison

- **Local files:** `assets/without mcp.png` and `assets/with mcp.png`
- **Dimensions:** 897 × 373 and 1114 × 373
- **SHA-256:**
  - `ace4baa10a5007dcc18689b223781d23f8d941e09cec016f70b8bef2f1f1fe86`
  - `5b9d31c0b23d6f44ffdfb61ca71fb207b1baa237e34fff576068a99727a8e324`
- **Exact upstream files:** `unit1/1a.png` and `unit1/2.png`, linked from
  Hugging Face MCP Course, “Key Concepts and Terminology”
  https://huggingface.co/learn/mcp-course/unit1/key-concepts
- **Teaching job:** contrast up to M×N pairwise application/provider adapters
  with the course's conceptual M+N shared-protocol simplification.
- **Qualification:** the caption explicitly states that M+N is an architectural
  simplification, not a literal implementation-cost guarantee.
- **Accessibility:** each image has mechanism-level alt text, intrinsic
  dimensions, and its own full-size link; the surrounding prose and caption
  explain the comparison without relying on color.

## C2-V05 — MCP server primitives

- **Local file:** `assets/mcp component.png`
- **Dimensions:** 786 × 283
- **SHA-256:** `ace68b97c579afb4826cdf2ca894869495583a142e169a9d0ad005c93e71526b`
- **Exact upstream file:** `unit1/8.png`, linked from Hugging Face MCP Course,
  “Key Concepts and Terminology”
  https://huggingface.co/learn/mcp-course/unit1/key-concepts
- **Teaching job:** reinforce the distinction between Tools, Resources, and
  Prompts after the text defines the three current server primitives.
- **Qualification:** the caption says that the image is not a
  Host/Client/Server architecture diagram. It does not present Sampling as an
  equal current primitive.
- **Accessibility:** detailed alt text names each example and relationship;
  intrinsic dimensions and a full-size link are present.

## C2-V06 — Skills as filesystem packages

- **Local file:** `assets/agent skill vm.jpeg`
- **Dimensions:** 1650 × 929
- **SHA-256:** `fa409512e8d0b9cba8e8c53de1beb0cf8a3901c27c4628b966d05125292df688`
- **Source:** Anthropic, “Equipping agents for the real world with Agent Skills”
  https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Source location:** the first mechanism diagram immediately before “The
  anatomy of a skill”; the article describes activating Skills through a
  `SKILL.md` file and organized folders of instructions, scripts, and resources.
- **Teaching job:** show that equipped Skills correspond to directories in an
  agent runtime and that one package can combine `SKILL.md`, supporting Markdown
  files, and an executable script.
- **Placement:** immediately after the `documentation-review/` directory tree in
  “Anatomy of a Skill.”
- **Qualification:** the caption labels the diagram Anthropic-oriented and says
  exact installation and runtime wiring differ by client.
- **Reuse:** copied byte-for-byte from the owner-provided local download; no
  cropping, relabeling, tracing, or other adaptation.
- **Accessibility:** detailed alt text describes the agent-to-filesystem
  relationship, the example Skill directories, the PDF package contents, and
  the separately configured MCP servers; the full-size local image is linked.

## Anthropic candidate audit

All four candidate downloads were inspected at their intrinsic size and mapped
to their position in the Anthropic article. Only C2-V06 was selected.

- `assets/agent skill vm.jpeg` — 1650 × 929; first mechanism diagram before
  “The anatomy of a skill”; teaches the relationship between equipped Skills,
  runtime filesystem directories, supporting files, and executable code.
  **Selected** because it adds package structure without repeating activation.
- `assets/a simple skill md.webp` — 1650 × 929; the first figure inside “The
  anatomy of a skill”; teaches YAML frontmatter and the Markdown body of one
  `SKILL.md`. **Not used** because the existing prose already explains those two
  parts and the image does not show the wider package.
- `assets/build additional content.webp` — 1650 × 1069; follows the article's
  explanation of bundling additional files; shows `SKILL.md` linking to
  `reference.md` and `forms.md`. **Not used** because it substantially overlaps
  the existing directory tree and the context-window figure's referenced forms
  file.
- `assets/executable script.webp` — 1650 × 929; appears under “Skills and code
  execution”; shows `forms.md` invoking a Python extraction script. **Not used**
  because scripts are already explained in the anatomy prose and end-to-end
  walkthrough, while the selected image covers the broader package relationship.

## Provenance and reuse note

All seven exact files were supplied by the owner in the main project checkout and
explicitly approved for this Chapter 2 revision. The chapter attributes each
asset to its direct source page.

For the three Hugging Face additions, byte hashes match the exact course-linked
dataset files listed above. The MCP Course source repository is published under
Apache License 2.0:
https://raw.githubusercontent.com/huggingface/mcp-course/main/LICENSE
The official image dataset route currently redirects to
`context-course/images`, whose README declares `license: apache-2.0`:
https://huggingface.co/datasets/mcp-course/images/raw/main/README.md
This finding is limited to the identified course repository and dataset; it is
not a claim about every image hosted on Hugging Face.

No separate image-specific reuse license was established for the four
Anthropic/MCP visuals, including C2-V06. Their publication-time rights review
remains an editorial/provenance item.

## Convergence gate

Do not add another visual unless review identifies a teaching relationship that
readers cannot reconstruct from the current prose, tables, and six visual
blocks. Any replacement still needs exact provenance, intrinsic dimensions,
alt text, a visible caption, mobile verification, and reduced-motion handling
when relevant.
