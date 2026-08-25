"""Readable source, Skill, and comparison rendering for Jupyter."""

from __future__ import annotations

import inspect
import json
from collections.abc import Mapping, Sequence
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table


def source_text(function) -> str:
    """Return the real source for a teaching helper."""

    return inspect.getsource(function)


def show_source(function) -> None:
    """Display a helper's real Python source with syntax highlighting."""

    Console().print(Syntax(source_text(function), "python", line_numbers=False))


def skill_text(path: Path) -> str:
    """Return Skill instructions without YAML frontmatter."""

    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        _, separator, body = text[4:].partition("\n---\n")
        if separator:
            return body.lstrip()
    return text


def show_skill(path: Path) -> None:
    """Display a Skill as readable Markdown."""

    Console().print(Markdown(skill_text(path)))


def show_text(title: str, text: str) -> None:
    """Display a teaching prompt or instruction as a readable panel."""

    Console().print(Panel(text, title=title, border_style="cyan", expand=False))


def show_json(value: object) -> None:
    """Display nested teaching data as readable, indented JSON."""

    Console().print_json(json.dumps(value, default=str))


def show_comparison(rows: Sequence[Mapping[str, object]]) -> None:
    """Display run metrics as a compact comparison table."""

    if not rows:
        return
    columns = list(rows[0])
    table = Table(show_header=True, header_style="bold cyan")
    for column in columns:
        table.add_column(str(column))
    for row in rows:
        table.add_row(*(str(row.get(column, "")) for column in columns))
    Console().print(table)
