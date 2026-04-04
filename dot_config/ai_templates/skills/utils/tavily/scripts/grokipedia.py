#!/usr/bin/env uv run python3
# /// script
# dependencies = [
#     "httpx>=0.27",
#     "rich>=13.0",
# ]
# ///
# -*- coding: utf-8 -*-
"""
Search Grokipedia.com using Tavily API.

Usage:
    uv run grokipedia.py "quantum computing"
    uv run grokipedia.py "Italian cuisine" --max-results 10
    uv run grokipedia.py "AI history" --raw
    uv run grokipedia.py "neural networks" --json | jq '.results[].url'
"""

import argparse
import json
import subprocess
import sys
from typing import Any

import httpx
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

__version__ = "0.1.0"

TAVILY_API_URL = "https://api.tavily.com/search"
SEARCH_DOMAINS = ["grokipedia.com", "grokxpedia.us"]

# Separate consoles: stdout for data, stderr for diagnostics
out = Console()
err = Console(stderr=True)


def get_api_key() -> str:
    """Retrieve Tavily API key from macOS keyring via chezmoi."""
    try:
        result = subprocess.run(
            [
                "chezmoi",
                "secret",
                "keyring",
                "get",
                "--service=tavily",
                "--user=api_key",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except FileNotFoundError:
        err.print("[red]Error: chezmoi not found in PATH[/red]")
        err.print("  Install chezmoi: https://www.chezmoi.io/install/")
        sys.exit(1)
    except subprocess.CalledProcessError:
        err.print("[red]Error: Could not retrieve Tavily API key from keyring[/red]")
        err.print(
            "  Set it with: chezmoi secret keyring set --service=tavily --user=api_key"
        )
        sys.exit(1)


def search_grokipedia(
    query: str, max_results: int = 5, include_raw: bool = False
) -> dict[str, Any]:
    """Search grokipedia.com using Tavily API with include_domains filter.

    Args:
        query: Search query string.
        max_results: Maximum number of results (1-20).
        include_raw: Whether to include raw page content.

    Returns:
        Tavily API response as a dictionary.

    Raises:
        httpx.HTTPStatusError: On non-2xx response.
        httpx.RequestError: On connection/timeout failure.
    """
    api_key = get_api_key()

    payload = {
        "query": query,
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": True,
        "include_raw_content": include_raw,
        "include_domains": SEARCH_DOMAINS,
        "topic": "general",
    }

    with httpx.Client(timeout=30.0) as client:
        response = client.post(
            TAVILY_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        return response.json()


def display_results(data: dict[str, Any], raw: bool = False) -> None:
    """Display search results with rich formatting.

    Args:
        data: Tavily API response dictionary.
        raw: Whether to show raw page content.
    """
    query = data.get("query", "Unknown")
    answer = data.get("answer")
    results = data.get("results", [])

    # Header
    out.print(
        Panel(
            f"[bold cyan]Query:[/bold cyan] {query}\n"
            f"[dim]Domains: {', '.join(SEARCH_DOMAINS)}[/dim]",
            title="[bold green]Grokipedia Search via Tavily[/bold green]",
            border_style="green",
        )
    )

    # AI Answer
    if answer:
        out.print(
            Panel(
                Markdown(answer),
                title="[bold yellow]AI Summary[/bold yellow]",
                border_style="yellow",
            )
        )

    # Results
    if not results:
        out.print("[yellow]No results found on grokipedia.com[/yellow]")
        return

    out.print(f"\n[bold]Found {len(results)} result(s):[/bold]\n")

    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        url = result.get("url", "")
        content = result.get("content", "")
        score = result.get("score", 0)

        title_text = Text()
        title_text.append(f"{i}. ", style="bold cyan")
        title_text.append(title, style="bold white underline")
        out.print(title_text)
        out.print(f"   [dim]{url}[/dim]")
        out.print(f"   [dim]Relevance: {score:.2f}[/dim]")

        if content:
            snippet = content[:300] + "..." if len(content) > 300 else content
            out.print(Panel(snippet, border_style="dim", padding=(0, 2)))

        if raw and result.get("raw_content"):
            out.print("[dim]--- Raw Content ---[/dim]")
            raw_text = result["raw_content"]
            out.print(raw_text[:500] + "..." if len(raw_text) > 500 else raw_text)

        out.print()

    # Footer
    response_time = data.get("response_time", 0)
    out.print(f"[dim]Response time: {response_time:.2f}s[/dim]")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Search Grokipedia.com using Tavily API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  uv run grokipedia.py "quantum physics"
  uv run grokipedia.py "Italian cuisine" -n 10
  uv run grokipedia.py "AI history" --raw
  uv run grokipedia.py "neural networks" --json | jq '.results[].url'
""",
    )

    parser.add_argument(
        "query",
        help="Search query (e.g., 'quantum computing')",
    )

    parser.add_argument(
        "-n",
        "--max-results",
        type=int,
        default=5,
        help="Maximum number of results (default: 5, max: 20)",
    )

    parser.add_argument(
        "--raw",
        action="store_true",
        help="Include raw content from pages",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output raw JSON instead of formatted results",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 success, 1 runtime error, 2 validation error.
    """
    args = parse_arguments()

    # Validate inputs before doing any work
    if args.max_results < 1 or args.max_results > 20:
        err.print(
            f"[red]Error: --max-results must be 1-20, got {args.max_results}[/red]"
        )
        err.print('  uv run grokipedia.py "your query" -n 5')
        return 2

    try:
        data = search_grokipedia(
            query=args.query,
            max_results=args.max_results,
            include_raw=args.raw,
        )

        if args.json_output:
            print(json.dumps(data, indent=2))
        else:
            display_results(data, raw=args.raw)

        return 0

    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        err.print(f"[red]Error: Tavily API returned HTTP {status}[/red]")
        if status in (401, 403):
            err.print(
                "  Verify API key: chezmoi secret keyring get --service=tavily --user=api_key"
            )
        elif status == 429:
            err.print("  Rate limited. Wait a moment and retry.")
        else:
            err.print(f"  Response: {e.response.text[:200]}")
        return 1

    except httpx.RequestError as e:
        err.print(f"[red]Error: Could not reach Tavily API[/red]")
        err.print(f"  {e}")
        err.print("  Check your internet connection and try again.")
        return 1

    except KeyboardInterrupt:
        err.print("\n[dim]Interrupted[/dim]")
        return 130


if __name__ == "__main__":
    sys.exit(main())
