#!/usr/bin/env uv run python3
# /// script
# dependencies = [
#     "typer",
#     "rich",
# ]
# ///
"""
Scan projects in WORKDIR/ and IDEATION/ directories.
Outputs discovery.json with deterministic project enumeration and git metrics.

Usage:
    uv run WORKDIR/project_status/scan_projects.py
    uv run WORKDIR/project_status/scan_projects.py --dry-run
    uv run WORKDIR/project_status/scan_projects.py --help
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

SCRIPT_VERSION = "1.0.0"
REPO_URL = "https://github.com/username/forzr/issues"
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
WORKDIR = REPO_ROOT / "WORKDIR"
IDEATION = REPO_ROOT / "IDEATION"
OUTPUT_DIR = REPO_ROOT / "EXPORT" / "statut_de_projet"
HISTORIQUE_DIR = OUTPUT_DIR / "historique"

# Directories to ignore when counting files
IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".cache",
    ".history",
    "dist",
    "build",
    ".next",
    ".nuxt",
}

# Files to ignore
IGNORE_FILES = {".DS_Store", ".gitkeep", "Thumbs.db"}

app = typer.Typer(
    help="Scan projects and generate discovery.json for project status.",
    epilog=f"Examples:\n"
    f"  uv run WORKDIR/project_status/scan_projects.py\n"
    f"  uv run WORKDIR/project_status/scan_projects.py --dry-run\n"
    f"  uv run WORKDIR/project_status/scan_projects.py --days 14 --verbose\n"
    f"  uv run WORKDIR/project_status/scan_projects.py --json | jq '.totals'\n"
    f"\nReport bugs at: {REPO_URL}",
)


def generate_run_id() -> str:
    """Generate run ID in format: 2025_12_30_14h30_00_123456"""
    now = datetime.now()
    return now.strftime("%Y_%m_%d_%Hh%M_%S_%f")


def get_timestamp() -> str:
    """Get ISO timestamp."""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def find_session_files(project_path: Path) -> tuple[int, str | None]:
    """
    Find session files (session-ses_*.md) within subdirectories.
    Returns (count, latest_session_relative_path).
    """
    session_files: list[tuple[Path, float]] = []

    for md_file in project_path.rglob("session-ses_*.md"):
        # Skip if at project root (sessions are always in subdirs)
        if md_file.parent == project_path:
            continue
        session_files.append((md_file, md_file.stat().st_mtime))

    if not session_files:
        return 0, None

    # Sort by modification time, newest first
    session_files.sort(key=lambda x: x[1], reverse=True)
    latest = session_files[0][0]
    relative_path = str(latest.relative_to(project_path))

    return len(session_files), relative_path


def count_files_and_extensions(project_path: Path) -> tuple[int, list[str]]:
    """
    Count files and collect extensions, excluding ignored dirs/files.
    Returns (file_count, extensions_sorted_by_frequency).
    """
    extension_counter: Counter[str] = Counter()
    file_count = 0

    for file_path in project_path.rglob("*"):
        if not file_path.is_file():
            continue

        # Skip ignored directories
        if any(ignored in file_path.parts for ignored in IGNORE_DIRS):
            continue

        # Skip ignored files
        if file_path.name in IGNORE_FILES:
            continue

        file_count += 1
        ext = file_path.suffix.lower()
        if ext:
            extension_counter[ext] += 1

    # Sort by frequency (most common first)
    extensions = [ext for ext, _ in extension_counter.most_common()]

    return file_count, extensions


def collect_hints(project_path: Path) -> dict:
    """Collect all hints for a directory project."""
    session_count, latest_session = find_session_files(project_path)
    file_count, extensions = count_files_and_extensions(project_path)

    return {
        "has_0o0o": (project_path / "0o0o.md").exists(),
        "has_statut": (project_path / "statut.md").exists(),
        "has_session_file": session_count > 0,
        "session_count": session_count,
        "latest_session": latest_session,
        "has_tests": any(
            [
                (project_path / "tests").is_dir(),
                (project_path / "test").is_dir(),
                (project_path / "__tests__").is_dir(),
                any(project_path.rglob("*.test.*")),
                any(project_path.rglob("*.spec.*")),
            ]
        ),
        "has_readme": (project_path / "README.md").exists(),
        "has_ci": (project_path / ".github" / "workflows").is_dir(),
        "has_package_json": (project_path / "package.json").exists(),
        "has_pyproject": (project_path / "pyproject.toml").exists(),
        "file_count": file_count,
        "extensions": extensions,
    }


def scan_workdir() -> list[dict]:
    """Scan WORKDIR for subdirectories only."""
    projects = []

    if not WORKDIR.exists():
        return projects

    for item in sorted(WORKDIR.iterdir()):
        if not item.is_dir():
            continue
        if item.name.startswith("."):
            continue

        projects.append(
            {
                "path": f"WORKDIR/{item.name}",
                "name": item.name,
                "source": "workdir",
                "type": "directory",
                "hints": collect_hints(item),
            }
        )

    return projects


def scan_ideation() -> list[dict]:
    """Scan IDEATION for subdirectories and root .md files."""
    projects = []

    if not IDEATION.exists():
        return projects

    for item in sorted(IDEATION.iterdir()):
        if item.name.startswith("."):
            continue

        if item.is_dir():
            projects.append(
                {
                    "path": f"IDEATION/{item.name}",
                    "name": item.name,
                    "source": "ideation",
                    "type": "directory",
                    "hints": collect_hints(item),
                }
            )
        elif item.is_file() and item.suffix.lower() == ".md":
            projects.append(
                {
                    "path": f"IDEATION/{item.name}",
                    "name": item.stem,
                    "source": "ideation",
                    "type": "file",
                    "hints": None,
                }
            )

    return projects


def get_git_metrics(days: int = 7, verbose: bool = False) -> list[dict]:
    """Collect git metrics for the last N days."""
    metrics = []

    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")

        if verbose:
            print(f"[dim]Collecting metrics for {date_str}...[/dim]")

        # Get commit count
        try:
            result = subprocess.run(
                [
                    "git",
                    "log",
                    f"--since={date_str} 00:00",
                    f"--until={date_str} 23:59:59",
                    "--oneline",
                ],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
                check=True,
            )
            commits = (
                len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
            )
        except subprocess.CalledProcessError as e:
            commits = 0
            print(
                f"[yellow]Warning: git log failed for {date_str}: {e}[/yellow]",
                file=sys.stderr,
            )

        # Get file stats
        try:
            result = subprocess.run(
                [
                    "git",
                    "log",
                    f"--since={date_str} 00:00",
                    f"--until={date_str} 23:59:59",
                    "--numstat",
                    "--pretty=",
                ],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
                check=True,
            )
            lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        except subprocess.CalledProcessError as e:
            lines = []
            print(
                f"[yellow]Warning: git numstat failed for {date_str}: {e}[/yellow]",
                file=sys.stderr,
            )

        files_prod, files_tests = 0, 0
        added_prod, added_tests = 0, 0
        deleted_prod, deleted_tests = 0, 0

        for line in lines:
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                continue

            added_str, deleted_str, filepath = parts

            # Skip binary files (marked as -)
            if added_str == "-" or deleted_str == "-":
                continue

            try:
                added = int(added_str)
                deleted = int(deleted_str)
            except ValueError:
                continue

            # Classify as test or prod
            is_test = any(
                pattern in filepath
                for pattern in ["test/", "tests/", "__tests__/", ".test.", ".spec."]
            )

            if is_test:
                files_tests += 1
                added_tests += added
                deleted_tests += deleted
            else:
                files_prod += 1
                added_prod += added
                deleted_prod += deleted

        metrics.append(
            {
                "date": date_str,
                "commits": commits,
                "files": {
                    "prod": files_prod,
                    "tests": files_tests,
                    "total": files_prod + files_tests,
                },
                "lines_added": {
                    "prod": added_prod,
                    "tests": added_tests,
                    "total": added_prod + added_tests,
                },
                "lines_deleted": {
                    "prod": deleted_prod,
                    "tests": deleted_tests,
                    "total": deleted_prod + deleted_tests,
                },
                "net": (added_prod + added_tests) - (deleted_prod + deleted_tests),
            }
        )

    return metrics


def archive_old_runs(current_run_id: str, dry_run: bool = False) -> list[str]:
    """
    Move old STATUT_* folders to historique/.
    Returns list of archived folder names.
    """
    archived = []

    if not OUTPUT_DIR.exists():
        return archived

    # Ensure historique directory exists
    HISTORIQUE_DIR.mkdir(parents=True, exist_ok=True)

    for item in OUTPUT_DIR.iterdir():
        if not item.is_dir():
            continue
        if not item.name.startswith("STATUT_"):
            continue
        if item.name == f"STATUT_{current_run_id}":
            continue
        if item.name == "historique":
            continue

        archived.append(item.name)
        if not dry_run:
            dest = HISTORIQUE_DIR / item.name
            try:
                shutil.move(str(item), str(dest))
            except OSError as e:
                print(f"[red]Error archiving {item.name}: {e}[/red]")

    return archived


def display_summary(
    discovery: dict,
    output_path: Path | None = None,
    archived: list[str] | None = None,
    console: Console | None = None,
) -> None:
    """Display a summary table using rich."""
    if console is None:
        console = Console(force_terminal=None)
    totals = discovery["totals"]

    table = Table(title="Project Scan Summary")
    table.add_column("Category", style="cyan")
    table.add_column("Count", justify="right", style="green")

    table.add_row("WORKDIR", str(totals["workdir"]))
    table.add_row("IDEATION (dirs)", str(totals["ideation_dirs"]))
    table.add_row("IDEATION (files)", str(totals["ideation_files"]))
    table.add_row("Total", str(totals["total"]), style="bold")

    console.print(table)

    if archived:
        console.print(
            f"\nArchived: [dim]{len(archived)} old run(s) moved to historique/[/dim]"
        )

    if output_path:
        console.print(f"\nRun ID: [bold]{discovery['meta']['run_id']}[/bold]")
        console.print(f"Output: [dim]{output_path}[/dim]")


@app.command()
def main(
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Show what would be scanned without writing files.",
    ),
    days: int = typer.Option(
        7,
        "--days",
        "-d",
        help="Number of days to collect git metrics for.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-essential output.",
    ),
    plain: bool = typer.Option(
        False,
        "--plain",
        help="Output plain text table (no colors, no styling).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON to stdout (machine-readable, no progress).",
    ),
    no_color: bool = typer.Option(
        False,
        "--no-color",
        help="Disable colored output (respects NO_COLOR and TERM=dumb).",
    ),
    output: Path | None = typer.Option(  # noqa: B008
        None,
        "--output",
        "-o",
        help="Output directory for discovery.json (default: auto-generated).",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        help="Show version and exit.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug mode with stack traces.",
    ),
    latest: bool = typer.Option(
        False,
        "--latest",
        "-l",
        help="Show the most recent scan result without re-scanning.",
    ),
) -> None:
    """
    Scan WORKDIR/ and IDEATION/ directories for projects.

    Generates discovery.json with project enumeration, hints, and git metrics.

        Examples:
        uv run WORKDIR/project_status/scan_projects.py
        uv run WORKDIR/project_status/scan_projects.py --dry-run
        uv run WORKDIR/project_status/scan_projects.py --days 14 --verbose
    """
    import os

    if debug:
        os.environ["DEBUG"] = "1"

    # Handle color settings
    if no_color or os.environ.get("NO_COLOR") or os.environ.get("TERM") == "dumb":
        console = Console(force_terminal=False)
        console_err = Console(stderr=True, force_terminal=False)
    elif os.environ.get("FORCE_COLOR"):
        console = Console(force_terminal=True, color_system="auto")
        console_err = Console(stderr=True, force_terminal=True, color_system="auto")
    else:
        console = Console(force_terminal=None)
        console_err = Console(stderr=True, force_terminal=None)

    if version:
        console.print(f"scan_projects.py version {SCRIPT_VERSION}")
        raise SystemExit(0)

    # Handle --latest flag
    if latest:
        if not OUTPUT_DIR.exists():
            console_err.print(
                "[red]No scan results found. Run without --latest first.[/red]"
            )
            raise SystemExit(1)
        # Find the most recent STATUT_* directory
        if not OUTPUT_DIR.exists():
            console_err.print(
                "[red]No scan results found. Run without --latest first.[/red]"
            )
            raise SystemExit(1)
        stat_dirs = [
            d
            for d in OUTPUT_DIR.iterdir()
            if d.is_dir() and d.name.startswith("STATUT_") and d.name != "historique"
        ]
        if not stat_dirs:
            console_err.print(
                "[red]No scan results found. Run without --latest first.[/red]"
            )
            raise SystemExit(1)
        latest_dir = max(item.name for item in stat_dirs)
        latest_path = OUTPUT_DIR / latest_dir / "discovery.json"
        if not latest_path.exists():
            console_err.print(f"[red]discovery.json not found in {latest_dir}[/red]")
            raise SystemExit(1)
        try:
            with open(latest_path, encoding="utf-8") as f:
                discovery = json.load(f)
        except OSError as e:
            console_err.print(f"[red]Error reading {latest_path}: {e}[/red]")
            raise SystemExit(1) from e
        if json_output:
            json.dump(discovery, sys.stdout, indent=2, ensure_ascii=False)
            raise SystemExit(0)
        if not quiet:
            if plain:
                print(f"WORKDIR: {discovery['totals']['workdir']}")
                print(f"IDEATION (dirs): {discovery['totals']['ideation_dirs']}")
                print(f"IDEATION (files): {discovery['totals']['ideation_files']}")
                print(f"Total: {discovery['totals']['total']}")
                print(f"Run ID: {discovery['meta']['run_id']}")
                print(f"Output: {latest_path}")
                print("\nNext: uv run WORKDIR/project_status/scan_projects.py --latest")
            else:
                display_summary(discovery, latest_path, console=console)
                console.print(
                    "\n[dim]Next:[/dim] [cyan]uv run WORKDIR/project_status/scan_projects.py --latest[/cyan]"
                )
        raise SystemExit(0)

    run_id = generate_run_id()
    timestamp = get_timestamp()

    if verbose and not quiet:
        console.print(f"[dim]Starting scan at {timestamp}...[/dim]")

    workdir_projects = scan_workdir()
    ideation_projects = scan_ideation()
    all_projects = workdir_projects + ideation_projects

    ideation_dirs = sum(1 for p in ideation_projects if p["type"] == "directory")
    ideation_files = sum(1 for p in ideation_projects if p["type"] == "file")

    discovery = {
        "meta": {
            "run_id": run_id,
            "timestamp": timestamp,
            "script_version": SCRIPT_VERSION,
        },
        "totals": {
            "workdir": len(workdir_projects),
            "ideation_dirs": ideation_dirs,
            "ideation_files": ideation_files,
            "total": len(all_projects),
        },
        "projects": all_projects,
        "git_metrics": get_git_metrics(days=days, verbose=verbose),
    }

    if json_output:
        json.dump(discovery, sys.stdout, indent=2, ensure_ascii=False)
        raise SystemExit(0)

    if dry_run:
        if not quiet:
            console.print("[yellow]Dry run mode - no files written[/yellow]\n")
        archived = archive_old_runs(run_id, dry_run=True)
        if not quiet:
            display_summary(discovery, archived=archived, console=console)
            if archived:
                console.print(f"[dim]Would archive: {', '.join(archived)}[/dim]")
        return

    archived = archive_old_runs(run_id, dry_run=False)

    if output:
        output_path = output / "discovery.json"
        run_dir = output
    else:
        run_dir = OUTPUT_DIR / f"STATUT_{run_id}"
        output_path = run_dir / "discovery.json"

    run_dir.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(discovery, f, indent=2, ensure_ascii=False)
    except OSError as e:
        console_err.print(
            f"[red]Error writing to {output_path}: {e}[/red]\n"
            f"[yellow]Check that the directory exists and you have write permissions.[/yellow]\n"
            f"[dim]Report bugs at: {REPO_URL} (include the error above)[/dim]"
        )
        raise SystemExit(1) from e

    if verbose and not quiet:
        console.print(f"[green]Created {output_path}[/green]")

    if not quiet:
        if plain:
            print(f"WORKDIR: {discovery['totals']['workdir']}")
            print(f"IDEATION (dirs): {discovery['totals']['ideation_dirs']}")
            print(f"IDEATION (files): {discovery['totals']['ideation_files']}")
            print(f"Total: {discovery['totals']['total']}")
            if archived:
                print(f"Archived: {len(archived)} old run(s) moved to historique/")
            print(f"Run ID: {run_id}")
            print(f"Output: {output_path}")
            print("\nNext: uv run WORKDIR/project_status/scan_projects.py --latest")
        else:
            display_summary(discovery, output_path, archived, console=console)
            console.print(
                "\n[dim]Next:[/dim] [cyan]uv run WORKDIR/project_status/scan_projects.py --latest[/cyan]"
            )


if __name__ == "__main__":
    raise SystemExit(app())
