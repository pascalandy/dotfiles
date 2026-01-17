#!/usr/bin/env uv run python3
# /// script
# dependencies = [
#     "rich",
# ]
# # ///
"""
Orchestrator for project status analysis.
Coordinates multi-agent workflow: discovery → analysis → report → post-mortem → commit.

Usage:
    uv run .opencode/skill/project_status/orchestrator.py
    uv run .opencode/skill/project_status/orchestrator.py --dry-run
    uv run .opencode/skill/project_status/orchestrator.py --no-commit
"""

from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import as_completed, ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent.parent
WORKDIR = REPO_ROOT / "WORKDIR"
IDEATION = REPO_ROOT / "IDEATION"
OUTPUT_DIR = REPO_ROOT / "EXPORT" / "statut_de_projet"

ANALYSIS_PROMPT = SCRIPT_DIR / "ANALYSIS_PROMPT.md"
TEMPLATE = SCRIPT_DIR / "TEMPLATE.md"
SCAN_SCRIPT = SCRIPT_DIR / "scan_projects.py"

# Agent aliases for fallback
L1_MODEL = "claude-3-5-sonnet-20241022"
L2_MODEL = "claude-3-5-sonnet-20241022"
L3_MODEL = "claude-3-5-sonnet-20241022"
ORACLE_MODEL = "claude-3-5-sonnet-20241022"

MAX_PARALLEL = 9
TIMEOUT = 60

console = Console()


def run_step_0() -> tuple[str, dict]:
    """Step 0: Pre-scan projects."""
    console.print("\n[bold cyan]Step 0: Pre-scan[/bold cyan]")
    console.print(f"Running: uv run {SCAN_SCRIPT.relative_to(REPO_ROOT)}")

    result = subprocess.run(
        ["uv", "run", str(SCAN_SCRIPT)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )

    if result.returncode != 0:
        console.print(f"[red]Error running scan script:[/red]\n{result.stderr}")
        raise SystemExit(1)

    output = json.loads(result.stdout)
    run_id = output["meta"]["run_id"]
    discovery = output

    console.print(f"[green]Run ID: {run_id}[/green]")
    console.print(f"Projects found: {discovery['totals']['total']}")

    return run_id, discovery


def analyze_project(project: dict, analysis_prompt: str) -> dict | None:
    """Analyze a single project using agent."""
    path = project["path"]
    name = project["name"]
    project_type = project["type"]
    hints = project.get("hints", {})

    prompt = analysis_prompt.replace("<PATH>", path).replace("<name>", name)
    prompt = prompt.replace("<directory|file>", project_type)
    prompt = prompt.replace("<hints object or null>", json.dumps(hints, indent=2))

    if hints and "latest_session" in hints and hints["latest_session"]:
        prompt = prompt.replace("<latest_session>", hints["latest_session"])
    else:
        prompt = prompt.replace("<latest_session>", "None")

    try:
        result = subprocess.run(
            [
                "opencode",
                "agent",
                L1_MODEL,
                "--",
                prompt,
            ],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=TIMEOUT,
        )

        if result.returncode != 0:
            console.print(f"[yellow]Failed to analyze {name}: {result.stderr}[/yellow]")
            return None

        analysis = json.loads(result.stdout)
        analysis["path"] = path
        analysis["name"] = name
        return analysis

    except subprocess.TimeoutExpired:
        console.print(f"[yellow]Timeout analyzing {name}[/yellow]")
        return None
    except json.JSONDecodeError as e:
        console.print(f"[yellow]Invalid JSON for {name}: {e}[/yellow]")
        return None
    except Exception as e:
        console.print(f"[yellow]Error analyzing {name}: {e}[/yellow]")
        return None


def run_step_1(discovery: dict, analysis_prompt: str) -> list[dict]:
    """Step 1: Analyze all projects in parallel."""
    console.print("\n[bold cyan]Step 1: Analysis[/bold cyan]")
    console.print(
        f"Analyzing {discovery['totals']['total']} projects (max {MAX_PARALLEL} parallel)"
    )

    projects = discovery["projects"]
    analyses = []

    with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as executor:
        future_to_project = {
            executor.submit(analyze_project, p, analysis_prompt): p for p in projects
        }

        for future in as_completed(future_to_project):
            project = future_to_project[future]
            try:
                result = future.result()
                if result:
                    analyses.append(result)
                    console.print(f"[green]✓[/green] {project['name']}")
                else:
                    console.print(f"[red]✗[/red] {project['name']} (failed)")
            except Exception as e:
                console.print(f"[red]✗[/red] {project['name']} ({e})")

    console.print(f"\n[green]Analyzed {len(analyses)}/{len(projects)} projects[/green]")
    return analyses


def run_step_2(analyses: list[dict], discovery: dict, template: str) -> str:
    """Step 2: Write STATUT.md using L3 agent."""
    console.print("\n[bold cyan]Step 2: Report generation[/bold cyan]")

    prompt = f"""
Using the following template, write STATUT.md:

{template}

Input data:
- Run ID: {discovery["meta"]["run_id"]}
- Timestamp: {discovery["meta"]["timestamp"]}
- Projects analyzed: {len(analyses)}
- Projects total: {discovery["totals"]["total"]}
- Git metrics: {json.dumps(discovery["git_metrics"], indent=2)}
- Analyses: {json.dumps(analyses, indent=2)}

Output ONLY the STATUT.md content, nothing else.
"""

    try:
        result = subprocess.run(
            ["opencode", "agent", L3_MODEL, "--", prompt],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=TIMEOUT,
        )

        if result.returncode != 0:
            console.print(f"[red]Error generating report:[/red]\n{result.stderr}")
            raise SystemExit(1)

        return result.stdout

    except subprocess.TimeoutExpired:
        console.print("[red]Timeout generating report[/red]")
        raise SystemExit(1)


def run_step_3(
    statut_path: Path,
    start_time: datetime,
    analyzed: int,
    total: int,
    failures: list[str],
) -> None:
    """Step 3: Append post-mortem."""
    console.print("\n[bold cyan]Step 3: Post-mortem[/bold cyan]")

    end_time = datetime.now()
    duration = end_time - start_time
    hours = int(duration.total_seconds() // 3600)
    minutes = int((duration.total_seconds() % 3600) // 60)
    seconds = int(duration.total_seconds() % 60)
    duration_str = f"{hours}h {minutes}m {seconds}s"

    post_mortem = f"""

## Post-mortem

- **Duration**: {duration_str}
- **Projects analyzed**: {analyzed}/{total}
- **Agent failures**: {len(failures)}
"""

    if failures:
        post_mortem += "\n\n**Failed projects**:\n"
        for failure in failures:
            post_mortem += f"- {failure}\n"

    with open(statut_path, "a", encoding="utf-8") as f:
        f.write(post_mortem)

    console.print("[green]Post-mortem appended[/green]")


def run_step_4(run_id: str, statut_path: Path, discovery_path: Path) -> None:
    """Step 4: Commit files."""
    console.print("\n[bold cyan]Step 4: Commit[/bold cyan]")

    date = datetime.now().strftime("%Y-%m-%d")
    total_files = len(json.loads(discovery_path.read_text())["projects"])

    message = f"chore(status): update project status {date} ({total_files}/{total_files} projects)"

    subprocess.run(
        ["git", "add", str(statut_path), str(discovery_path)],
        cwd=REPO_ROOT,
        check=True,
    )

    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=REPO_ROOT,
        check=True,
    )

    console.print(f"[green]Committed: {message}[/green]")


def main(
    dry_run: bool = False,
    no_commit: bool = False,
) -> None:
    """Main orchestrator workflow."""
    start_time = datetime.now()
    console.print(Panel.fit("Project Status Orchestrator", style="bold magenta"))

    # Step 0: Pre-scan
    run_id, discovery = run_step_0()
    run_dir = OUTPUT_DIR / f"STATUT_{run_id}"
    discovery_path = run_dir / "discovery.json"

    # Step 1: Analysis
    analysis_prompt = ANALYSIS_PROMPT.read_text()
    analyses = run_step_1(discovery, analysis_prompt)

    failures = [
        p["name"]
        for p in discovery["projects"]
        if p["name"] not in [a["name"] for a in analyses]
    ]

    # Step 2: Report
    template = TEMPLATE.read_text()
    statut_content = run_step_2(analyses, discovery, template)

    if dry_run:
        console.print("\n[yellow]Dry run - not writing files[/yellow]")
        console.print(f"\nSTATUT.md preview:\n{statut_content[:500]}...")
        return

    statut_path = run_dir / "STATUT.md"
    statut_path.write_text(statut_content, encoding="utf-8")
    console.print(f"[green]Wrote {statut_path}[/green]")

    # Step 3: Post-mortem
    run_step_3(
        statut_path, start_time, len(analyses), discovery["totals"]["total"], failures
    )

    # Step 4: Commit
    if not no_commit:
        run_step_4(run_id, statut_path, discovery_path)

    # Step 5: Summary
    end_time = datetime.now()
    duration = end_time - start_time
    hours = int(duration.total_seconds() // 3600)
    minutes = int((duration.total_seconds() % 3600) // 60)
    seconds = int(duration.total_seconds() % 60)

    console.print("\n[bold green]Complete![/bold green]")
    console.print(f"Folder: {run_dir.relative_to(REPO_ROOT)}")
    console.print(f"Files: STATUT.md + discovery.json")
    if not no_commit:
        console.print(
            f"Commit: chore(status): update project status {end_time.strftime('%Y-%m-%d')} ({len(analyses)}/{discovery['totals']['total']})"
        )
    console.print(f"Duration: {hours}h {minutes}m {seconds}s")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Project status orchestrator")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Dry run mode")
    parser.add_argument("--no-commit", action="store_true", help="Skip git commit")

    args = parser.parse_args()
    main(dry_run=args.dry_run, no_commit=args.no_commit)
