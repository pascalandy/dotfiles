"""Frontmatter validation and reference checking."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from lib.models import AtlasFile, AtlasType, ErrorCode, ScanError
from lib.parser import Parser


@dataclass
class ValidationResult:
    atlases: list[AtlasFile]
    errors: list[ScanError]
    warnings: list[str]


class Validator:
    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        self.errors: list[ScanError] = []

    def validate(self, atlases: list[AtlasFile]) -> ValidationResult:
        errors: list[ScanError] = []
        warnings: list[str] = []

        for atlas in atlases:
            field_errors = Parser.validate_frontmatter_fields(atlas)
            atlas.validation_errors.extend(field_errors)
            if field_errors:
                errors.append(
                    ScanError(
                        ErrorCode.E005,
                        f"Validation errors: {'; '.join(field_errors)}",
                        atlas.path,
                    )
                )

        self._validate_parent_refs(atlases, errors)

        self._check_circular_hierarchy(atlases, errors)

        self.validate_date_consistency(atlases, errors)

        return ValidationResult(
            atlases=atlases,
            errors=errors,
            warnings=warnings,
        )

    def _validate_parent_refs(
        self, atlases: list[AtlasFile], errors: list[ScanError]
    ) -> None:
        by_dir: dict[Path, AtlasFile] = {}
        for atlas in atlases:
            by_dir[atlas.dir_path] = atlas

        for atlas in atlases:
            parent_ref = atlas.parent_ref
            if parent_ref is None or parent_ref == "":
                continue

            expected_parent_dir = atlas.dir_path.parent
            parent_atlas = by_dir.get(expected_parent_dir)

            if not parent_atlas:
                atlas.validation_errors.append(
                    f"Parent reference '{parent_ref}' but no atlas in parent dir"
                )
                errors.append(
                    ScanError(
                        ErrorCode.E006,
                        f"Broken parent reference: expected atlas in {expected_parent_dir}",
                        atlas.path,
                        {"parent_ref": parent_ref},
                    )
                )

    def _check_circular_hierarchy(
        self, atlases: list[AtlasFile], errors: list[ScanError]
    ) -> None:
        by_dir: dict[Path, AtlasFile] = {a.dir_path: a for a in atlases}

        def has_cycle(
            start: AtlasFile, visited: set[Path], path: list[Path]
        ) -> list[Path] | None:
            current_dir = start.dir_path
            if current_dir in visited:
                return path + [current_dir]
            visited.add(current_dir)
            path.append(current_dir)

            parent_dir = current_dir.parent
            if parent_dir == current_dir:
                return None

            parent_atlas = by_dir.get(parent_dir)
            if not parent_atlas:
                return None

            return has_cycle(parent_atlas, visited, path)

        for atlas in atlases:
            cycle_path = has_cycle(atlas, set(), [])
            if cycle_path and len(cycle_path) > 1:
                cycle_str = " -> ".join(str(p) for p in cycle_path)
                atlas.validation_errors.append(
                    f"Circular hierarchy detected: {cycle_str}"
                )
                errors.append(
                    ScanError(
                        ErrorCode.E007,
                        f"Circular hierarchy: {cycle_str}",
                        atlas.path,
                    )
                )

    def validate_date_consistency(
        self, atlases: list[AtlasFile], errors: list[ScanError]
    ) -> None:
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")

        for atlas in atlases:
            date_updated = atlas.frontmatter.get("date_updated")
            if not date_updated:
                continue

            date_str = str(date_updated)
            if not date_pattern.match(date_str):
                atlas.validation_errors.append(
                    f"Invalid date_updated format: {date_str} (expected YYYY-MM-DD)"
                )
                continue

            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError as e:
                atlas.validation_errors.append(f"Invalid date: {date_str} - {e}")
