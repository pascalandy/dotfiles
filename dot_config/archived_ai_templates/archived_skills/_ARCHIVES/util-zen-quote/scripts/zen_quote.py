#!/usr/bin/env uv run python3
# /// script
# dependencies = [
# ]
# ///
"""
Dynamic quotes script using Zen Quotes API.

Usage:
    uv run python3 zen_quotes.py
    uv run python3 zen_quotes.py --author "Author Name"
    uv run python3 zen_quotes.py --search "wisdom"
    uv run python3 zen_quotes.py --random --count 5
    chmod +x zen_quotes.py, then: ./zen_quotes.py

Examples:
    uv run python3 zen_quotes.py
    uv run python3 zen_quotes.py --author "Albert Einstein"
    uv run python3 zen_quotes.py --search "motivation"
    uv run python3 zen_quotes.py --random --count 3

Zen Quotes API: https://zenquotes.io/
"""

import argparse
import json
import random
import sys
import urllib.parse
import urllib.request


def fetch_random_quote() -> dict:
    """Fetch a random quote from Zen Quotes."""
    try:
        url = "https://zenquotes.io/api/random"

        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise urllib.error.HTTPError(url, response.status, "HTTP Error", {}, None)
            data = json.loads(response.read().decode())

        # API returns a list with one quote
        if not data or not isinstance(data, list):
            raise ValueError("Invalid response from quotes API")

        return data[0]

    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to connect to quotes service: {e}") from e
    except json.JSONDecodeError:
        raise ValueError("Invalid response from quotes service") from None


def fetch_quotes_by_author(author: str) -> list:
    """Fetch quotes by specific author from Zen Quotes."""
    try:
        # First get the author's quotes
        url = "https://zenquotes.io/api/quotes"

        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise urllib.error.HTTPError(url, response.status, "HTTP Error", {}, None)
            data = json.loads(response.read().decode())

        if not data or not isinstance(data, list):
            raise ValueError("Invalid response from quotes API")

        # Filter quotes by author (case-insensitive)
        author_lower = author.lower()
        author_quotes = []

        for quote in data:
            if quote.get("a", "").lower() == author_lower:
                author_quotes.append(quote)

        return author_quotes

    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to connect to quotes service: {e}") from e
    except json.JSONDecodeError:
        raise ValueError("Invalid response from quotes service") from None


def search_quotes(query: str) -> list:
    """Search quotes containing specific keywords from Zen Quotes."""
    try:
        # Get all quotes and filter client-side
        url = "https://zenquotes.io/api/quotes"

        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise urllib.error.HTTPError(url, response.status, "HTTP Error", {}, None)
            data = json.loads(response.read().decode())

        if not data or not isinstance(data, list):
            raise ValueError("Invalid response from quotes API")

        # Search in both quote text and author name
        query_lower = query.lower()
        matching_quotes = []

        for quote in data:
            quote_text = quote.get("q", "").lower()
            author = quote.get("a", "").lower()

            if query_lower in quote_text or query_lower in author:
                matching_quotes.append(quote)

        return matching_quotes

    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to connect to quotes service: {e}") from e
    except json.JSONDecodeError:
        raise ValueError("Invalid response from quotes service") from None


def fetch_daily_quote() -> dict:
    """Fetch the daily quote from Zen Quotes."""
    try:
        url = "https://zenquotes.io/api/today"

        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise urllib.error.HTTPError(url, response.status, "HTTP Error", {}, None)
            data = json.loads(response.read().decode())

        # API returns a list with one quote
        if not data or not isinstance(data, list):
            raise ValueError("Invalid response from quotes API")

        return data[0]

    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to connect to quotes service: {e}") from e
    except json.JSONDecodeError:
        raise ValueError("Invalid response from quotes service") from None


def display_quote(quote_data: dict, index: int | None = None, total: int | None = None):
    """Display a single quote with formatting."""
    quote_text = quote_data.get("q", "No quote text available")
    author = quote_data.get("a", "Unknown Author")

    # Add quotes around the text
    formatted_text = f'"{quote_text}"'

    # Add author attribution
    formatted_author = f"— {author}"

    # Add index if multiple quotes
    if index is not None and total is not None:
        print(f"\n[{index}/{total}] {formatted_text}")
        print(f"     {formatted_author}")
    else:
        print(f"\n📝 {formatted_text}")
        print(f"     {formatted_author}")


def display_quotes(quotes: list, title: str = "Quotes"):
    """Display multiple quotes with nice formatting."""
    if not quotes:
        print(f"No quotes found for: {title}")
        return

    print(f"\n📚 {title}")
    print("=" * 80)

    for i, quote in enumerate(quotes, 1):
        display_quote(quote, i, len(quotes))


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Get inspirational quotes using Zen Quotes API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Get daily quote
  %(prog)s --random           # Get random quote
  %(prog)s --author "Einstein"
  %(prog)s --search "wisdom"
  %(prog)s --random --count 5 # Get 5 random quotes
  %(prog)s --author "Steve Jobs" --count 3

Available Options:
  --random      Get random quotes (default: 1 quote)
  --author      Get quotes by specific author
  --search      Search quotes by keyword
  --count       Number of quotes to fetch (default: 1)
  --daily       Get the daily inspirational quote
        """,
    )

    parser.add_argument(
        "--author",
        help="Get quotes by specific author (e.g., 'Albert Einstein', 'Steve Jobs')",
    )
    parser.add_argument("--search", help="Search quotes containing specific keywords")
    parser.add_argument(
        "--random", action="store_true", help="Get random quote(s) (default behavior)"
    )
    parser.add_argument("--daily", action="store_true", help="Get the daily inspirational quote")
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of quotes to fetch (default: 1, max: 10 for random quotes)",
    )

    args = parser.parse_args()

    try:
        # Determine which mode to use
        if args.daily:
            print("Fetching today's inspirational quote...")
            quote = fetch_daily_quote()
            display_quote(quote)
            return

        elif args.author:
            print(f"Fetching quotes by {args.author}...")
            quotes = fetch_quotes_by_author(args.author)

            if not quotes:
                print(f"No quotes found by author: {args.author}")
                print("Tip: Check the spelling or try a different author name.")
                sys.exit(1)

            # Limit results for better readability
            if len(quotes) > 10:
                quotes = random.sample(quotes, 10)

            display_quotes(quotes, f"Quotes by {args.author}")

        elif args.search:
            print(f"Searching quotes for: '{args.search}'...")
            quotes = search_quotes(args.search)

            if not quotes:
                print(f"No quotes found containing: '{args.search}'")
                print("Tip: Try different keywords or check the spelling.")
                sys.exit(1)

            # Limit results for better readability
            if len(quotes) > 10:
                quotes = random.sample(quotes, 10)

            display_quotes(quotes, f"Search results for '{args.search}'")

        else:  # Random quotes (default)
            print("Fetching inspirational quote(s)...")

            # Validate count
            if args.count > 10:
                print("Maximum 10 quotes allowed per request. Limiting to 10.")
                args.count = 10
            elif args.count < 1:
                print("Count must be at least 1. Setting to 1.")
                args.count = 1

            if args.count == 1:
                quote = fetch_random_quote()
                display_quote(quote)
            else:
                all_quotes = []
                for _i in range(args.count):
                    quote = fetch_random_quote()
                    all_quotes.append(quote)

                display_quotes(all_quotes, "Random Inspirational Quotes")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ConnectionError as e:
        print(f"Connection Error: {e}", file=sys.stderr)
        print("Please check your internet connection and try again.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
