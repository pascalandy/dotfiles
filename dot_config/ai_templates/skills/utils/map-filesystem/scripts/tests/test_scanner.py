"""Tests for scanner module."""

from __future__ import annotations

from pathlib import Path

import pytest
from lib.models import AtlasType, ErrorCode
from lib.scanner import Scanner, ScannerConfig


class TestScanner:
    def test_scan_finds_atlas_files(self, tmp_repo: Path) -> None:
        config = ScannerConfig(root_path=tmp_repo)
        scanner = Scanner(config)
        results = scanner.scan()

        assert len(results) >= 3

        types = {r.atlas_type for r in results}
        assert AtlasType.ABSTRACT in types
        assert AtlasType.OVERVIEW in types

    def test_scan_respects_depth_limit(self, tmp_repo: Path) -> None:
        config = ScannerConfig(root_path=tmp_repo, max_depth=0)
        scanner = Scanner(config)
        results = scanner.scan()

        for atlas in results:
            assert atlas.dir_path == tmp_repo

    def test_scan_nonexistent_path(self, tmp_path: Path) -> None:
        config = ScannerConfig(root_path=tmp_path / "nonexistent")
        scanner = Scanner(config)
        results = scanner.scan()

        assert results == []
        assert any(e.code == ErrorCode.E001 for e in scanner.errors)

    def test_scan_file_not_directory(self, tmp_path: Path) -> None:
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")

        config = ScannerConfig(root_path=file_path)
        scanner = Scanner(config)
        results = scanner.scan()

        assert results == []
        assert any(e.code == ErrorCode.E001 for e in scanner.errors)

    def test_filter_has_abstract(self, tmp_repo: Path) -> None:
        config = ScannerConfig(root_path=tmp_repo, has_abstract=True)
        scanner = Scanner(config)
        results = scanner.scan()

        for atlas in results:
            parent = atlas.dir_path
            has_abstract = (parent / ".abstract.md").exists()
            assert has_abstract

    def test_filter_has_overview(self, tmp_repo: Path) -> None:
        config = ScannerConfig(root_path=tmp_repo, has_overview=True)
        scanner = Scanner(config)
        results = scanner.scan()

        for atlas in results:
            parent = atlas.dir_path
            has_overview = (parent / ".overview.md").exists()
            assert has_overview

    def test_filter_has_both(self, tmp_repo: Path) -> None:
        config = ScannerConfig(root_path=tmp_repo, has_both=True)
        scanner = Scanner(config)
        results = scanner.scan()

        for atlas in results:
            parent = atlas.dir_path
            has_abstract = (parent / ".abstract.md").exists()
            has_overview = (parent / ".overview.md").exists()
            assert has_abstract and has_overview

    def test_find_orphans(self, tmp_repo: Path) -> None:
        deep_dir = tmp_repo / "deep" / "nested" / "dir"
        deep_dir.mkdir(parents=True)
        (deep_dir / "file.txt").write_text("test")

        config = ScannerConfig(root_path=tmp_repo)
        scanner = Scanner(config)
        atlases = scanner.scan()
        orphans = scanner.find_orphans(atlases)

        assert tmp_repo / "deep" in orphans

    def test_scan_empty_directory(self, tmp_repo_empty: Path) -> None:
        config = ScannerConfig(root_path=tmp_repo_empty)
        scanner = Scanner(config)
        results = scanner.scan()

        assert results == []

    def test_symlink_cycle_detection(self, tmp_path: Path) -> None:
        dir_a = tmp_path / "a"
        dir_b = tmp_path / "b"
        dir_a.mkdir()
        dir_b.mkdir()

        try:
            (dir_a / "link_to_b").symlink_to(dir_b)
            (dir_b / "link_to_a").symlink_to(dir_a)

            config = ScannerConfig(root_path=tmp_path, verbose=True)
            scanner = Scanner(config)
            scanner.scan()

            assert any(e.code == ErrorCode.E003 for e in scanner.errors)
        except OSError:
            pytest.skip("Symlinks not supported on this system")

    def test_atlas_type_correct(self, tmp_repo: Path) -> None:
        config = ScannerConfig(root_path=tmp_repo)
        scanner = Scanner(config)
        results = scanner.scan()

        for atlas in results:
            if atlas.path.name == ".abstract.md":
                assert atlas.atlas_type == AtlasType.ABSTRACT
            elif atlas.path.name == ".overview.md":
                assert atlas.atlas_type == AtlasType.OVERVIEW

    def test_skips_git_directory(self, tmp_repo: Path) -> None:
        git_dir = tmp_repo / ".git" / "objects"
        git_dir.mkdir(parents=True)
        (git_dir / ".abstract.md").write_text("# Git atlas")

        config = ScannerConfig(root_path=tmp_repo)
        scanner = Scanner(config)
        results = scanner.scan()

        git_atlases = [a for a in results if a.path.is_relative_to(tmp_repo / ".git")]
        assert git_atlases == []

    def test_skips_node_modules(self, tmp_repo: Path) -> None:
        node_dir = tmp_repo / "node_modules" / "package"
        node_dir.mkdir(parents=True)
        (node_dir / ".abstract.md").write_text("# Node atlas")

        config = ScannerConfig(root_path=tmp_repo)
        scanner = Scanner(config)
        results = scanner.scan()

        node_atlases = [a for a in results if a.path.is_relative_to(tmp_repo / "node_modules")]
        assert node_atlases == []

    def test_skips_venv(self, tmp_repo: Path) -> None:
        venv_dir = tmp_repo / ".venv" / "lib"
        venv_dir.mkdir(parents=True)
        (venv_dir / ".abstract.md").write_text("# Venv atlas")

        config = ScannerConfig(root_path=tmp_repo)
        scanner = Scanner(config)
        results = scanner.scan()

        venv_atlases = [a for a in results if a.path.is_relative_to(tmp_repo / ".venv")]
        assert venv_atlases == []

    def test_skips_hidden_directories(self, tmp_repo: Path) -> None:
        hidden_dir = tmp_repo / ".hidden" / "nested"
        hidden_dir.mkdir(parents=True)
        (hidden_dir / ".abstract.md").write_text("# Hidden atlas")

        config = ScannerConfig(root_path=tmp_repo)
        scanner = Scanner(config)
        results = scanner.scan()

        hidden_atlases = [a for a in results if a.path.is_relative_to(tmp_repo / ".hidden")]
        assert hidden_atlases == []

    def test_skip_sdk_dirs(self, tmp_repo: Path) -> None:
        sdk_dir = tmp_repo / "google-cloud-sdk" / "lib"
        sdk_dir.mkdir(parents=True)
        (sdk_dir / ".abstract.md").write_text("# SDK atlas")

        gcloud_dir = tmp_repo / ".gcloud" / "config"
        gcloud_dir.mkdir(parents=True)
        (gcloud_dir / ".abstract.md").write_text("# GCloud atlas")

        config = ScannerConfig(root_path=tmp_repo)
        scanner = Scanner(config)
        results = scanner.scan()

        sdk_atlases = [
            a
            for a in results
            if a.path.is_relative_to(tmp_repo / "google-cloud-sdk")
            or a.path.is_relative_to(tmp_repo / ".gcloud")
        ]
        assert sdk_atlases == []

    def test_skip_vendor_dirs(self, tmp_repo: Path) -> None:
        vendor_dir = tmp_repo / "vendors" / "lib"
        vendor_dir.mkdir(parents=True)
        (vendor_dir / ".abstract.md").write_text("# Vendor atlas")

        vendor2_dir = tmp_repo / "vendor" / "pkg"
        vendor2_dir.mkdir(parents=True)
        (vendor2_dir / ".abstract.md").write_text("# Vendor2 atlas")

        config = ScannerConfig(root_path=tmp_repo)
        scanner = Scanner(config)
        results = scanner.scan()

        vendor_atlases = [
            a
            for a in results
            if a.path.is_relative_to(tmp_repo / "vendors")
            or a.path.is_relative_to(tmp_repo / "vendor")
        ]
        assert vendor_atlases == []

    def test_skip_archive_dirs(self, tmp_repo: Path) -> None:
        archive_dir = tmp_repo / "archived" / "old"
        archive_dir.mkdir(parents=True)
        (archive_dir / ".abstract.md").write_text("# Archive atlas")

        archive2_dir = tmp_repo / "project_archived" / "old"
        archive2_dir.mkdir(parents=True)
        (archive2_dir / ".abstract.md").write_text("# Archive2 atlas")

        archive3_dir = tmp_repo / "Z_ARCHIVED" / "old"
        archive3_dir.mkdir(parents=True)
        (archive3_dir / ".abstract.md").write_text("# Archive3 atlas")

        config = ScannerConfig(root_path=tmp_repo)
        scanner = Scanner(config)
        results = scanner.scan()

        archive_atlases = [
            a
            for a in results
            if a.path.is_relative_to(tmp_repo / "archived")
            or a.path.is_relative_to(tmp_repo / "project_archived")
            or a.path.is_relative_to(tmp_repo / "Z_ARCHIVED")
        ]
        assert archive_atlases == []
