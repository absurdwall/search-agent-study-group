#!/usr/bin/env python3
"""Compatibility entry point for the published glossary's canonical builder.

Keep the repository's existing command while using the builder shipped with the
current glossary. Command-line arguments, including --check, are forwarded.
"""
from pathlib import Path
import runpy


if __name__ == "__main__":
    runpy.run_path(
        str(Path(__file__).resolve().parents[1] / "glossary" / "build_glossary.py"),
        run_name="__main__",
    )
