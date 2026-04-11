---
name: USMetrics
description: 68 US economic indicators from FRED, EIA, Treasury, BLS, Census APIs -- data refresh, trend analysis, cross-metric correlation, and individual series lookup. Three modes routed automatically based on intent.
keywords: [economics, GDP, inflation, unemployment, FRED, EIA, Treasury, BLS, Census, metrics, trend-analysis, US-economy, indicators, update-data, refresh-data, economic-overview, fetch-series, gas-prices, housing, consumer, trade, fiscal]
---

# USMetrics

> Three economic analysis modes in one skill -- data refresh from federal APIs, comprehensive economic state analysis, and individual FRED series lookup, routed automatically based on what you need.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Understanding the US economy requires pulling data from half a dozen federal APIs (FRED, EIA, Treasury FiscalData, BLS, Census), each with different formats, authentication, and endpoints. When you want a quick economic overview, you end up:

- **Manually fetching data** -- bouncing between FRED, EIA, Treasury, and BLS websites to assemble a picture
- **Missing context** -- seeing one metric (unemployment) without understanding its relationship to others (GDP, inflation, labor force participation)
- **No trend perspective** -- getting the current value but not the 1-year, 2-year, 5-year, or 10-year trajectory
- **Stale data** -- relying on cached or outdated numbers because refreshing is tedious
- **No single-metric deep dives** -- when you want the full history and trend statistics for one indicator, there is no quick path

The fundamental issue: economic analysis requires current data across many categories, correlated intelligently, with multi-timeframe trend context -- and there is no simple way to get all of that at once.

---

## The Solution

USMetrics provides three sub-skills that handle the full pipeline from data fetching to analysis:

1. **UpdateData** -- Fetches live data from FRED, EIA, and Treasury APIs for all 68 metrics. Updates dataset files with current values, produces human-readable markdown and machine-readable CSV outputs, and appends to historical time series for trend tracking.

2. **GetCurrentState** -- Reads current and historical data for all 68 metrics across 10 categories. Calculates 10-year, 5-year, 2-year, and 1-year trends. Analyzes cross-metric correlations and leading indicators. Detects anomalies, regime changes, and emerging patterns. Generates a comprehensive structured markdown report with research recommendations.

3. **FetchSeries** -- Fetches historical data for individual FRED series with configurable time ranges. Calculates multi-timeframe trend statistics (10y/5y/2y/1y) with direction indicators. Outputs human-readable summaries or JSON for further processing.

The 10 categories covered: Economic Output and Growth, Inflation and Prices, Employment and Labor, Housing, Consumer and Personal Finance, Financial Markets, Trade and International, Government and Fiscal, Demographics and Social, Health and Crisis.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | Minimal routing table that dispatches to the right sub-skill |
| UpdateData skill | `references/UpdateData/MetaSkill.md` | Data ingestion from federal APIs |
| UpdateData workflow | `references/UpdateData/workflows/UpdateData.md` | Step-by-step data fetch and update procedure |
| UpdateData script | `references/UpdateData/scripts/UpdateSubstrateMetrics.ts` | TypeScript tool -- fetches all 68 metrics, updates dataset files |
| GetCurrentState skill | `references/GetCurrentState/MetaSkill.md` | Comprehensive economic analysis generation |
| GetCurrentState workflow | `references/GetCurrentState/workflows/GetCurrentState.md` | Analysis pipeline with trend calculations and pattern detection |
| GetCurrentState script | `references/GetCurrentState/scripts/GenerateAnalysis.ts` | TypeScript tool -- generates analysis report from fetched data |
| FetchSeries skill | `references/FetchSeries/MetaSkill.md` | Individual FRED series lookup with trends |
| FetchSeries script | `references/FetchSeries/scripts/FetchFredSeries.ts` | TypeScript tool -- fetches historical data for any FRED series |

**Summary:**
- **Sub-skills:** 3 (UpdateData, GetCurrentState, FetchSeries)
- **Workflows:** 2 (UpdateData, GetCurrentState)
- **Scripts:** 3 TypeScript tools (require `bun` runtime)
- **Dependencies:** `bun` runtime, `FRED_API_KEY`, `EIA_API_KEY` environment variables

---

## What Makes This Different

USMetrics fetches 68 metrics across 10 categories from federal data sources in a single operation. It does not just give you a number -- it calculates multi-timeframe trends (10y/5y/2y/1y), correlates metrics across categories (e.g., how unemployment relates to consumer sentiment and housing starts), detects anomalies and regime changes, and produces a structured report with research recommendations. A manual FRED lookup gives you one data point. USMetrics gives you the full economic picture with context.

- Covers 68 metrics across 10 categories from multiple federal APIs
- Multi-timeframe trend analysis (1-year through 10-year)
- Cross-metric correlation and pattern detection
- Individual series deep dives with full historical data
- Structured output format ready for AI analysis and human consumption

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "Update the US metrics" | Routes to UpdateData -- fetches live data from all APIs, updates dataset files |
| "Refresh economic data" | Routes to UpdateData -- same as above |
| "How is the US economy doing?" | Routes to GetCurrentState -- produces comprehensive analysis with trends |
| "Give me an economic overview" | Routes to GetCurrentState -- generates full economic state report |
| "What's happening with inflation?" | Routes to GetCurrentState -- generates analysis (focused on Inflation category) |
| "Analyze economic trends" | Routes to GetCurrentState -- multi-timeframe trend analysis across all categories |
| "Fetch the unemployment rate history" | Routes to FetchSeries -- retrieves UNRATE with trend statistics |
| "Get FRED data for GDP" | Routes to FetchSeries -- fetches GDPC1 series with historical observations |
| "What's the 10-year trend for CPI?" | Routes to FetchSeries -- fetches CPIAUCSL with trend calculations |

---

## Example Usage

### Updating Metrics Data

```
User: "Update the US metrics"

AI responds:
Running the UpdateData workflow...

[Executes UpdateSubstrateMetrics.ts]

Updated 68 metrics across 10 categories:
- Economic Output & Growth: 8 metrics updated
- Inflation & Prices: 7 metrics updated
- Employment & Labor: 12 metrics updated
...

Files updated:
- US-Common-Metrics.md (human-readable)
- us-metrics-current.csv (machine-readable snapshot)
- us-metrics-historical.csv (appended time series)
```

### Getting Economic Overview

```
User: "How is the US economy doing?"

AI responds:
Running the GetCurrentState workflow...

# US Economic State Analysis
Generated: 2026-03-15
Data Sources: FRED, EIA, Treasury, BLS, Census

## Executive Summary
- GDP growth at 2.3% (10y avg: 2.1%) -- slightly above trend
- CPI inflation at 2.8% (trending down from 3.4% one year ago)
- Unemployment at 4.1% (stable, within historical norms)
- Housing starts declining 12% year-over-year
- Consumer sentiment recovering from 2-year low

## Trend Analysis by Category
[10y/5y/2y/1y trends with analysis per category]

## Cross-Metric Analysis
[Correlations, leading indicators, divergences]

## Pattern Detection
[Anomalies, regime changes, emerging trends]

## Research Recommendations
[Suggested areas for deeper investigation]
```

### Fetching Individual Series

```
User: "Get the unemployment rate history with trends"

AI responds:
Running the FetchSeries workflow...

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

---

## Configuration

### Required: API Keys

The UpdateData and GetCurrentState sub-skills require API keys set as environment variables:

| Key | Source | Purpose |
|-----|--------|---------|
| `FRED_API_KEY` | [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html) | Federal Reserve Economic Data (most metrics) |
| `EIA_API_KEY` | [EIA API](https://www.eia.gov/opendata/register.php) | Energy Information Administration (gas/oil prices) |

### Required: Runtime

The TypeScript scripts require `bun` to be installed and available in PATH.

### Data Directory

Set `US_METRICS_DATA_DIR` to point to the directory where metrics data is stored. The scripts read from and write to this directory. If unset, defaults to `~/Projects/Substrate/Data/US-Common-Metrics`.

---

## Customization

### Optional Customization

| Customization | File | Impact |
|--------------|------|--------|
| Add or remove tracked metrics | `references/UpdateData/scripts/UpdateSubstrateMetrics.ts` | Changes which metrics are fetched and tracked |
| Change data directory | `US_METRICS_DATA_DIR` environment variable | Points to a different dataset location |
| Modify analysis format | `references/GetCurrentState/workflows/GetCurrentState.md` | Changes the output structure of economic reports |
| Add new API sources | `references/UpdateData/scripts/UpdateSubstrateMetrics.ts` | Extends data coverage to additional APIs |
| Adjust trend periods | `references/FetchSeries/scripts/FetchFredSeries.ts` | Changes which timeframes are calculated |

---

## Credits

- **Original concept:** Daniel Miessler -- developed as part of the [PAI](https://github.com/danielmiessler/Personal_AI_Infrastructure) system
- **Data sources:** FRED (Federal Reserve), EIA (Energy Information Administration), Treasury FiscalData, BLS (Bureau of Labor Statistics), Census Bureau

---

## Changelog

### 1.0.0
- Initial release as hierarchical meta-skill
- Three sub-skills: UpdateData, GetCurrentState, FetchSeries
- Unified routing via `references/ROUTER.md`
- 68 metrics across 10 categories from federal APIs
- Multi-timeframe trend analysis (1y/2y/5y/10y)
- Cross-metric correlation and pattern detection
- Individual series lookup with trend statistics
- Harness-agnostic: no hardcoded assistant paths
