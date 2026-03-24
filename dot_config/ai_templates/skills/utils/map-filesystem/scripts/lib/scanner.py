"""File scanner for atlas discovery."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from lib.models import AtlasFile, AtlasType, ErrorCode, ScanError

ATLAS_FILES = {".abstract.md": AtlasType.ABSTRACT, ".overview.md": AtlasType.OVERVIEW}
MAX_FILE_SIZE = 1_000_000
LARGE_DIR_THRESHOLD = 10_000

SKIP_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        ".bzr",
        ".venv",
        "venv",
        ".env",
        "env",
        ".tox",
        "node_modules",
        "__pycache__",
        ".mypy_cache",
        ".ruff_cache",
        ".pytest_cache",
        ".idea",
        ".vscode",
        ".sublime",
        "dist",
        "build",
        ".eggs",
        ".egg-info",
        ".cache",
        ".Trash",
        "google-cloud-sdk",
        "gcloud",
        ".gcloud",
        "vendors",
        "vendor",
    }
)

ARCHIVE_PATTERNS = frozenset(
    {
        "archived",
        "archive",
        "_archived",
        "_archive",
        "old",
        "_old",
        "backup",
        "_backup",
        "deprecated",
        "_deprecated",
        "legacy",
        "_legacy",
    }
)


def _is_archive_dir(name: str) -> bool:
    lower = name.lower()
    return (
        lower in ARCHIVE_PATTERNS
        or lower.endswith("_archived")
        or lower.endswith("_archive")
    )


@dataclass
class ScannerConfig:
    root_path: Path
    max_depth: int | None = None
    follow_symlinks: bool = True
    has_abstract: bool = False
    has_overview: bool = False
    has_both: bool = False
    quiet: bool = False
    verbose: bool = False


class Scanner:
    def __init__(self, config: ScannerConfig):
        self.config = config
        self.errors: list[ScanError] = []
        self._visited_inodes: set[int] = set()
        self._file_count = 0
        self._dir_count = 0

    def scan(self) -> list[AtlasFile]:
        self._visited_inodes = set()
        self._file_count = 0
        self._dir_count = 0

        root = self.config.root_path.resolve()
        if not root.exists():
            self.errors.append(
                ScanError(ErrorCode.E001, f"Path not found: {root}", root)
            )
            return []

        if not root.is_dir():
            self.errors.append(
                ScanError(ErrorCode.E001, f"Not a directory: {root}", root)
            )
            return []

        results: list[AtlasFile] = []
        for atlas_file in self._walk(root, depth=0):
            results.append(atlas_file)

        return results

    def _walk(self, path: Path, depth: int) -> Iterator[AtlasFile]:
        if self.config.max_depth is not None and depth > self.config.max_depth:
            return

        try:
            entries = list(path.iterdir())
        except PermissionError:
            self.errors.append(ScanError(ErrorCode.E002, "Permission denied", path))
            return
        except OSError as e:
            self.errors.append(ScanError(ErrorCode.E002, str(e), path))
            return

        self._dir_count += 1
        self._file_count += len(entries)

        if self._file_count > LARGE_DIR_THRESHOLD:
            if self.config.verbose and not any(
                e.code == ErrorCode.E013 for e in self.errors
            ):
                self.errors.append(
                    ScanError(
                        ErrorCode.E013,
                        f"Large directory detected ({self._file_count} files), continuing",
                        path,
                    )
                )

        dir_atlases: list[AtlasFile] = []

        for entry in entries:
            try:
                resolved = self._resolve_entry(entry)
                if resolved is None:
                    continue

                if resolved.is_dir():
                    if (
                        resolved.name in SKIP_DIRS
                        or resolved.name.startswith(".")
                        or _is_archive_dir(resolved.name)
                    ):
                        continue
                    yield from self._walk(resolved, depth + 1)
                elif resolved.name in ATLAS_FILES:
                    atlas_file = self._create_atlas_entry(resolved)
                    if atlas_file and self._matches_filters(atlas_file):
                        dir_atlases.append(atlas_file)

            except OSError as e:
                if not self.config.quiet:
                    self.errors.append(ScanError(ErrorCode.E002, str(e), entry))

        yield from dir_atlases

    def _resolve_entry(self, entry: Path) -> Path | None:
        if entry.is_symlink():
            if not self.config.follow_symlinks:
                return None

            try:
                inode = entry.stat().st_ino
                if inode in self._visited_inodes:
                    if self.config.verbose:
                        self.errors.append(
                            ScanError(ErrorCode.E003, "Symlink cycle detected", entry)
                        )
                    return None
                self._visited_inodes.add(inode)

                resolved = entry.resolve()
                if not str(resolved).startswith(str(self.config.root_path.resolve())):
                    self.errors.append(
                        ScanError(ErrorCode.E003, "Symlink escapes root scope", entry)
                    )
                    return None
                return resolved
            except OSError:
                if self.config.verbose:
                    self.errors.append(
                        ScanError(ErrorCode.E003, "Broken symlink", entry)
                    )
                return None

        return entry

    def _create_atlas_entry(self, path: Path) -> AtlasFile | None:
        try:
            file_stat = path.stat()
            if file_stat.st_size > MAX_FILE_SIZE:
                self.errors.append(
                    ScanError(
                        ErrorCode.E011,
                        f"File too large ({file_stat.st_size} bytes)",
                        path,
                    )
                )
                return None
        except OSError as e:
            self.errors.append(ScanError(ErrorCode.E002, str(e), path))
            return None

        return AtlasFile(path=path, atlas_type=ATLAS_FILES[path.name])

    def _matches_filters(self, atlas: AtlasFile) -> bool:
        if (
            not self.config.has_abstract
            and not self.config.has_overview
            and not self.config.has_both
        ):
            return True

        parent = atlas.dir_path
        has_abstract = (parent / ".abstract.md").exists()
        has_overview = (parent / ".overview.md").exists()

        if self.config.has_both:
            return has_abstract and has_overview
        if self.config.has_abstract:
            return has_abstract
        if self.config.has_overview:
            return has_overview
        return True

    def find_orphans(self, atlases: list[AtlasFile]) -> list[Path]:
        orphan_dirs: list[Path] = []
        visited: set[Path] = set()

        atlas_dirs = {a.dir_path for a in atlases}

        def check_orphan(path: Path, depth: int) -> None:
            if self.config.max_depth is not None and depth > self.config.max_depth:
                return
            if path in visited:
                return
            visited.add(path)

            try:
                entries = list(path.iterdir())
            except (PermissionError, OSError):
                return

            subdirs: list[Path] = []
            for entry in entries:
                resolved = self._resolve_entry(entry)
                if (
                    resolved is not None
                    and resolved.is_dir()
                    and resolved.name not in SKIP_DIRS
                    and not resolved.name.startswith(".")
                    and not _is_archive_dir(resolved.name)
                ):
                    subdirs.append(resolved)

            if subdirs and path not in atlas_dirs:
                orphan_dirs.append(path)

            for subdir in subdirs:
                check_orphan(subdir, depth + 1)

        check_orphan(self.config.root_path.resolve(), 0)
        return orphan_dirs

    @property
    def stats(self) -> dict[str, int]:
        return {
            "files_scanned": self._file_count,
            "dirs_scanned": self._dir_count,
        }
