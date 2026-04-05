"""Tests for validator module."""

from __future__ import annotations

from pathlib import Path

from lib.models import AtlasFile, AtlasType, ErrorCode
from lib.parser import Parser
from lib.validator import Validator


class TestValidator:
    def test_validate_valid_atlases(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
            AtlasFile(path=tmp_repo / ".overview.md", atlas_type=AtlasType.OVERVIEW),
        ]
        atlases = parser.parse_batch(atlases)

        validator = Validator()
        result = validator.validate(atlases)

        assert all(a.is_valid for a in result.atlases)

    def test_validate_missing_required_fields(self, tmp_repo_with_invalid: Path) -> None:
        parser = Parser()
        atlas = AtlasFile(
            path=tmp_repo_with_invalid / ".abstract.md",
            atlas_type=AtlasType.ABSTRACT,
        )
        parser.parse(atlas)

        validator = Validator()
        validator.validate([atlas])

        assert not atlas.is_valid
        assert any("layer" in e.lower() or "scope" in e.lower() for e in atlas.validation_errors)

    def test_validate_parent_refs_broken(self, tmp_path: Path) -> None:
        child_dir = tmp_path / "child"
        child_dir.mkdir()

        (child_dir / ".abstract.md").write_text(
            """---
type: atlas
layer: l1
corpus: code
scope: sub
root: test
parent: nonexistent
date_updated: 2026-03-21
---
# Abstract
"""
        )

        parser = Parser()
        atlas = AtlasFile(path=child_dir / ".abstract.md", atlas_type=AtlasType.ABSTRACT)
        parser.parse(atlas)

        validator = Validator()
        result = validator.validate([atlas])

        assert any(e.code == ErrorCode.E006 for e in result.errors)

    def test_validate_parent_refs_valid(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
            AtlasFile(path=tmp_repo / "subdir" / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        validator = Validator()
        result = validator.validate(atlases)

        broken_refs = [e for e in result.errors if e.code == ErrorCode.E006]
        assert len(broken_refs) == 0

    def test_empty_atlas_list(self) -> None:
        validator = Validator()
        result = validator.validate([])

        assert result.atlases == []
        assert result.errors == []

    def test_validate_date_format(self, tmp_path: Path) -> None:
        file_path = tmp_path / ".abstract.md"
        file_path.write_text(
            """---
type: atlas
layer: l0
corpus: mixed
scope: top
root: test
date_updated: invalid-date
---
# Abstract
"""
        )

        parser = Parser()
        atlas = AtlasFile(path=file_path, atlas_type=AtlasType.ABSTRACT)
        parser.parse(atlas)

        validator = Validator()
        validator.validate_date_consistency([atlas], [])

        assert any("date" in e.lower() for e in atlas.validation_errors)
