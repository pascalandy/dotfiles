"""Tests for exporter module."""

from __future__ import annotations

import json
from pathlib import Path

from lib.exporter import ExportConfig, Exporter
from lib.models import AtlasFile, AtlasType, ErrorCode, ScanResult
from lib.parser import Parser


class TestExporter:
    def test_format_human(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
            AtlasFile(path=tmp_repo / ".overview.md", atlas_type=AtlasType.OVERVIEW),
        ]
        atlases = parser.parse_batch(atlases)

        result = ScanResult(atlases=atlases)

        exporter = Exporter(ExportConfig(format="human"))
        output = exporter.export(result)

        assert str(tmp_repo) in output
        assert "abstract" in output
        assert "overview" in output

    def test_format_json(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        result = ScanResult(atlases=atlases)

        exporter = Exporter(ExportConfig(format="json"))
        output = exporter.export(result)

        data = json.loads(output)
        assert len(data) >= 1
        assert data[0]["files"] == ["abstract"]

    def test_format_json_with_metadata(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        result = ScanResult(atlases=atlases)

        exporter = Exporter(ExportConfig(format="json", include_metadata=True))
        output = exporter.export(result)

        data = json.loads(output)
        assert "frontmatter" in data[0]

    def test_format_plain(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        result = ScanResult(atlases=atlases)

        exporter = Exporter(ExportConfig(format="plain"))
        output = exporter.export(result)

        assert ".abstract.md" in output

    def test_export_tree(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
            AtlasFile(path=tmp_repo / "subdir" / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        result = ScanResult(atlases=atlases)

        exporter = Exporter(ExportConfig(format="human"))
        output = exporter.export_tree(result)

        assert "└──" in output or "├──" in output

    def test_export_graphviz(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        result = ScanResult(atlases=atlases)

        exporter = Exporter(ExportConfig(format="human"))
        output = exporter.export_graphviz(result)

        assert "digraph" in output
        assert tmp_repo.name in output

    def test_empty_result(self) -> None:
        result = ScanResult(atlases=[])

        exporter = Exporter(ExportConfig(format="human"))
        output = exporter.export(result)

        assert output == ""

    def test_format_json_with_stats(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        result = ScanResult(
            atlases=atlases,
            stats={"scan_time_ms": 100, "atlases_found": 1},
        )

        exporter = Exporter(ExportConfig(format="json", show_stats=True))
        output = exporter.export(result)

        data = json.loads(output)
        assert "stats" in data
        assert data["stats"]["scan_time_ms"] == 100

    def test_format_yaml_fallback(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        result = ScanResult(atlases=atlases)

        exporter = Exporter(ExportConfig(format="yaml"))
        output = exporter.export(result)

        assert output.startswith("#") or "path:" in output or output.startswith("[")

    def test_format_toml_fallback(self, tmp_repo: Path) -> None:
        parser = Parser()
        atlases = [
            AtlasFile(path=tmp_repo / ".abstract.md", atlas_type=AtlasType.ABSTRACT),
        ]
        atlases = parser.parse_batch(atlases)

        result = ScanResult(atlases=atlases)

        exporter = Exporter(ExportConfig(format="toml"))
        output = exporter.export(result)

        assert output.startswith("#") or "[[atlases]]" in output or output.startswith("{")

    def test_check_graphviz_available_returns_error_when_not_found(self, monkeypatch) -> None:
        import shutil

        def mock_which(cmd: str):
            return None if cmd == "dot" else shutil.which(cmd)

        monkeypatch.setattr(shutil, "which", mock_which)

        exporter = Exporter()
        error = exporter.check_graphviz_available()

        assert error is not None
        assert error.code == ErrorCode.E012
        assert "graphviz" in error.message.lower()
