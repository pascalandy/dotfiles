"""Shared fixtures for abstract_gen tests."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.models import AtlasFile, AtlasType


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "test_repo"
    repo.mkdir()

    root_dir = repo
    (root_dir / ".abstract.md").write_text(
        """---
type: atlas
layer: l0
corpus: mixed
scope: top
root: test_repo
parent:
date_updated: 2026-03-21
---
# Abstract
Root abstract.
"""
    )
    (root_dir / ".overview.md").write_text(
        """---
type: atlas
layer: l0
corpus: mixed
scope: top
root: test_repo
parent:
date_updated: 2026-03-21
---
# Overview
Root overview.
"""
    )

    subdir = repo / "subdir"
    subdir.mkdir()
    (subdir / ".abstract.md").write_text(
        """---
type: atlas
layer: l1
corpus: code
scope: sub
root: test_repo
parent: test_repo
date_updated: 2026-03-21
---
# Abstract
Subdir abstract.
"""
    )

    return repo


@pytest.fixture
def tmp_repo_with_invalid(tmp_path: Path) -> Path:
    repo = tmp_path / "invalid_repo"
    repo.mkdir()

    (repo / ".abstract.md").write_text(
        """---
type: atlas
layer: invalid_layer
corpus: mixed
date_updated: 2026-03-21
---
# Abstract
Missing required fields.
"""
    )

    return repo


@pytest.fixture
def tmp_repo_empty(tmp_path: Path) -> Path:
    repo = tmp_path / "empty_repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Empty repo")
    return repo


def make_atlas(
    path: Path,
    atlas_type: AtlasType = AtlasType.ABSTRACT,
    frontmatter: dict[str, Any] | None = None,
    content: str = "",
) -> AtlasFile:
    fm = frontmatter or {
        "type": "atlas",
        "layer": "l0",
        "corpus": "mixed",
        "scope": "top",
        "root": "test",
        "parent": None,
        "date_updated": "2026-03-21",
    }
    return AtlasFile(path=path, atlas_type=atlas_type, frontmatter=fm, content=content)
