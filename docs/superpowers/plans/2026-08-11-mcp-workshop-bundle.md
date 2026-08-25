# August 11 MCP Workshop Bundle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a portable August 11 workshop bundle containing one standalone HTML deck and all runnable participant and instructor notebooks with their exact runtime dependencies.

**Architecture:** Treat the merged `adk_agent` workshop artifacts at source commit `614c5a8` as immutable inputs. Copy the generated deck and notebooks into the study-group layout, preserve the notebook package structure, add the three prepared Skills at the dated week root, and verify the destination as if it were a fresh checkout.

**Tech Stack:** Static HTML, Jupyter notebooks, Python 3.12, Google ADK 2.6.3, MCP 1.29.0, Phoenix/OpenInference, GitHub Pages.

## Global Constraints

- Destination repository: `/home/npatta01/data/search-agent-study-group`.
- Source repository: `/home/npatta01/.codex/worktrees/595d/adk_agent` at commit `614c5a8`.
- Python requirement: `>=3.12,<3.13`; do not pin the patch version.
- Keep all participant, instructor, exercise, and solution notebooks together under `weeks/2026-08-11/notebooks/`.
- Do not add package-install cells to notebooks.
- Copy generated source notebooks, not executed copies.
- The deck must be one offline standalone HTML file under `presentations/`.
- Never copy `.env`, credentials, private attachment paths, temporary environments, caches, or raw debug outputs.
- Preserve generic ecommerce tool names `search_products` and `product_details`.

---

### Task 1: Add a bundle contract validator

**Files:**
- Create: `scripts/validate_2026_08_11_workshop.py`

**Interfaces:**
- Consumes: the exact destination manifest from the approved design.
- Produces: `main() -> int`, returning zero only when the deck and notebook bundle are portable and safe.

- [ ] **Step 1: Create a failing manifest validator**

Implement a dependency-light validator using `json`, `base64`, `hashlib`, `pathlib`, and `re`. It must assert the presence of:

```python
EXPECTED_NOTEBOOKS = (
    "05_mcp_under_the_hood_instructor.ipynb",
    "05_orders_mcp_skill_subagents_demo_phoenix.ipynb",
    "06_ecommerce_skills_vs_subagents_instructor_phoenix.ipynb",
    "07_product_mcp_skill_takehome_exercise_phoenix.ipynb",
    "07_product_mcp_skill_takehome_solution_phoenix.ipynb",
    "08_ecommerce_composition_takehome_exercise_phoenix.ipynb",
)

EXPECTED_SUPPORT = (
    ".env.example",
    "materials.md",
    "notebooks/.python-version",
    "notebooks/requirements.txt",
    "notebooks/mcp_workshop/__init__.py",
    "notebooks/mcp_workshop/workshop_helpers.py",
    "notebooks/orders_workshop/__init__.py",
    "notebooks/orders_workshop/tools_order.py",
    "notebooks/orders_workshop/tools_store.py",
    "notebooks/product_takehome/product-shopping-code/SKILL.md",
    "skills/order-support/SKILL.md",
    "skills/product-shopping-mcp/SKILL.md",
    "skills/store-information/SKILL.md",
)
```

The validator must also check:

- every notebook is valid notebook JSON with `nbformat == 4`;
- every source code cell has `execution_count is None` and no outputs;
- every embedded attachment decodes as non-empty data;
- the six notebook filenames occur once each and no extra `.ipynb` is present;
- helper source contains no private absolute path;
- the deck contains its JavaScript and CSS inline and has no local asset references;
- no added text file contains `.codex/attachments`, `/home/npatta01`, `Event(model_version=`, `search_walmart_products`, `get_walmart_product`, or common API-key patterns.

- [ ] **Step 2: Run the validator and confirm it fails for missing artifacts**

Run:

```bash
python3 scripts/validate_2026_08_11_workshop.py
```

Expected: non-zero with a concise missing-file list for the August 11 bundle.

- [ ] **Step 3: Commit the red contract**

```bash
git add scripts/validate_2026_08_11_workshop.py
git commit -m "test: define August 11 workshop bundle contract"
```

---

### Task 2: Package the standalone deck

**Files:**
- Create: `presentations/mcp-skills-subagents-intro.html`
- Modify: `README.md`

**Interfaces:**
- Consumes: source `presentations/mcp-skills-subagents-intro/mcp-skills-subagents-intro.html` at commit `614c5a8`.
- Produces: a single-file offline deck linked from the repository presentation index.

- [ ] **Step 1: Copy the generated standalone artifact byte-for-byte**

Copy only the generated HTML artifact to:

```text
presentations/mcp-skills-subagents-intro.html
```

Do not copy the React/Vite source project, `node_modules`, build scripts, or deck tests.

- [ ] **Step 2: Add the deck to the README presentation list**

Add:

```markdown
- [MCP, Skills, and Subagents](presentations/mcp-skills-subagents-intro.html)
```

- [ ] **Step 3: Verify the standalone artifact**

Run the repository validator and a local HTTP check:

```bash
python3 scripts/validate_2026_08_11_workshop.py
python3 -m http.server 8765
curl -fsS http://127.0.0.1:8765/presentations/mcp-skills-subagents-intro.html >/dev/null
```

Expected: the validator now reports only missing weekly files; HTTP returns 200.

- [ ] **Step 4: Commit the deck**

```bash
git add README.md presentations/mcp-skills-subagents-intro.html
git commit -m "docs: add standalone MCP workshop deck"
```

---

### Task 3: Package notebooks, helpers, Skills, and setup docs

**Files:**
- Create: `weeks/2026-08-11/.env.example`
- Create: `weeks/2026-08-11/materials.md`
- Create: all files under the approved `weeks/2026-08-11/notebooks/` and `weeks/2026-08-11/skills/` manifest.

**Interfaces:**
- Consumes: generated notebooks, runtime helpers, requirements, Python version, and Skill Markdown from source commit `614c5a8`.
- Produces: a dated bundle runnable with notebook working directory `weeks/2026-08-11/notebooks/`.

- [ ] **Step 1: Copy the six source notebooks and runtime support files**

Copy the exact files listed by `EXPECTED_NOTEBOOKS` and `EXPECTED_SUPPORT`. Preserve these package boundaries:

```text
notebooks/mcp_workshop/
notebooks/orders_workshop/
notebooks/product_takehome/product-shopping-code/
skills/order-support/
skills/product-shopping-mcp/
skills/store-information/
```

- [ ] **Step 2: Add the safe environment template**

Create `weeks/2026-08-11/.env.example` containing names and safe defaults only:

```dotenv
GOOGLE_API_KEY=
GOOGLE_MODEL=gemini-3.1-flash-lite
PHOENIX_API_KEY=
PHOENIX_COLLECTOR_ENDPOINT=https://app.phoenix.arize.com/s/adk-demo-search
```

- [ ] **Step 3: Write the learner-facing materials guide**

`materials.md` must include:

- Python 3.12 and hosted-Jupyter assumptions;
- `python -m pip install -r notebooks/requirements.txt` as the environment setup command outside notebooks;
- copying `.env.example` to `.env` and filling only the required keys;
- the public ecommerce MCP endpoint dependency;
- the recommended live order: under-the-hood, Orders demo, architecture comparison;
- the product exercise/solution and ecommerce composition take-home sequence;
- Phoenix trace expectations and cleanup guidance;
- source provenance: `npatta01/adk-agent` commit `614c5a8`;
- a note that exercises intentionally contain learner-owned prompts/agent wiring while the reference notebooks are complete.

- [ ] **Step 4: Run the static bundle contract**

```bash
python3 scripts/validate_2026_08_11_workshop.py
```

Expected: PASS.

- [ ] **Step 5: Commit the weekly bundle**

```bash
git add weeks/2026-08-11
git commit -m "docs: add August 11 MCP workshop notebooks"
```

---

### Task 4: Verify Python 3.12 portability and notebook execution

**Files:**
- Modify only when verification exposes a destination-layout defect: files under `weeks/2026-08-11/`.

**Interfaces:**
- Consumes: the packaged bundle and the existing project-level runtime `.env` without printing or copying its values.
- Produces: executed temporary notebook copies and a clean verification report in the PR body; no executed notebooks are committed.

- [ ] **Step 1: Create a disposable Python 3.12 environment**

```bash
VERIFY_ENV=$(mktemp -d /tmp/search-agent-study-group-2026-08-11-XXXXXX)
uv venv --python 3.12 "$VERIFY_ENV"
uv pip install --python "$VERIFY_ENV/bin/python" \
  -r weeks/2026-08-11/notebooks/requirements.txt \
  jupyter nbclient ipykernel pytest
"$VERIFY_ENV/bin/python" -m ipykernel install \
  --prefix "$VERIFY_ENV" --name study-group-2026-08-11
export JUPYTER_PATH="$VERIFY_ENV/share/jupyter"
```

- [ ] **Step 2: Verify helper imports from the destination layout**

From `weeks/2026-08-11/notebooks/`, import:

```python
from mcp_workshop.workshop_helpers import MCP_ENDPOINT, repository_root
from orders_workshop.tools_order import list_orders
from orders_workshop.tools_store import get_store_hours
```

Assert `repository_root.name == "2026-08-11"` and all four Skill files resolve from their expected destinations.

- [ ] **Step 3: Execute the four completed notebooks into a temporary directory**

Use `nbclient.NotebookClient` with timeout 900 seconds, kernel `study-group-2026-08-11`, and resources path `weeks/2026-08-11/notebooks/`. Load environment variables only into the execution process from `/home/npatta01/data/presentation/adk_agent/.env`. Write executed copies under `/tmp`, never into the repository.

Execute these notebooks top-to-bottom:

```text
05_mcp_under_the_hood_instructor.ipynb
05_orders_mcp_skill_subagents_demo_phoenix.ipynb
06_ecommerce_skills_vs_subagents_instructor_phoenix.ipynb
07_product_mcp_skill_takehome_solution_phoenix.ipynb
```

Expected:

- zero error outputs;
- completed demos show Order MCP, MCP Code, Skill, and subagent behavior;
- solution/reference notebooks produce grounded results;
- Phoenix flush and cleanup cells execute.

- [ ] **Step 4: Validate participant exercise checkpoints**

Execute each participant exercise only through its first `YOUR TURN` assertion:

```text
07_product_mcp_skill_takehome_exercise_phoenix.ipynb
08_ecommerce_composition_takehome_exercise_phoenix.ipynb
```

Expected: setup cells and helper imports pass, then execution stops on the notebook's explicit learner-owned assertion. Any import, missing-file, connection, credential-loading, or package error is a failure.

- [ ] **Step 5: Run browser checks for the deck**

Open the deck through local HTTP and directly from disk. Verify:

- 17 slides;
- keyboard previous/next navigation;
- no overlapping title rule at a 1366×768 viewport;
- no console errors;
- no network request for a local image, stylesheet, or script.

- [ ] **Step 6: Run final safety and diff checks**

```bash
python3 scripts/validate_2026_08_11_workshop.py
git diff --check
git status --short
```

Scan the added files against the actual non-empty `.env` values of length eight or greater, reporting only pass/fail and never printing values.

- [ ] **Step 7: Commit any portability fix**

If verification required a fix, stage only affected August 11 files and commit:

```bash
git commit -m "fix: make August 11 workshop bundle portable"
```

If no source change was required, do not create an empty commit.

---

### Task 5: Publish the draft pull request

**Files:**
- No new source files; consume the verified branch.

**Interfaces:**
- Consumes: clean intended branch commits.
- Produces: a draft PR from `codex/2026-08-11-mcp-workshop` to `main`.

- [ ] **Step 1: Review exact PR scope**

```bash
git status -sb
git diff --stat origin/main...HEAD
git diff --name-status origin/main...HEAD
```

Expected: only the design/plan, validator, standalone presentation, README link, and August 11 bundle.

- [ ] **Step 2: Push the branch**

```bash
git push -u origin codex/2026-08-11-mcp-workshop
```

- [ ] **Step 3: Open a draft PR into `main`**

Use title:

```text
Add August 11 MCP workshop materials
```

The PR body must summarize the standalone deck, six notebooks, runtime helpers and Skills, Python 3.12 setup, source provenance, notebook execution result, deck browser result, and safety scan.

- [ ] **Step 4: Confirm the remote head**

```bash
LOCAL_HEAD=$(git rev-parse HEAD)
REMOTE_HEAD=$(git ls-remote origin refs/heads/codex/2026-08-11-mcp-workshop | cut -f1)
test "$LOCAL_HEAD" = "$REMOTE_HEAD"
gh pr view --json url,state,isDraft,baseRefName,headRefName,headRefOid
```

Expected: open draft PR, base `main`, head branch `codex/2026-08-11-mcp-workshop`, and `headRefOid` equal to local `HEAD`.
