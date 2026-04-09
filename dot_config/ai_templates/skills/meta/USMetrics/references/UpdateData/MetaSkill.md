---
name: UpdateData
description: Fetch live US economic data from FRED, EIA, and Treasury APIs and update the metrics dataset files. USE WHEN update metrics, refresh data, pull latest, fetch live data, update dataset, refresh economic data, update substrate metrics.
---

# UpdateData

Fetch current data from all configured federal API sources and write the results to the metrics dataset directory.

## Workflow Routing

| Intent | Workflow |
|--------|----------|
| Update all metrics from APIs | `workflows/UpdateData.md` |

## Overview

This sub-skill pulls live data from FRED, EIA, Treasury FiscalData, and other APIs, then writes current values to the dataset files. The GetCurrentState sub-skill reads from these files for analysis.

## Data Flow

```
APIs (FRED, EIA, Treasury)
    |
    v
UpdateData workflow (this)
    |
    v
Dataset files:
  - US-Common-Metrics.md (markdown with values)
  - us-metrics-current.csv (machine-readable)
  - us-metrics-historical.csv (time series)
    |
    v
GetCurrentState workflow (reads from here)
```

## Script

| Script | Purpose |
|--------|---------|
| `scripts/UpdateSubstrateMetrics.ts` | Fetches all 68 metrics from APIs, updates dataset files |

Execute with:

```bash
bun scripts/UpdateSubstrateMetrics.ts
```

Use `--dry-run` to fetch data without writing files.

## API Sources

| Source | API | Metrics | Auth |
|--------|-----|---------|------|
| FRED | api.stlouisfed.org | GDP, CPI, unemployment, rates, etc. | `FRED_API_KEY` |
| EIA | api.eia.gov | Gas prices, oil prices | `EIA_API_KEY` |
| Treasury | api.fiscaldata.treasury.gov | Federal debt, budget | None |

## Environment Requirements

```bash
export FRED_API_KEY="your_key"    # Required
export EIA_API_KEY="your_key"     # Required for energy data
export US_METRICS_DATA_DIR="/path/to/data"  # Optional, has default
```

## Output Files

| File | Format | Purpose |
|------|--------|---------|
| `US-Common-Metrics.md` | Markdown tables | Human-readable metric values with sources |
| `us-metrics-current.csv` | CSV | Machine-readable snapshot of all current values |
| `us-metrics-historical.csv` | CSV (append-only) | Time series with fetch timestamps |

## Error Handling

- **API failure**: Logs which metrics failed, continues with others
- **Missing API key**: Warns and skips that source
- **Rate limit**: Implements delays between requests (100ms)
- **Partial update**: Marks which metrics are stale in output

## Metric Categories (68 metrics total)

1. **Economic Output & Growth** (8) -- GDP, industrial production, retail sales, durable goods
2. **Inflation & Prices** (7) -- CPI, PCE, PPI, oil, gas prices
3. **Employment & Labor** (12) -- Unemployment, payrolls, claims, JOLTS, wages
4. **Housing** (8) -- Home prices, sales, starts, permits, mortgage rates
5. **Consumer & Personal Finance** (8) -- Sentiment, income, saving, credit, delinquency
6. **Financial Markets** (10) -- Fed funds, Treasuries, VIX, S&P 500, stress index
7. **Trade & International** (5) -- Trade balance, exports, imports, USD index
8. **Government & Fiscal** (5) -- Federal debt, debt-to-GDP, receipts, expenditures
9. **Demographics & Social** (3) -- Population, GINI index, median household income
10. **Health & Crisis** (2) -- Life expectancy, deaths of despair

## Update Frequency Recommendations

| Frequency | Metrics |
|-----------|---------|
| Daily | Treasury yields, oil prices, federal debt |
| Weekly | Gas prices, jobless claims, mortgage rates |
| Monthly | CPI, employment, GDP, housing data |
