---
name: GetCurrentState
description: Generate comprehensive US economic overview with multi-timeframe trend analysis, cross-metric correlation, pattern detection, and research recommendations. USE WHEN how is the economy, economic overview, get current state, analyze trends, economic report, US metrics analysis, cross-metric correlation, pattern detection, economic state, what is happening with inflation, employment analysis.
---

# GetCurrentState

Generate a comprehensive analysis document examining all 68 metrics across 10 categories with multi-timeframe trends, cross-metric correlations, and pattern detection.

## Workflow Routing

| Intent | Workflow |
|--------|----------|
| Full economic state analysis | `workflows/GetCurrentState.md` |

## Overview

This sub-skill reads current and historical data for all metrics, calculates trends across four time horizons, analyzes cross-category relationships, and produces a structured markdown report. Run the UpdateData sub-skill first to ensure data is current.

## Data Dependency

This sub-skill reads from dataset files produced by UpdateData. If data is stale or missing, run UpdateData first.

## Script

| Script | Purpose |
|--------|---------|
| `scripts/GenerateAnalysis.ts` | Fetches data from FRED/EIA APIs and generates the full analysis report |

Execute with:

```bash
bun scripts/GenerateAnalysis.ts
```

Use `--output=path` to save to a file instead of stdout.

## Analysis Pipeline

1. **Load Metrics** -- Read the master metrics document and extract all metric definitions
2. **Fetch Historical Data** -- Retrieve 10+ years of observations for each metric from FRED/EIA
3. **Calculate Trends** -- Compute 10-year, 5-year, 2-year, and 1-year statistics (CAGR, total change, volatility)
4. **Cross-Category Analysis** -- Analyze interrelationships (Phillips Curve, yield curve, housing affordability)
5. **Pattern Detection** -- Identify regime changes, divergences, extremes, leading indicator signals
6. **Research Recommendations** -- Suggest areas for deeper investigation based on patterns detected
7. **Compile Report** -- Generate structured markdown output

## Cross-Category Analyses Performed

| Analysis | Metrics Compared |
|----------|-----------------|
| Inflation-Employment (Phillips Curve) | CPI vs. Unemployment, wage growth vs. inflation |
| Monetary Policy Transmission | Fed Funds Rate impact on mortgages, housing |
| Yield Curve Status | 10Y-2Y spread as recession indicator |
| Consumer-Economy Linkage | Sentiment vs. retail sales, saving rate vs. spending |
| Housing Affordability | Home prices vs. mortgage rates |
| Energy-Inflation | Oil/gas prices impact on CPI |
| Fiscal-Financial Markets | Debt growth vs. Treasury yields |

## Output Format

The workflow produces a structured markdown document:

```markdown
# US Economic State Analysis
**Generated:** [timestamp]
**Data Sources:** FRED, EIA, Treasury, BLS, Census

## Executive Summary
[3-5 bullet points with key findings]

## Current Snapshot
[Table: Category | Key Metric | Value | YoY Change | Trend]

## Detailed Trend Analysis
### 1. Economic Output & Growth
[10y/5y/2y/1y analysis per metric]
### 2. Inflation & Prices
...
[All 10 categories]

## Cross-Metric Analysis
[Correlations, leading indicators, divergences]

## Pattern Detection
[Regime changes, divergences, historical extremes, momentum shifts]

## Research Recommendations
[High priority investigations, risks to monitor, data gaps]

## Sources
[Data attribution]
```

## Environment Requirements

```bash
export FRED_API_KEY="your_key"    # Required
export EIA_API_KEY="your_key"     # Optional (gas prices)
```

## Key FRED Series (Priority)

| Category | Metric | FRED ID |
|----------|--------|---------|
| GDP | Real GDP | GDPC1 |
| Inflation | CPI-U All Items | CPIAUCSL |
| Inflation | Core PCE | PCEPILFE |
| Employment | Unemployment Rate | UNRATE |
| Employment | Nonfarm Payrolls | PAYEMS |
| Housing | Median Home Price | MSPUS |
| Housing | 30-Year Mortgage Rate | MORTGAGE30US |
| Consumer | Consumer Sentiment | UMCSENT |
| Markets | Fed Funds Rate | FEDFUNDS |
| Markets | 10-Year Treasury | DGS10 |
| Trade | Trade Balance | BOPGSTB |
| Fiscal | Federal Debt | GFDEBTN |
