# ChatGPT Site version 14 source synchronization

## Provenance and scope

- Source: [current ChatGPT Site](https://search-agent-study-group.absurdgreaterfool.chatgpt.site/), saved/published version **14**.
- Exact saved source commit: `19b9695c0f937ed7e8206b859f30c8a7a386a563`.
- Target: `tykswtr/search-agent-study-group-backup`, default branch `main`, observed base `d7e444e9babc06b2bb970eafc1b2b38d947bcea4`.
- Retrieved from the saved Git source, not reconstructed from rendered HTML. The source manifest declares `dist/` as its static directory; the existing GitHub Pages site publishes from the repository root.
- Map all 144 static files from `dist/<path>` to `<path>`. Before portability adjustments, 84 already matched, 34 differed, and 26 were new. Copy only additions/changes; delete no repository files.

This imports the current Chapter 5 teaching content, its stylesheet and interaction script, the three long-running/multi-agent Extended Reading resources, navigation/sidebar consistency changes across the book, and the refreshed 44-term glossary (42 current terms plus two earlier entries available through search/deep links). Existing images, source notices, other assets, notebooks, weekly pages, and legacy routes are retained. No separate Chapter 5 demo Skill, hook handler, harness, runtime evidence, or demo implementation was added.

## Deliberate hosting adaptations

1. Keep the existing repository-root publishing layout and `.nojekyll`; do not add a duplicate `dist/` tree.
2. Rebase 52 first-party chapter-link occurrences in glossary Markdown from the ChatGPT Site origin to `https://tykswtr.github.io/search-agent-study-group-backup`, then regenerate `glossary/terms.json`. External references and glossary wording are unchanged. The untouched saved-source export in the handoff preserves the original URLs.
3. Update the glossary README’s build commands for its root-relative location. Keep `glossary/build_glossary.py` as the canonical imported builder; preserve `scripts/build_glossary.py` as a compatibility entry point so old commands do not overwrite the current index with a different serialization.
4. Do not copy Site identity, hosting configuration, credentials, local caches, or working directories into this repository. ChatGPT’s access controls, version history, and private hosting are platform services, not part of this static tree. No Sites Worker, MCP connection, database binding, or connected-app runtime is required by the saved static source.

The Chapter 5 HTML/CSS/JavaScript is byte-identical to the saved source. Other Site-owned files also match, apart from the documented glossary path/URL adaptations and its regenerated index. Repository-only teaching/project/service files are retained.

## Validation

Completed locally, before the handoff:

- Every imported file accounted for by source and repository SHA-256 manifests.
- 27 published HTML pages; 569 local references checked under the GitHub project base path, including fragment targets, assets, glossary chapter citations, and ARIA targets. No missing targets or project-prefix escapes.
- Both glossary builder entry points pass `--check`; all standalone JavaScript and inline executable scripts parse, and JSON/notebook files decode.
- Chapter 5: Codex/Claude tabs and keyboard state logic; three Guardrails states; four artifact states; repeated selections; fragment/disclosure reveal; same-fragment reopening; print-state restoration; no-JavaScript reference fallback.
- Glossary: data loading, search, empty results, category filters, progressive expansion, and preserved earlier-term deep links.
- Imported payload and intended diff scanned for high-confidence credential patterns and accidental local-only files; none found. This is a bounded check, not a claim of exhaustive secret detection.
- Existing GitHub Pages homepage returned HTTP 200. No branch was deployed for this review.

Interaction checks use a DOM simulation. Actual desktop/mobile rendering, native focus/keyboard behavior, accessibility assistive technology, print layout, and screenshots were not verified because managed browser preview is unavailable. No real agent evals, model calls, or demos were run.

## External dependency requiring review

“Ask Spooky” calls `https://spooky-api-jcysmpnqda-ue.a.run.app/v1/chat`. A read-only OPTIONS preflight for POST with Content-Type returned **400 / Disallowed CORS origin** and no Access-Control-Allow-Origin for both `https://tykswtr.github.io` and the current ChatGPT Site origin. This is an observed existing backend configuration issue, not a missing static asset. The chat service and its model/provider availability are not reproduced by GitHub Pages; no chat request was made. Backend ownership and the correct origin allowlist need separate review. The frontend and unrelated repository services are unchanged.

External canonical reading links remain external; they were not exhaustively live-checked. Hosting access/settings, the live chat path, and native browser layout remain acceptance checks after the PR is opened. Do not merge automatically.
