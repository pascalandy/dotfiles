"""Tests for tree_builder module."""

from __future__ import annotations

from pathlib import Path

from lib.models import AtlasFile, AtlasType
from lib.parser import Parser
from lib.tree_builder import TreeBuilder


class TestTreeBuilder:
    def test_build_tree_structure(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
            AtlasFile(path=tmp_repo / ".overview.md", atlas_type=AtlasType.OVERVIEW),
            AtlasFile(path=tmp_repo / "subdir" / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        builder = TreeBuilder()
        tree = builder.build(atlases)

        assert "roots" in tree
        assert "nodes" in tree
        assert len(tree["roots"]) >= 1

    def test_tree_has_children(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
            AtlasFile(path=tmp_repo / "subdir" / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        builder = TreeBuilder()
        tree = builder.build(atlases)

        root_node = tree["roots"][0]
        assert len(root_node["children"]) >= 1

    def test_tree_atlas_types(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
            AtlasFile(path=tmp_repo / ".overview.md", atlas_type=AtlasType.OVERVIEW),
        ]
        atlases = parser.parse_batch(atlases)

        builder = TreeBuilder()
        tree = builder.build(atlases)

        root_node = tree["roots"][0]
        assert "abstract" in root_node["atlases"]
        assert "overview" in root_node["atlases"]

    def test_build_ascii_tree(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
            AtlasFile(path=tmp_repo / "subdir" / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        builder = TreeBuilder()
        output = builder.build_ascii_tree(atlases)

        assert "└──" in output or "├──" in output
        assert tmp_repo.name in output

    def test_empty_atlases(self) -> None:
        builder = TreeBuilder()
        tree = builder.build([])

        assert tree["roots"] == []
        assert tree["nodes"] == {}

    def test_single_atlas(self, tmp_path: Path) -> None:
        file_path = tmp_path / ".abstract.md"
        file_path.write_text(
            """---
type: atlas
layer: l0
corpus: mixed
scope: top
root: test
---
# Abstract
"""
        )

        parser = Parser()
        atlas = AtlasFile(path=file_path, atlas_type=AtlasType.ABSTRACT)
        parser.parse(atlas)

        builder = TreeBuilder()
        tree = builder.build([atlas])

        assert len(tree["roots"]) == 1
        assert tree["roots"][0]["atlases"] == ["abstract"]

    def test_layer_inheritance(self, tmp_path: Path) -> None:
        file_path = tmp_path / ".abstract.md"
        file_path.write_text(
            """---
type: atlas
layer: l2
corpus: mixed
scope: sub
root: test
---
# Abstract
"""
        )

        parser = Parser()
        atlas = AtlasFile(path=file_path, atlas_type=AtlasType.ABSTRACT)
        parser.parse(atlas)

        builder = TreeBuilder()
        tree = builder.build([atlas])

        assert tree["roots"][0]["layer"] == "l2"
