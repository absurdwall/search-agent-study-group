"""Portable environment-file discovery for hosted Jupyter notebooks."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv


def env_file_candidates(
    *,
    repository_root: Path,
    cwd: Path | None = None,
    home: Path | None = None,
) -> tuple[Path, ...]:
    """Return ordered `.env` locations used by the workshop."""

    working_directory = (cwd or Path.cwd()).resolve()
    root = repository_root.resolve()
    home_directory = (home or Path.home()).resolve()

    candidates = [
        working_directory / ".env",
        *(parent / ".env" for parent in working_directory.parents),
        root / "notebooks" / ".env",
        root / ".env",
        *(parent / ".env" for parent in root.parents),
        home_directory / "search-agent-study-group" / ".env",
    ]

    unique_candidates: list[Path] = []
    for candidate in candidates:
        if candidate not in unique_candidates:
            unique_candidates.append(candidate)
    return tuple(unique_candidates)


def load_workshop_env(*, repository_root: Path) -> Path | None:
    """Load the first workshop `.env` file found without replacing kernel values."""

    for candidate in env_file_candidates(repository_root=repository_root):
        if candidate.is_file():
            load_dotenv(candidate, override=False)
            return candidate
    return None
