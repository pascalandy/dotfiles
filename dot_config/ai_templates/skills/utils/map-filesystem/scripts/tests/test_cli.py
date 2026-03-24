"""Tests for CLI module."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

runner = CliRunner()


class TestCLI:
    def test_help(self) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "abstract_gen" in result.output

    def test_version(self) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "abstract_gen" in result.output

    def test_scan_directory(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", str(tmp_repo)])
        assert result.exit_code == 0
        assert "test_repo" in result.output
        assert "abstract" in result.output

    def test_scan_json_format(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", str(tmp_repo), "--format", "json"])
        assert result.exit_code == 0
        assert '"path"' in result.output

    def test_scan_tree_output(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", str(tmp_repo), "--tree"])
        assert result.exit_code == 0
        assert "└──" in result.output or "├──" in result.output

    def test_scan_nonexistent_path(self) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", "/nonexistent/path"])
        assert result.exit_code == 1
        assert "Error" in result.output

    def test_scan_empty_directory(self, tmp_repo_empty: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", str(tmp_repo_empty)])
        assert result.exit_code == 2
        assert "No atlas files found" in result.output

    def test_validate_command(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["validate", str(tmp_repo)])
        assert result.exit_code == 0

    def test_validate_invalid_atlas(self, tmp_repo_with_invalid: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["validate", str(tmp_repo_with_invalid)])
        assert result.exit_code == 3

    def test_orphans_command(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        deep_dir = tmp_repo / "deep" / "nested" / "dir"
        deep_dir.mkdir(parents=True)
        (deep_dir / "file.txt").write_text("test")

        result = runner.invoke(app, ["orphans", str(tmp_repo)])
        assert result.exit_code == 0

    def test_depth_limit(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", str(tmp_repo), "--depth", "0"])
        assert result.exit_code == 0

    def test_filter_has_abstract(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", str(tmp_repo), "--has-abstract"])
        assert result.exit_code == 0

    def test_filter_has_overview(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", str(tmp_repo), "--has-overview"])
        assert result.exit_code == 0

    def test_stats_flag(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", str(tmp_repo), "--stats"])
        assert result.exit_code == 0
        assert "Statistics" in result.output or "scan_time" in result.output.lower()

    def test_graphviz_export(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", str(tmp_repo), "--export", "graphviz"])
        assert result.exit_code == 0
        assert "digraph" in result.output

    def test_plain_format(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", str(tmp_repo), "--format", "plain"])
        assert result.exit_code == 0
        assert ".abstract.md" in result.output or ".overview.md" in result.output

    def test_validate_flag_on_scan(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["scan", str(tmp_repo), "--validate"])
        assert result.exit_code == 0


class TestList:
    def test_list_outputs_paths(self, tmp_repo_with_both: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["list", str(tmp_repo_with_both)])
        assert result.exit_code == 0
        paths = result.output.strip().split("\n")
        assert len(paths) >= 2  # root + child_project
        for p in paths:
            assert Path(p).is_absolute()

    def test_list_all_flag(self, tmp_repo_with_both: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["list", str(tmp_repo_with_both), "--all"])
        assert result.exit_code == 0
        paths = result.output.strip().split("\n")
        assert len(paths) >= 2

    def test_list_empty_dir(self, tmp_repo_empty: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["list", str(tmp_repo_empty)])
        assert result.exit_code == 2

    def test_list_nonexistent(self, tmp_path: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["list", str(tmp_path / "nope")])
        assert result.exit_code == 1

    def test_list_no_trailing_slash(self, tmp_repo_with_both: Path) -> None:
        from abstract_gen import app

        result = runner.invoke(app, ["list", str(tmp_repo_with_both)])
        assert result.exit_code == 0
        for line in result.output.strip().split("\n"):
            assert not line.endswith("/")


class TestOrphansFlag:
    def test_orphans_flag_on_scan(self, tmp_repo: Path) -> None:
        from abstract_gen import app

        deep_dir = tmp_repo / "deep" / "nested" / "dir"
        deep_dir.mkdir(parents=True)
        (deep_dir / "file.txt").write_text("test")

        result = runner.invoke(app, ["scan", str(tmp_repo), "--orphans"])
        assert result.exit_code == 0
