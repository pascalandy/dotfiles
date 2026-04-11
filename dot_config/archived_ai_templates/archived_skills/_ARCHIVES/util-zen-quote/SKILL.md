---
name: zen-quote
description: "Fetch inspirational quotes from Zen Quotes API. Use when the user asks for: (1) Random inspirational quote, (2) Daily quote, (3) Quotes by specific author, (4) Search quotes by keyword. Triggers: 'give me a quote', 'inspire me', 'zen quote', 'motivational quote', 'quote of the day'."
---

# Zen Quote

Fetch inspirational quotes from the [Zen Quotes API](https://zenquotes.io/).

## Usage

Run the script via `uv run`:

```bash
uv run scripts/zen_quote.py                     # Daily quote (default)
uv run scripts/zen_quote.py --random            # Random quote
uv run scripts/zen_quote.py --random --count 5  # Multiple random quotes
uv run scripts/zen_quote.py --author "Einstein" # Quotes by author
uv run scripts/zen_quote.py --search "wisdom"   # Search by keyword
uv run scripts/zen_quote.py --daily             # Today's quote
```

## Options

| Flag               | Description                        |
| ------------------ | ---------------------------------- |
| `--random`         | Get random quote(s)                |
| `--daily`          | Get the daily inspirational quote  |
| `--author NAME`    | Get quotes by specific author      |
| `--search KEYWORD` | Search quotes containing keyword   |
| `--count N`        | Number of quotes to fetch (max 10) |
