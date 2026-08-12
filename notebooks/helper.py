"""Small bootstrap helpers for notebooks opened directly in JupyterLab."""

from __future__ import annotations

import sys
from pathlib import Path


def setup() -> Path:
    """Add the repository root to Python's import path and return it."""
    repository_root = Path(__file__).resolve().parent.parent
    root = str(repository_root)
    if root not in sys.path:
        sys.path.insert(0, root)
    return repository_root
