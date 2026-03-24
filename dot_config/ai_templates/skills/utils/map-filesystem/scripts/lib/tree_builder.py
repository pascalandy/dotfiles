"""Tree hierarchy builder for atlas files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lib.models import AtlasFile, AtlasType


@dataclass
class TreeNode:
    dir_path: Path
    layer: str | None = None
    abstract: AtlasFile | None = None
    overview: AtlasFile | None = None
    children: list[TreeNode] = field(default_factory=list)

    def has_atlases(self) -> bool:
        return self.abstract is not None or self.overview is not None

    def atlas_types(self) -> list[str]:
        types: list[str] = []
        if self.abstract:
            types.append("abstract")
        if self.overview:
            types.append("overview")
        return types


class TreeBuilder:
    def build(self, atlases: list[AtlasFile]) -> dict[str, Any]:
        by_dir: dict[Path, TreeNode] = {}

        for atlas in atlases:
            dir_path = atlas.dir_path
            if dir_path not in by_dir:
                by_dir[dir_path] = TreeNode(dir_path=dir_path)

            node = by_dir[dir_path]
            if atlas.atlas_type == AtlasType.ABSTRACT:
                node.abstract = atlas
            elif atlas.atlas_type == AtlasType.OVERVIEW:
                node.overview = atlas

            if node.layer is None and atlas.layer:
                node.layer = atlas.layer

        for node in by_dir.values():
            if node.layer is None:
                node.layer = self._infer_layer(node.dir_path, by_dir)

        self._link_children(by_dir)

        roots = self._find_roots(by_dir)

        return {
            "roots": [self._node_to_dict(r) for r in roots],
            "nodes": {str(p): self._node_to_dict(n) for p, n in by_dir.items()},
        }

    def _infer_layer(self, dir_path: Path, by_dir: dict[Path, TreeNode]) -> str:
        depth = self._count_depth(dir_path)
        return f"l{depth}"

    def _count_depth(self, path: Path) -> int:
        parts = path.parts
        return max(0, len(parts) - 1)

    def _link_children(self, by_dir: dict[Path, TreeNode]) -> None:
        sorted_dirs = sorted(by_dir.keys(), key=lambda p: len(p.parts))

        for dir_path in sorted_dirs:
            node = by_dir[dir_path]
            parent_path = dir_path.parent

            if parent_path in by_dir and parent_path != dir_path:
                parent_node = by_dir[parent_path]
                if node not in parent_node.children:
                    parent_node.children.append(node)

    def _find_roots(self, by_dir: dict[Path, TreeNode]) -> list[TreeNode]:
        roots: list[TreeNode] = []
        for node in by_dir.values():
            parent_path = node.dir_path.parent
            if parent_path not in by_dir or parent_path == node.dir_path:
                roots.append(node)

        return sorted(roots, key=lambda n: str(n.dir_path))

    def _node_to_dict(self, node: TreeNode) -> dict[str, Any]:
        result: dict[str, Any] = {
            "path": str(node.dir_path),
            "name": node.dir_path.name or str(node.dir_path),
            "layer": node.layer,
            "atlases": node.atlas_types(),
            "children": [self._node_to_dict(c) for c in node.children],
        }

        if node.abstract:
            result["abstract_valid"] = node.abstract.is_valid
        if node.overview:
            result["overview_valid"] = node.overview.is_valid

        return result

    def build_ascii_tree(self, atlases: list[AtlasFile]) -> str:
        tree = self.build(atlases)
        lines: list[str] = []

        for root in tree["roots"]:
            self._render_node(root, lines, prefix="", is_last=True)

        return "\n".join(lines)

    def _render_node(
        self, node: dict[str, Any], lines: list[str], prefix: str, is_last: bool
    ) -> None:
        name = node["name"]
        layer = node.get("layer", "")
        atlases = node.get("atlases", [])

        connector = "└── " if is_last else "├── "
        layer_str = f" ({layer})" if layer else ""
        atlas_str = f" [{', '.join(atlases)}]" if atlases else ""

        lines.append(f"{prefix}{connector}{name}/{layer_str}{atlas_str}")

        children = node.get("children", [])
        child_prefix = prefix + ("    " if is_last else "│   ")

        for i, child in enumerate(children):
            self._render_node(child, lines, child_prefix, i == len(children) - 1)
