# Agent Concepts Glossary

The Markdown files in `terms/` are the human-edited source of truth. Do not edit
`terms.json` by hand; generate it from the repository root:

```sh
python3 scripts/build_glossary.py
python3 scripts/build_glossary.py --check
```

The first command validates every term and writes deterministic JSON. The
second validates the Markdown and exits nonzero when the existing JSON differs
from what the sources would generate.

## Supported frontmatter subset

Frontmatter is delimited by `---`. This project intentionally supports only a
small YAML-compatible subset:

- Each field starts at the beginning of a line as `key: value`.
- Scalar values are unquoted text on the same line, such as `status: published`.
- Arrays and objects use valid JSON flow syntax. They may span multiple lines.
- JSON strings and object keys must use double quotes. JSON trailing commas and
  comments are not supported.
- Blank lines are allowed between fields. YAML block lists, anchors, tags,
  folded strings, implicit types, and other general YAML features are not.
- Only the documented metadata fields are accepted, so typos fail validation.

Required metadata fields are `id`, `term`, `aliases`, `category`, `status`,
`last_reviewed`, `relations`, and `sources`. `introduced_in` is optional; add it
only when a term has been covered in a study-group week.

Allowed statuses are `draft`, `published`, `needs-review`, and `deprecated`.
Allowed relationship types are `broader`, `narrower`, `related`, `uses`,
`contrasts_with`, and `evaluated_by`.

Each source must have `title`, an HTTP(S) `url`, and a nonempty `note` explaining
what the source supports. Each relation must have exactly `type` and `target`.

## Required Markdown sections

Each term uses exact level-two headings for:

- `Simple definition`
- `Working definition`
- `Why it matters`
- `Example`
- `Common confusion`
- `Study-group notes`

The first five sections must contain text. `Simple definition` must be one
short, beginner-friendly line of at most 180 characters, used by the glossary
card preview.
`Study-group notes` may be empty, but
its heading remains so the term can accumulate group-specific context later.
