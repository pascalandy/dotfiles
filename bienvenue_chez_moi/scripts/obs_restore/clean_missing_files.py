#!/usr/bin/env uv run python3
# /// script
# dependencies = [
#     "rich",
# ]
# ///

"""
Clean Missing Files Script

Reformats a list of missing files from an Obsidian vault export.
Extracts just the filename from lines like:
- [[Filename]] in [[location1]], [[location2]]

Usage:
    uv run clean_missing_files.py input_file.md [--output output_file.md]
"""

import argparse
import re
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def extract_filename(line: str) -> str | None:
    """
    Extract filename from a line containing Obsidian link format.

    Args:
        line: A line from the input file

    Returns:
        The extracted filename or None if no valid filename found
    """
    # Check if it's a list item with Obsidian link format
    # Pattern: - [[filename]] (optional "in [[location]]" part)
    match = re.match(r"^-\s*\[\[(.*?)\]\]", line.strip())
    if not match:
        return None

    filename = match.group(1)
    return filename if filename else None


def process_file(input_path: Path) -> str:
    """
    Process the input file and extract filenames from valid lines.

    Args:
        input_path: Path to the input file

    Returns:
        String containing the cleaned output

    Raises:
        FileNotFoundError: If the input file doesn't exist
    """
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    lines = input_path.read_text(encoding="utf-8").splitlines()
    result_lines = []

    for line in lines:
        filename = extract_filename(line)
        if filename:
            result_lines.append(f"- {filename}")

    return "\n".join(result_lines)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Clean Obsidian missing files list - extract just the filenames",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run clean_missing_files.py input.md
  uv run clean_missing_files.py input.md --output cleaned.md
  uv run clean_missing_files.py MISSING_FILES/missing_file_example.md --output cleaned_files.md
  uv run clean_missing_files.py input.md --dry-run

Input format:
  - [[Filename]] in [[location1]], [[location2]]
  - [[Simple File]]

Output format:
  - Filename
  - Simple File
        """,
    )
    parser.add_argument(
        "input_file", type=Path, help="Input file containing missing files list"
    )
    parser.add_argument(
        "--output", "-o", type=Path, help="Output file (default: print to stdout)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be extracted without writing to file",
    )
    return parser.parse_args()


def main() -> None:
    """Main workflow."""
    args = parse_args()

    # Process the file with progress indicator
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing file...", total=None)

        try:
            result = process_file(args.input_file)
            progress.update(task, description="✅ Processing complete")
        except FileNotFoundError as e:
            console.print(f"[red]Error: {e}[/red]")
            return
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            return

    # Output result
    if args.dry_run:
        # Read original lines and filter those that would be processed
        original_lines = args.input_file.read_text(encoding="utf-8").splitlines()
        before_lines = [line for line in original_lines if extract_filename(line)]
        before_content = "\n".join(before_lines).strip()
        console.print("[cyan]🔍 Dry run - showing before and after:[/cyan]")
        console.print("[bold]Before (lines to process):[/bold]")
        console.print(before_content, markup=False)
        console.print("\n[bold]After:[/bold]")
        console.print(result)
        if args.output:
            console.print(f"[dim]Would write to: {args.output}[/dim]")
    elif args.output:
        args.output.write_text(result, encoding="utf-8")
        console.print(f"[green]✅ Output written to: {args.output}[/green]")
    else:
        console.print(result)


if __name__ == "__main__":
    main()
