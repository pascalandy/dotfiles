"""YAML frontmatter parser for atlas files."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from lib.models import AtlasFile, ErrorCode, ScanError

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
REQUIRED_FIELDS = ["type", "layer", "corpus", "scope", "root"]


class Parser:
    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        self.errors: list[ScanError] = []

    def parse(self, atlas: AtlasFile) -> AtlasFile:
        try:
            content = atlas.path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = atlas.path.read_text(encoding="utf-8-sig")
        except OSError as e:
            self.errors.append(ScanError(ErrorCode.E002, str(e), atlas.path))
            atlas.validation_errors.append(f"Cannot read file: {e}")
            return atlas

        content = self._strip_bom(content)

        match = FRONTMATTER_PATTERN.match(content)
        if not match:
            atlas.validation_errors.append("Missing or invalid YAML frontmatter")
            return atlas

        yaml_content = match.group(1)
        body = match.group(2)

        try:
            frontmatter = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            self.errors.append(
                ScanError(ErrorCode.E004, f"Invalid YAML: {e}", atlas.path)
            )
            atlas.validation_errors.append(f"Invalid YAML frontmatter: {e}")
            return atlas

        if not isinstance(frontmatter, dict):
            atlas.validation_errors.append("Frontmatter must be a YAML mapping")
            return atlas

        atlas.frontmatter = frontmatter
        atlas.content = body

        return atlas

    def parse_batch(self, atlases: list[AtlasFile]) -> list[AtlasFile]:
        return [self.parse(atlas) for atlas in atlases]

    def _strip_bom(self, content: str) -> str:
        if content.startswith("\ufeff"):
            return content[1:]
        return content

    @staticmethod
    def validate_frontmatter_fields(atlas: AtlasFile) -> list[str]:
        errors: list[str] = []
        fm = atlas.frontmatter

        if not fm:
            return ["Missing frontmatter"]

        for field in REQUIRED_FIELDS:
            if field not in fm:
                errors.append(f"Missing required field: {field}")
            elif fm[field] is None or fm[field] == "":
                errors.append(f"Empty required field: {field}")

        layer = fm.get("layer", "")
        if layer and not re.match(r"^l\d+$", str(layer)):
            errors.append(f"Invalid layer format: {layer} (expected l0, l1, l2...)")

        return errors
