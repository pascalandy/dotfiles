"""Data models for abstract_gen."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class AtlasType(str, Enum):
    ABSTRACT = "abstract"
    OVERVIEW = "overview"


class ErrorCode(str, Enum):
    E001 = "E001"
    E002 = "E002"
    E003 = "E003"
    E004 = "E004"
    E005 = "E005"
    E006 = "E006"
    E007 = "E007"
    E008 = "E008"
    E009 = "E009"
    E010 = "E010"
    E011 = "E011"
    E012 = "E012"
    E013 = "E013"


@dataclass
class ScanError:
    code: ErrorCode
    message: str
    path: Path | None = None
    context: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        loc = f" ({self.path})" if self.path else ""
        return f"[{self.code.value}] {self.message}{loc}"


@dataclass
class AtlasFile:
    path: Path
    atlas_type: AtlasType
    frontmatter: dict[str, Any] = field(default_factory=dict)
    content: str = ""
    children: list[AtlasFile] = field(default_factory=list)
    validation_errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.validation_errors) == 0

    @property
    def layer(self) -> str | None:
        return self.frontmatter.get("layer")

    @property
    def parent_ref(self) -> str | None:
        return self.frontmatter.get("parent")

    @property
    def root(self) -> str | None:
        return self.frontmatter.get("root")

    @property
    def dir_path(self) -> Path:
        return self.path.parent

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": str(self.path),
            "dir": str(self.dir_path),
            "atlas_type": self.atlas_type.value,
            "layer": self.layer,
            "parent": self.parent_ref,
            "root": self.root,
            "is_valid": self.is_valid,
            "validation_errors": self.validation_errors,
            "frontmatter": self.frontmatter,
        }


@dataclass
class ScanResult:
    atlases: list[AtlasFile] = field(default_factory=list)
    orphans: list[Path] = field(default_factory=list)
    tree: dict[str, Any] = field(default_factory=dict)
    errors: list[ScanError] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)

    @property
    def abstract_count(self) -> int:
        return sum(1 for a in self.atlases if a.atlas_type == AtlasType.ABSTRACT)

    @property
    def overview_count(self) -> int:
        return sum(1 for a in self.atlases if a.atlas_type == AtlasType.OVERVIEW)

    @property
    def valid_count(self) -> int:
        return sum(1 for a in self.atlases if a.is_valid)

    @property
    def invalid_count(self) -> int:
        return sum(1 for a in self.atlases if not a.is_valid)

    def get_dirs_with_atlases(self) -> set[Path]:
        return {a.dir_path for a in self.atlases}
