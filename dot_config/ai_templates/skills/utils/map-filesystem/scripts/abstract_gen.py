#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "typer>=0.9.0",
#     "rich>=13.0.0",
#     "pyyaml>=6.0",
#     "tomli-w>=1.0",
# ]
# ///
"""abstract_gen - Discover, validate, and export atlas files."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Annotated

import typer
from lib.exporter import ExportConfig, Exporter
from lib.models import ErrorCode, ScanResult
from lib.parser import Parser
from lib.scanner import Scanner, ScannerConfig
from lib.tree_builder import TreeBuilder
from lib.validator import Validator
from rich.console import Console
from rich.table import Table

_HELP = """\
Discover, validate, and export atlas files (.abstract.md, .overview.md).

Via AI harness (OpenCode, Claude Code):
  /map-filesystem              Map current directory
  /map-filesystem map ~/path   Map a specific path
  /map-filesystem refresh      Batch-refresh existing atlases

Via CLI:
  uv run abstract_gen.py scan ~/path           Discover atlas files
  uv run abstract_gen.py scan ~/path --tree    Show as ASCII tree
  uv run abstract_gen.py scan ~/path -f json   JSON output
  uv run abstract_gen.py validate ~/path       Check frontmatter
  uv run abstract_gen.py orphans ~/path        Find missing atlases
  uv run abstract_gen.py refresh               List dirs to refresh
  uv run abstract_gen.py refresh --all         List ALL dirs (heavy)

Exit codes: 0=ok  1=error  2=empty  3=invalid"""

app = typer.Typer(
    name="abstract_gen",
    help=_HELP,
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    if value:
        console.print("abstract_gen 1.0.0")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool, typer.Option("--version", "-v", callback=version_callback, is_eager=True)
    ] = False,
) -> None:
    pass


@app.command()
def scan(
    path: Annotated[
        Path, typer.Argument(help="Directory to scan", exists=False)
    ] = Path("."),
    format: Annotated[
        str,
        typer.Option(
            "--format", "-f", help="Output format: human, json, yaml, toml, plain"
        ),
    ] = "human",
    tree: Annotated[
        bool, typer.Option("--tree", "-t", help="Show ASCII tree hierarchy")
    ] = False,
    export: Annotated[
        str | None, typer.Option("--export", "-e", help="Export to file: graphviz")
    ] = None,
    has_abstract: Annotated[
        bool, typer.Option("--has-abstract", help="Only dirs with .abstract.md")
    ] = False,
    has_overview: Annotated[
        bool, typer.Option("--has-overview", help="Only dirs with .overview.md")
    ] = False,
    has_both: Annotated[
        bool, typer.Option("--has-both", help="Only dirs with both atlases")
    ] = False,
    validate: Annotated[
        bool, typer.Option("--validate", help="Check frontmatter consistency")
    ] = False,
    orphans: Annotated[
        bool, typer.Option("--orphans", help="Find dirs missing expected atlases")
    ] = False,
    depth: Annotated[
        int | None, typer.Option("--depth", "-d", help="Max recursion depth")
    ] = None,
    metadata: Annotated[
        bool, typer.Option("--metadata", "-m", help="Include frontmatter")
    ] = False,
    stats: Annotated[
        bool, typer.Option("--stats", "-s", help="Show timing statistics")
    ] = False,
    verbose: Annotated[bool, typer.Option("--verbose", help="Show progress")] = False,
    debug: Annotated[bool, typer.Option("--debug", help="Full debug output")] = False,
    quiet: Annotated[
        bool, typer.Option("--quiet", "-q", help="Suppress warnings")
    ] = False,
) -> None:
    """Discover atlas files with filters and multiple output formats."""
    _run_scan(
        path=path,
        format=format,
        show_tree=tree,
        export_format=export,
        has_abstract=has_abstract,
        has_overview=has_overview,
        has_both=has_both,
        validate=validate,
        find_orphans=orphans,
        depth=depth,
        include_metadata=metadata,
        show_stats=stats,
        verbose=verbose,
        debug=debug,
        quiet=quiet,
    )


@app.command()
def validate(
    path: Annotated[
        Path, typer.Argument(help="Directory to scan", exists=False)
    ] = Path("."),
    depth: Annotated[
        int | None, typer.Option("--depth", "-d", help="Max recursion depth")
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose", help="Show progress")] = False,
    quiet: Annotated[
        bool, typer.Option("--quiet", "-q", help="Suppress warnings")
    ] = False,
) -> None:
    """Check frontmatter consistency across atlas files."""
    _run_scan(
        path=path,
        format="human",
        validate=True,
        depth=depth,
        verbose=verbose,
        quiet=quiet,
    )


@app.command()
def orphans(
    path: Annotated[
        Path, typer.Argument(help="Directory to scan", exists=False)
    ] = Path("."),
    depth: Annotated[
        int | None, typer.Option("--depth", "-d", help="Max recursion depth")
    ] = None,
    format: Annotated[
        str, typer.Option("--format", "-f", help="Output format: human, json")
    ] = "human",
    quiet: Annotated[
        bool, typer.Option("--quiet", "-q", help="Suppress warnings")
    ] = False,
) -> None:
    """Find directories missing expected atlas files."""
    _run_scan(
        path=path,
        format=format,
        find_orphans=True,
        depth=depth,
        quiet=quiet,
    )


@app.command()
def refresh(
    path: Annotated[Path, typer.Argument(help="Directory to scan")] = Path.home()
    / "Documents/github_local/executive-assistant",
    all_projects: Annotated[
        bool,
        typer.Option("--all", help="Output ALL atlas directories (resource-intensive)"),
    ] = False,
    quiet: Annotated[
        bool, typer.Option("--quiet", "-q", help="Suppress warnings")
    ] = False,
) -> None:
    """List directories with existing atlas files for batch refresh."""
    stderr_console = Console(stderr=True)
    resolved = path.expanduser().resolve()
    if not resolved.is_dir():
        stderr_console.print(f"[red]Error:[/red] {resolved} is not a directory")
        raise typer.Exit(1)

    config = ScannerConfig(root_path=resolved, has_both=True, quiet=quiet)
    scanner = Scanner(config)
    atlases = scanner.scan()
    if not atlases:
        stderr_console.print(
            "[yellow]No directories with both atlas files found.[/yellow]"
        )
        raise typer.Exit(2)

    # Deduplicate by directory
    atlas_dirs = sorted({a.dir_path for a in atlases})

    # Group by root project (first component relative to scan root)
    groups: dict[str, list[Path]] = {}
    for d in atlas_dirs:
        try:
            rel = d.relative_to(resolved)
            root_name = rel.parts[0] if rel.parts else "."
        except ValueError:
            root_name = d.name
        groups.setdefault(root_name, []).append(d)

    if all_projects:
        for d in atlas_dirs:
            print(d)
        raise typer.Exit(0)

    # Default: output only directories under the scan root itself
    # (the scan root is typically one project like executive-assistant)
    for d in atlas_dirs:
        print(d)
    raise typer.Exit(0)


def _run_scan(
    path: Path,
    format: str = "human",
    show_tree: bool = False,
    export_format: str | None = None,
    has_abstract: bool = False,
    has_overview: bool = False,
    has_both: bool = False,
    depth: int | None = None,
    include_metadata: bool = False,
    show_stats: bool = False,
    validate: bool = False,
    find_orphans: bool = False,
    verbose: bool = False,
    debug: bool = False,
    quiet: bool = False,
) -> None:
    start_time = time.time()

    resolved_path = path.resolve()
    if not resolved_path.exists():
        console.print(f"[red]Error: Path not found: {resolved_path}[/red]")
        raise typer.Exit(1)

    if not resolved_path.is_dir():
        console.print(f"[red]Error: Not a directory: {resolved_path}[/red]")
        raise typer.Exit(1)

    config = ScannerConfig(
        root_path=resolved_path,
        max_depth=depth,
        has_abstract=has_abstract,
        has_overview=has_overview,
        has_both=has_both,
        quiet=quiet,
        verbose=verbose,
    )

    scanner = Scanner(config)

    if verbose:
        console.print(f"[dim]Scanning {resolved_path}...[/dim]")

    atlases = scanner.scan()

    parser = Parser(quiet=quiet)
    atlases = parser.parse_batch(atlases)

    all_errors = scanner.errors + parser.errors

    validator = Validator(quiet=quiet)
    if validate:
        validation_result = validator.validate(atlases)
        all_errors.extend(validation_result.errors)

    orphan_dirs: list[Path] = []
    if find_orphans:
        orphan_dirs = scanner.find_orphans(atlases)

    scan_time = time.time() - start_time

    result = ScanResult(
        atlases=atlases,
        orphans=orphan_dirs,
        errors=all_errors,
        stats={
            "scan_time_ms": int(scan_time * 1000),
            "atlases_found": len(atlases),
            "orphan_dirs": len(orphan_dirs),
            **scanner.stats,
        },
    )

    valid_formats = {"human", "json", "yaml", "toml", "plain"}
    if format not in valid_formats:
        console.print(
            f"[red]Error: Invalid format '{format}'. Valid formats: {', '.join(sorted(valid_formats))}[/red]"
        )
        raise typer.Exit(1)

    if show_tree:
        builder = TreeBuilder()
        tree_output = builder.build_ascii_tree(atlases)
        console.print(tree_output)
    elif export_format == "graphviz":
        exporter = Exporter(ExportConfig(format="human"))
        dot_output = exporter.export_graphviz(result)
        console.print(dot_output, markup=False)
    elif find_orphans:
        _output_orphans(orphan_dirs, format)
    else:
        exporter = Exporter(
            ExportConfig(
                format=format,
                include_metadata=include_metadata,
                show_stats=show_stats,
            )
        )
        output = exporter.export(result)
        console.print(output, markup=False)

    if not quiet:
        for error in all_errors:
            if error.code in (
                ErrorCode.E002,
                ErrorCode.E003,
                ErrorCode.E004,
                ErrorCode.E011,
            ):
                console.print(f"[yellow]Warning: {error}[/yellow]")
            else:
                console.print(f"[red]Error: {error}[/red]")

    if show_stats:
        stats_table = Table(title="Statistics")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        for key, value in result.stats.items():
            stats_table.add_row(key, str(value))
        console.print(stats_table)

    if not atlases and not find_orphans:
        console.print("[yellow]No atlas files found.[/yellow]")
        console.print("Try a different path or check --help for options.")
        raise typer.Exit(2)

    if validate and any(not a.is_valid for a in atlases):
        invalid_count = sum(1 for a in atlases if not a.is_valid)
        console.print(
            f"[red]Validation failed: {invalid_count} invalid atlas file(s)[/red]"
        )
        raise typer.Exit(3)


def _output_orphans(orphan_dirs: list[Path], format: str) -> None:
    if not orphan_dirs:
        console.print("[green]No orphan directories found.[/green]")
        return

    if format == "json":
        console.print(json.dumps([str(p) for p in orphan_dirs], indent=2), markup=False)
    else:
        console.print(
            f"[yellow]Orphan directories (missing atlases): {len(orphan_dirs)}[/yellow]\n"
        )
        for dir_path in sorted(orphan_dirs):
            console.print(f"  {dir_path}")


if __name__ == "__main__":
    app()
