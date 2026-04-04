---
name: FetchSeries
description: Fetch historical data for individual FRED series with multi-timeframe trend statistics. USE WHEN fetch FRED series, series history, individual metric, get UNRATE, get GDP, specific indicator, trend for CPI, single metric lookup, FRED data, historical data, one metric.
---

# FetchSeries

Fetch historical data from FRED (Federal Reserve Economic Data) for individual economic series with configurable time ranges and trend calculations.

## Overview

Use this sub-skill when you need historical data or trend statistics for a specific economic indicator rather than a full economic overview. Supports all FRED series IDs and includes 40+ pre-configured core series.

## Script

| Script | Purpose |
|--------|---------|
| `scripts/FetchFredSeries.ts` | Fetches historical observations and calculates trend statistics |

## Usage

Fetch a single series:

```bash
bun scripts/FetchFredSeries.ts UNRATE
```

Fetch with custom history length:

```bash
bun scripts/FetchFredSeries.ts GDPC1 --years=20
```

Fetch with trend analysis:

```bash
bun scripts/FetchFredSeries.ts CPIAUCSL --trends
```

Fetch all core series as JSON:

```bash
bun scripts/FetchFredSeries.ts --all --json > data.json
```

## Options

| Flag | Default | Purpose |
|------|---------|---------|
| `--years=N` | 10 | Number of years of historical data to fetch |
| `--all` | false | Fetch all 40+ core series |
| `--json` | false | Output as JSON (machine-readable) |
| `--trends` | false | Include 10y/5y/2y/1y trend calculations |
| `-h, --help` | | Show usage help |

## Output (Human-Readable)

```
============================================================
Unemployment Rate (UNRATE)
Category: Employment
Unit: Percent
Latest: 4.1 (2026-02-01)
Range: 3.4 - 14.7
Mean: 4.8
Observations: 120

Trend Analysis:
  10y: 5.8 -> 4.1 (-29.3% down)
  5y:  3.5 -> 4.1 (+17.1% up)
  2y:  3.7 -> 4.1 (+10.8% up)
  1y:  3.9 -> 4.1 (+5.1% up)
```

## Output (JSON)

With `--json`, returns an array of objects:

```json
[
  {
    "series_id": "UNRATE",
    "name": "Unemployment Rate (U-3)",
    "category": "Employment",
    "unit": "Percent",
    "observations": [{"date": "2016-01-01", "value": 4.9}, ...],
    "latest": {"date": "2026-02-01", "value": 4.1},
    "stats": {"min": 3.4, "max": 14.7, "mean": 4.8, "count": 120},
    "trends": {
      "10y": {"startValue": 5.8, "endValue": 4.1, "percentChange": -29.3, "direction": "down"},
      "5y": {"startValue": 3.5, "endValue": 4.1, "percentChange": 17.1, "direction": "up"}
    }
  }
]
```

## Trend Calculations

For each timeframe (10y, 5y, 2y, 1y), the script calculates:

| Statistic | Description |
|-----------|-------------|
| Start Value | Value at the beginning of the period |
| End Value | Most recent value |
| Absolute Change | End minus start |
| Percent Change | Percentage change from start |
| CAGR | Compound annual growth rate |
| Direction | Up, Down, or Stable (threshold: 2% change) |

## Core Series (40+ pre-configured)

| Category | Series | FRED ID |
|----------|--------|---------|
| Economic Output | Real GDP | GDPC1 |
| Economic Output | GDP Growth Rate | A191RL1Q225SBEA |
| Economic Output | Industrial Production | INDPRO |
| Inflation | CPI-U All Items | CPIAUCSL |
| Inflation | Core CPI | CPILFESL |
| Inflation | PCE Price Index | PCEPI |
| Inflation | WTI Crude Oil | DCOILWTICO |
| Employment | Unemployment Rate (U-3) | UNRATE |
| Employment | Nonfarm Payrolls | PAYEMS |
| Employment | Initial Jobless Claims | ICSA |
| Employment | Labor Force Participation | CIVPART |
| Employment | Average Hourly Earnings | CES0500000003 |
| Housing | Median Home Price | MSPUS |
| Housing | 30-Year Mortgage Rate | MORTGAGE30US |
| Housing | Housing Starts | HOUST |
| Housing | Case-Shiller Index | CSUSHPINSA |
| Consumer | Consumer Sentiment | UMCSENT |
| Consumer | Personal Saving Rate | PSAVERT |
| Consumer | Consumer Credit | TOTALSL |
| Financial | Fed Funds Rate | FEDFUNDS |
| Financial | 10-Year Treasury | DGS10 |
| Financial | 2-Year Treasury | DGS2 |
| Financial | VIX | VIXCLS |
| Trade | Trade Balance | BOPGSTB |
| Trade | USD Index | DTWEXBGS |
| Fiscal | Federal Debt | GFDEBTN |

Any valid FRED series ID works, not just the pre-configured ones.

## Environment Requirements

```bash
export FRED_API_KEY="your_key"  # Required
```

Get a free API key at: https://fred.stlouisfed.org/docs/api/api_key.html
