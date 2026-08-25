"""Friendly environment discovery for hosted and local workshop notebooks."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv


@dataclass(frozen=True)
class EnvironmentStatus:
    """The selected environment file and required workshop settings."""

    selected_path: Path | None
    missing: tuple[str, ...]
    values: dict[str, str]


class MissingWorkshopEnvironment(RuntimeError):
    """Raised with safe, actionable guidance when required settings are absent."""


def env_candidates(
    *,
    repository_root: Path,
    notebook_dir: Path | None = None,
    cwd: Path | None = None,
    home: Path | None = None,
    shared_env: Path = Path("/etc/skel/.env"),
) -> tuple[Path, ...]:
    """Return `.env` locations in the order used by workshop notebooks."""

    root = repository_root.resolve()
    working = (cwd or Path.cwd()).resolve()
    notebooks = (notebook_dir or root / "notebooks").resolve()
    home_dir = (home or Path.home()).resolve()
    candidates = [
        working / ".env",
        *(parent / ".env" for parent in working.parents),
        notebooks / ".env",
        root / ".env",
        *(parent / ".env" for parent in root.parents),
        home_dir / "search-agent-study-group" / ".env",
        shared_env,
    ]
    return tuple(dict.fromkeys(candidates))


def load_workshop_env(
    *,
    repository_root: Path,
    notebook_dir: Path | None = None,
    cwd: Path | None = None,
    home: Path | None = None,
    shared_env: Path = Path("/etc/skel/.env"),
    required: Iterable[str] = ("GOOGLE_API_KEY",),
) -> EnvironmentStatus:
    """Load the first available `.env` without replacing kernel settings."""

    candidates = env_candidates(
        repository_root=repository_root,
        notebook_dir=notebook_dir,
        cwd=cwd,
        home=home,
        shared_env=shared_env,
    )
    selected = next((path for path in candidates if path.is_file()), None)
    if selected is not None:
        load_dotenv(selected, override=False)

    names = tuple(required)
    values = {name: os.getenv(name, "").strip() for name in names}
    missing = tuple(name for name, value in values.items() if not value)
    status = EnvironmentStatus(selected, missing, values)
    if missing:
        checked = "\n".join(f"  - {path}" for path in candidates)
        raise MissingWorkshopEnvironment(
            "Almost ready! Add the missing setting(s) "
            f"{', '.join(missing)} to one of these `.env` files:\n{checked}"
        )
    return status
