"""Tests for parser module."""

from __future__ import annotations

from pathlib import Path

from lib.models import AtlasFile, AtlasType
from lib.parser import Parser


class TestParser:
    def test_parse_valid_frontmatter(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlas = AtlasFile(
            path=tmp_repo / ".abstract.md",
            atlas_type=AtlasType.ABSTRACT,
        )
        result = parser.parse(atlas)

        assert result.frontmatter != {}
        assert result.frontmatter.get("type") == "atlas"
        assert result.frontmatter.get("layer") == "l0"
        assert result.content != ""

    def test_parse_missing_frontmatter(self, tmp_path: Path) -> None:
        file_path = tmp_path / "no_frontmatter.md"
        file_path.write_text("# Just content\nNo frontmatter here.")

        parser = Parser()
        atlas = AtlasFile(path=file_path, atlas_type=AtlasType.ABSTRACT)
        result = parser.parse(atlas)

        assert "Missing or invalid YAML frontmatter" in result.validation_errors

    def test_parse_invalid_yaml(self, tmp_path: Path) -> None:
        file_path = tmp_path / "invalid.md"
        file_path.write_text(
            """---
invalid: yaml: syntax:
---
# Content
"""
        )

        parser = Parser()
        atlas = AtlasFile(path=file_path, atlas_type=AtlasType.ABSTRACT)
        result = parser.parse(atlas)

        assert len(result.validation_errors) > 0

    def test_parse_bom_handling(self, tmp_path: Path) -> None:
        file_path = tmp_path / "bom.md"
        content = "---\ntype: atlas\n---\nContent"
        file_path.write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))

        parser = Parser()
        atlas = AtlasFile(path=file_path, atlas_type=AtlasType.ABSTRACT)
        result = parser.parse(atlas)

        assert result.frontmatter.get("type") == "atlas"

    def test_parse_empty_frontmatter(self, tmp_path: Path) -> None:
        file_path = tmp_path / "empty.md"
        file_path.write_text(
            """---
---
# Content
"""
        )

        parser = Parser()
        atlas = AtlasFile(path=file_path, atlas_type=AtlasType.ABSTRACT)
        result = parser.parse(atlas)

        assert result.frontmatter == {} or result.frontmatter is None

    def test_parse_batch(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
            AtlasFile(path=tmp_repo / ".overview.md", atlas_type=AtlasType.OVERVIEW),
        ]

        results = parser.parse_batch(atlases)

        assert len(results) == 2
        for r in results:
            assert r.frontmatter != {}

    def test_validate_required_fields(self, tmp_path: Path) -> None:
        file_path = tmp_path / "missing.md"
        file_path.write_text(
            """---
type: atlas
---
# Content
"""
        )

        parser = Parser()
        atlas = AtlasFile(path=file_path, atlas_type=AtlasType.ABSTRACT)
        parser.parse(atlas)

        errors = Parser.validate_frontmatter_fields(atlas)

        assert any("layer" in e for e in errors)
        assert any("corpus" in e for e in errors)

    def test_validate_layer_format(self, tmp_path: Path) -> None:
        file_path = tmp_path / "bad_layer.md"
        file_path.write_text(
            """---
type: atlas
layer: invalid
corpus: mixed
scope: top
root: test
---
# Content
"""
        )

        parser = Parser()
        atlas = AtlasFile(path=file_path, atlas_type=AtlasType.ABSTRACT)
        parser.parse(atlas)

        errors = Parser.validate_frontmatter_fields(atlas)

        assert any("Invalid layer format" in e for e in errors)

    def test_parse_preserves_content(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlas = AtlasFile(
            path=tmp_repo / ".abstract.md",
            atlas_type=AtlasType.ABSTRACT,
        )
        result = parser.parse(atlas)

        assert "# Abstract" in result.content or "Abstract" in result.content
