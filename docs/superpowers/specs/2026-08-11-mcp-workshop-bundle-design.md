# 2026-08-11 MCP Workshop Bundle Design

## Objective

Publish the August 11 MCP workshop as a self-contained study-group bundle:

- one downloadable, offline HTML deck under `presentations/`; and
- all participant, instructor, exercise, and solution notebooks with their runtime dependencies under `weeks/2026-08-11/`.

The pull request must not depend on the source repository's directory layout or contain credentials, private paths, build caches, or executed debug dumps.

## Destination layout

```text
presentations/
  mcp-skills-subagents-intro.html

weeks/2026-08-11/
  .env.example
  materials.md
  skills/
    order-support/
      SKILL.md
    product-shopping-mcp/
      SKILL.md
    store-information/
      SKILL.md
  notebooks/
    .python-version
    requirements.txt
    05_mcp_under_the_hood_instructor.ipynb
    05_orders_mcp_skill_subagents_demo_phoenix.ipynb
    06_ecommerce_skills_vs_subagents_instructor_phoenix.ipynb
    07_product_mcp_skill_takehome_exercise_phoenix.ipynb
    07_product_mcp_skill_takehome_solution_phoenix.ipynb
    08_ecommerce_composition_takehome_exercise_phoenix.ipynb
    mcp_workshop/
      __init__.py
      workshop_helpers.py
    orders_workshop/
      __init__.py
      tools_order.py
      tools_store.py
    product_takehome/
      product-shopping-code/
        SKILL.md
```

Participant and instructor materials stay together in the same notebook directory, as requested. Filenames identify exercises, solutions, and instructor demos without another folder layer.

## Packaging rules

### Presentation

Copy the generated `mcp-skills-subagents-intro.html` artifact, not its React/Vite authoring project. The resulting file must open directly from disk, contain its scripts and styles inline, preserve keyboard navigation, and require no network assets.

### Notebooks

Copy the generated source notebooks, not executed copies. Preserve their current relative imports and embedded image attachments. Include only runtime support files referenced by these notebooks, including the prepared Order, Store, and Product Skills resolved from the dated week root. Exclude notebook builders, deck source code, tests, temporary environments, and unrelated earlier-week helpers.

### Configuration

Standardize the bundle on Python `>=3.12,<3.13`. `requirements.txt` is the installation source of truth. `.env.example` documents variable names and safe placeholder values only. `materials.md` explains notebook order, setup, the remote ecommerce MCP dependency, Phoenix tracing, and which files are exercises versus references.

No `pip install` cells will be added to notebooks because participants use hosted JupyterLab.

## Portability and safety

- Notebook code must resolve helpers relative to `weeks/2026-08-11/notebooks/`, with no dependency on the source repository.
- The public MCP endpoint may be referenced; credentials and private `.env` values may not.
- No `/home/...`, `.codex/attachments`, raw `Event(model_version=...)` dumps, API keys, or Walmart-specific legacy tool names may appear in the packaged artifacts.
- The presentation and notebooks must retain generic ecommerce names: `search_products` and `product_details`.
- The source repository and exact source commit will be recorded in `materials.md` for provenance.

## Verification

Before opening the pull request:

1. Validate every notebook with `nbformat` and confirm source code cells contain no execution outputs.
2. Execute the four completed/instructor notebooks top-to-bottom from the destination layout using Python 3.12 and the project-level runtime environment, while keeping executed copies outside the repository.
3. Execute each participant exercise through its first learner-owned assertion; confirm all setup imports and dependencies work and that execution stops for the expected `YOUR TURN` checkpoint rather than an environment failure.
4. Confirm the completed notebooks show the expected MCP, Skill, subagent, and Phoenix behaviors with zero notebook errors.
5. Open the standalone deck through both a local HTTP server and a direct `file://` browser load; verify keyboard navigation, slide count, offline assets, and no console errors.
6. Scan all added files for credentials, private source paths, legacy Walmart names, and raw event dumps.
7. Confirm a fresh clone can install `notebooks/requirements.txt` and import both helper packages from the dated notebook directory.

## Pull request

Create a draft pull request from `codex/2026-08-11-mcp-workshop` into `main`. The PR description will list the deck, notebook sequence, included helpers, Python 3.12 requirement, source provenance, and verification evidence.
