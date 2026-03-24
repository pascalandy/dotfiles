"""Output formatting and export for scan results."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from io import StringIO
from pathlib import Path
from typing import Any

from lib.models import AtlasFile, AtlasType, ErrorCode, ScanError, ScanResult
from lib.tree_builder import TreeBuilder


class AtlasJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, Path):
            return str(o)
        return super().default(o)


@dataclass
class ExportConfig:
    format: str = "human"
    include_metadata: bool = False
    show_stats: bool = False


class Exporter:
    def __init__(self, config: ExportConfig | None = None):
        self.config = config or ExportConfig()
        self.tree_builder = TreeBuilder()

    def check_graphviz_available(self) -> ScanError | None:
        import shutil

        if shutil.which("dot") is None:
            return ScanError(
                ErrorCode.E012,
                "Graphviz 'dot' command not found. Install graphviz to render diagrams.",
                None,
            )
        return None

    def export(self, result: ScanResult) -> str:
        format_map = {
            "human": self._format_human,
            "json": self._format_json,
            "yaml": self._format_yaml,
            "toml": self._format_toml,
            "plain": self._format_plain,
        }

        formatter = format_map.get(self.config.format, self._format_human)
        return formatter(result)

    def export_tree(self, result: ScanResult) -> str:
        return self.tree_builder.build_ascii_tree(result.atlases)

    def export_graphviz(self, result: ScanResult) -> str:
        lines: list[str] = [
            "digraph atlas_tree {",
            "    rankdir=TB;",
            "    node [shape=box, style=rounded];",
            "",
        ]

        by_dir: dict[Path, AtlasFile] = {}
        for atlas in result.atlases:
            if atlas.dir_path not in by_dir:
                by_dir[atlas.dir_path] = atlas

        for dir_path, atlas in by_dir.items():
            node_id = self._path_to_node_id(dir_path)
            label = dir_path.name or str(dir_path)
            layer = atlas.layer or ""

            color = self._get_layer_color(layer)

            lines.append(
                f'    "{node_id}" [label="{label}\\n({layer})" fillcolor="{color}" style="filled,rounded"];'
            )

        lines.append("")

        for dir_path, atlas in by_dir.items():
            parent_dir = dir_path.parent
            if parent_dir in by_dir and parent_dir != dir_path:
                parent_id = self._path_to_node_id(parent_dir)
                child_id = self._path_to_node_id(dir_path)
                lines.append(f'    "{parent_id}" -> "{child_id}";')

        lines.append("}")
        return "\n".join(lines)

    def _path_to_node_id(self, path: Path) -> str:
        return str(path).replace("/", "_").replace("\\", "_").replace(":", "_")

    def _get_layer_color(self, layer: str) -> str:
        colors = {
            "l0": "#e3f2fd",
            "l1": "#fff3e0",
            "l2": "#e8f5e9",
            "l3": "#fce4ec",
            "l4": "#f3e5f5",
        }
        return colors.get(layer, "#fafafa")

    def _format_human(self, result: ScanResult) -> str:
        lines: list[str] = []

        grouped: dict[Path, list[str]] = {}
        for atlas in result.atlases:
            dir_path = atlas.dir_path
            if dir_path not in grouped:
                grouped[dir_path] = []
            grouped[dir_path].append(
                "abstract" if atlas.atlas_type == AtlasType.ABSTRACT else "overview"
            )

        for dir_path in sorted(grouped.keys()):
            types = sorted(grouped[dir_path])
            type_str = ", ".join(types)
            lines.append(f"{dir_path} ({type_str})")

        return "\n".join(lines)

    def _format_json(self, result: ScanResult) -> str:
        output: list[dict[str, Any]] = []

        grouped: dict[Path, dict[str, Any]] = {}
        for atlas in result.atlases:
            dir_path = atlas.dir_path
            if dir_path not in grouped:
                grouped[dir_path] = {
                    "path": str(dir_path),
                    "files": [],
                    "layer": atlas.layer,
                    "is_valid": atlas.is_valid,
                }
                if self.config.include_metadata:
                    grouped[dir_path]["frontmatter"] = atlas.frontmatter

            file_type = (
                "abstract" if atlas.atlas_type == AtlasType.ABSTRACT else "overview"
            )
            if file_type not in grouped[dir_path]["files"]:
                grouped[dir_path]["files"].append(file_type)

        output = list(grouped.values())

        if self.config.show_stats:
            return json.dumps(
                {
                    "atlases": output,
                    "stats": result.stats,
                    "errors": [str(e) for e in result.errors],
                },
                indent=2,
                cls=AtlasJSONEncoder,
            )

        return json.dumps(output, indent=2, cls=AtlasJSONEncoder)

    def _format_yaml(self, result: ScanResult) -> str:
        try:
            import yaml

            data = self._prepare_data(result)
            return yaml.dump(data, default_flow_style=False, sort_keys=False)
        except ImportError:
            return "# Error: pyyaml not installed\n" + self._format_json(result)

    def _format_toml(self, result: ScanResult) -> str:
        try:
            import tomli_w

            data = self._prepare_data(result)
            return tomli_w.dumps({"atlases": data})
        except ImportError:
            return "# Error: tomli-w not installed\n" + self._format_json(result)

    def _format_plain(self, result: ScanResult) -> str:
        lines: list[str] = []
        for atlas in sorted(result.atlases, key=lambda a: str(a.path)):
            lines.append(str(atlas.path))
        return "\n".join(lines)

    def _prepare_data(self, result: ScanResult) -> list[dict[str, Any]]:
        output: list[dict[str, Any]] = []

        grouped: dict[Path, dict[str, Any]] = {}
        for atlas in result.atlases:
            dir_path = atlas.dir_path
            if dir_path not in grouped:
                grouped[dir_path] = {
                    "path": str(dir_path),
                    "files": [],
                    "layer": atlas.layer,
                    "is_valid": atlas.is_valid,
                }

            file_type = (
                "abstract" if atlas.atlas_type == AtlasType.ABSTRACT else "overview"
            )
            if file_type not in grouped[dir_path]["files"]:
                grouped[dir_path]["files"].append(file_type)

        return list(grouped.values())
