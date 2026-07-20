#!/usr/bin/env python3
"""Validate glossary Markdown sources and build glossary/terms.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
TERMS_DIR = ROOT / "glossary" / "terms"
OUTPUT_PATH = ROOT / "glossary" / "terms.json"

REQUIRED_METADATA = (
    "id",
    "term",
    "aliases",
    "category",
    "status",
    "last_reviewed",
    "relations",
    "sources",
)
OPTIONAL_METADATA = ("introduced_in",)
REQUIRED_SECTIONS = (
    "Simple definition",
    "Working definition",
    "Why it matters",
    "Example",
    "Common confusion",
)
ALL_SECTIONS = REQUIRED_SECTIONS + ("Study-group notes",)
ALLOWED_STATUSES = {"draft", "published", "needs-review", "deprecated"}
ALLOWED_RELATION_TYPES = {
    "broader",
    "narrower",
    "related",
    "uses",
    "contrasts_with",
    "evaluated_by",
}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KEY_PATTERN = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$")
HEADING_PATTERN = re.compile(r"^##\s+(.+?)\s*$")


@dataclass
class GlossaryError(Exception):
    path: Path
    message: str

    def __str__(self) -> str:
        try:
            display_path = self.path.relative_to(ROOT)
        except ValueError:
            display_path = self.path
        return f"{display_path}: {self.message}"


def parse_frontmatter(path: Path, text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise GlossaryError(path, "frontmatter must start with '---' on the first line")

    try:
        closing_index = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration as exc:
        raise GlossaryError(path, "frontmatter is missing its closing '---'") from exc

    frontmatter_lines = lines[1:closing_index]
    metadata: dict[str, Any] = {}
    index = 0
    while index < len(frontmatter_lines):
        raw_line = frontmatter_lines[index]
        if not raw_line.strip():
            index += 1
            continue
        match = KEY_PATTERN.match(raw_line)
        if not match:
            raise GlossaryError(
                path,
                f"frontmatter line {index + 2} must use 'key: value' syntax",
            )
        key, raw_value = match.groups()
        if key in metadata:
            raise GlossaryError(path, f"frontmatter key '{key}' appears more than once")
        value = (raw_value or "").strip()
        if not value:
            raise GlossaryError(path, f"frontmatter key '{key}' has an empty value")

        if value[0] in "[{":
            json_lines = [value]
            while True:
                candidate = "\n".join(json_lines)
                try:
                    metadata[key] = json.loads(candidate)
                    break
                except json.JSONDecodeError as exc:
                    index += 1
                    if index >= len(frontmatter_lines):
                        raise GlossaryError(
                            path,
                            f"frontmatter key '{key}' has invalid JSON-compatible syntax: {exc.msg}",
                        ) from exc
                    json_lines.append(frontmatter_lines[index])
        else:
            metadata[key] = value
        index += 1

    body = "\n".join(lines[closing_index + 1 :]).strip("\n")
    return metadata, body


def parse_sections(path: Path, body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        match = HEADING_PATTERN.match(line)
        if match:
            heading = match.group(1).strip()
            current = heading
            if heading in sections:
                raise GlossaryError(path, f"section '## {heading}' appears more than once")
            sections[heading] = []
        elif current is not None:
            sections[current].append(line)

    missing = [heading for heading in ALL_SECTIONS if heading not in sections]
    if missing:
        raise GlossaryError(path, "missing section(s): " + ", ".join(f"## {item}" for item in missing))

    parsed = {heading: "\n".join(lines).strip() for heading, lines in sections.items()}
    for heading in REQUIRED_SECTIONS:
        if not parsed[heading]:
            raise GlossaryError(path, f"section '## {heading}' must not be empty")
    simple_definition = parsed["Simple definition"]
    if "\n" in simple_definition or len(simple_definition) > 180:
        raise GlossaryError(
            path,
            "section '## Simple definition' must be one short line (180 characters or fewer)",
        )
    return parsed


def require_string(path: Path, metadata: dict[str, Any], key: str) -> str:
    value = metadata.get(key)
    if not isinstance(value, str) or not value.strip():
        raise GlossaryError(path, f"metadata '{key}' must be a nonempty scalar string")
    return value.strip()


def validate_record(path: Path, metadata: dict[str, Any], sections: dict[str, str]) -> dict[str, Any]:
    missing = [key for key in REQUIRED_METADATA if key not in metadata]
    if missing:
        raise GlossaryError(path, "missing metadata field(s): " + ", ".join(missing))
    extra = sorted(set(metadata) - set(REQUIRED_METADATA) - set(OPTIONAL_METADATA))
    if extra:
        raise GlossaryError(path, "unsupported metadata field(s): " + ", ".join(extra))

    term_id = require_string(path, metadata, "id")
    if not ID_PATTERN.fullmatch(term_id):
        raise GlossaryError(path, "metadata 'id' must use lowercase letters, numbers, and hyphens")
    term = require_string(path, metadata, "term")
    category = require_string(path, metadata, "category")
    if not ID_PATTERN.fullmatch(category):
        raise GlossaryError(path, "metadata 'category' must use lowercase letters, numbers, and hyphens")
    status = require_string(path, metadata, "status")
    if status not in ALLOWED_STATUSES:
        raise GlossaryError(path, f"metadata 'status' must be one of: {', '.join(sorted(ALLOWED_STATUSES))}")
    introduced_in = (
        require_string(path, metadata, "introduced_in")
        if "introduced_in" in metadata
        else None
    )
    last_reviewed = require_string(path, metadata, "last_reviewed")
    if not DATE_PATTERN.fullmatch(last_reviewed):
        raise GlossaryError(path, "metadata 'last_reviewed' must use YYYY-MM-DD")
    try:
        date.fromisoformat(last_reviewed)
    except ValueError as exc:
        raise GlossaryError(path, "metadata 'last_reviewed' must be a real calendar date") from exc

    aliases = metadata["aliases"]
    if not isinstance(aliases, list) or not all(isinstance(item, str) and item.strip() for item in aliases):
        raise GlossaryError(path, "metadata 'aliases' must be a JSON array of nonempty strings")
    normalized_aliases = [item.strip().casefold() for item in aliases]
    if len(normalized_aliases) != len(set(normalized_aliases)):
        raise GlossaryError(path, "metadata 'aliases' contains a duplicate (comparison is case-insensitive)")

    relations = metadata["relations"]
    if not isinstance(relations, list):
        raise GlossaryError(path, "metadata 'relations' must be a JSON array")
    normalized_relations: set[tuple[str, str]] = set()
    clean_relations: list[dict[str, str]] = []
    for position, relation in enumerate(relations, start=1):
        if not isinstance(relation, dict) or set(relation) != {"type", "target"}:
            raise GlossaryError(path, f"relation {position} must contain only 'type' and 'target'")
        relation_type = relation.get("type")
        target = relation.get("target")
        if not isinstance(relation_type, str) or relation_type not in ALLOWED_RELATION_TYPES:
            raise GlossaryError(path, f"relation {position} has an unsupported type")
        if not isinstance(target, str) or not ID_PATTERN.fullmatch(target):
            raise GlossaryError(path, f"relation {position} target must be a valid glossary id")
        signature = (relation_type, target)
        if signature in normalized_relations:
            raise GlossaryError(path, f"relation {position} duplicates '{relation_type}: {target}'")
        normalized_relations.add(signature)
        clean_relations.append({"type": relation_type, "target": target})

    sources = metadata["sources"]
    if not isinstance(sources, list) or not sources:
        raise GlossaryError(path, "metadata 'sources' must be a nonempty JSON array")
    clean_sources: list[dict[str, str]] = []
    source_urls: set[str] = set()
    for position, source in enumerate(sources, start=1):
        if not isinstance(source, dict) or set(source) != {"title", "url", "note"}:
            raise GlossaryError(path, f"source {position} must contain only 'title', 'url', and 'note'")
        title = source.get("title")
        url = source.get("url")
        note = source.get("note")
        if not all(isinstance(item, str) and item.strip() for item in (title, url, note)):
            raise GlossaryError(path, f"source {position} fields must be nonempty strings")
        parsed_url = urlparse(url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise GlossaryError(path, f"source {position} URL must use HTTP or HTTPS")
        if url in source_urls:
            raise GlossaryError(path, f"source {position} duplicates URL '{url}'")
        source_urls.add(url)
        clean_sources.append({"title": title.strip(), "url": url.strip(), "note": note.strip()})

    record = {
        "id": term_id,
        "term": term,
        "aliases": [item.strip() for item in aliases],
        "category": category,
        "status": status,
        "last_reviewed": last_reviewed,
        "relations": sorted(clean_relations, key=lambda item: (item["type"], item["target"])),
        "sources": clean_sources,
        "sections": {heading: sections[heading] for heading in ALL_SECTIONS},
    }
    if introduced_in is not None:
        record["introduced_in"] = introduced_in
    return record


def build_payload() -> dict[str, Any]:
    paths = sorted(TERMS_DIR.glob("*.md"))
    if not paths:
        raise GlossaryError(TERMS_DIR, "no Markdown term files found")

    records: list[tuple[Path, dict[str, Any]]] = []
    errors: list[GlossaryError] = []
    for path in paths:
        try:
            metadata, body = parse_frontmatter(path, path.read_text(encoding="utf-8"))
            sections = parse_sections(path, body)
            records.append((path, validate_record(path, metadata, sections)))
        except (GlossaryError, OSError) as exc:
            errors.append(exc if isinstance(exc, GlossaryError) else GlossaryError(path, str(exc)))

    ids: dict[str, Path] = {}
    for path, record in records:
        term_id = record["id"]
        if term_id in ids:
            errors.append(GlossaryError(path, f"id '{term_id}' is already used by {ids[term_id].name}"))
        ids[term_id] = path

    known_ids = {record["id"] for _, record in records}
    for path, record in records:
        for relation in record["relations"]:
            if relation["target"] not in known_ids:
                errors.append(GlossaryError(path, f"relation target '{relation['target']}' does not exist"))
            if relation["target"] == record["id"]:
                errors.append(GlossaryError(path, "a relation cannot target its own term"))

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)

    return {
        "schema_version": 1,
        "generated_from": "glossary/terms/*.md",
        "terms": sorted((record for _, record in records), key=lambda record: record["id"]),
    }


def serialize(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate sources and verify that glossary/terms.json is current without rewriting it",
    )
    args = parser.parse_args()

    payload = build_payload()
    expected = serialize(payload)
    if args.check:
        try:
            current = OUTPUT_PATH.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"error: {OUTPUT_PATH.relative_to(ROOT)} does not exist; run the builder", file=sys.stderr)
            return 1
        if current != expected:
            print(
                f"error: {OUTPUT_PATH.relative_to(ROOT)} is out of date; run "
                "python3 scripts/build_glossary.py",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {len(payload['terms'])} terms valid; {OUTPUT_PATH.relative_to(ROOT)} is current")
        return 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(expected, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} with {len(payload['terms'])} valid terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
