# UpdateData Workflow

**Skill:** USMetrics > UpdateData
**Purpose:** Fetch current data from all sources and update the metrics dataset

## Overview

This workflow pulls live data from FRED, EIA, Treasury FiscalData, and other APIs, then writes the current values to the dataset files. The GetCurrentState workflow reads from these files for analysis.

## Data Flow

```
APIs (FRED, EIA, Treasury)
    |
    v
UpdateSubstrateMetrics.ts
    |
    v
Dataset files:
  - US-Common-Metrics.md (markdown with values)
  - us-metrics-current.csv (machine-readable)
  - us-metrics-historical.csv (time series)
```

## Execution Steps

### Step 1: Check Prerequisites

Verify environment before running:
- `FRED_API_KEY` must be set (required for most metrics)
- `EIA_API_KEY` should be set (required for energy data)
- `bun` must be available in PATH
- `US_METRICS_DATA_DIR` should point to the dataset directory (optional, has default)

### Step 2: Run Update Script

Execute the update script from this sub-skill's directory:

```bash
bun scripts/UpdateSubstrateMetrics.ts
```

The script:
1. Fetches current values from all configured APIs (68 metrics)
2. Updates `US-Common-Metrics.md` with current values in the markdown tables
3. Exports to `us-metrics-current.csv` as a machine-readable snapshot
4. Appends to `us-metrics-historical.csv` with a fetch timestamp
5. Logs update status for each metric (success/failure)

For a dry run (fetch without writing):

```bash
bun scripts/UpdateSubstrateMetrics.ts --dry-run
```

### Step 3: Verify Update

After the script completes, verify:
- `US-Common-Metrics.md` has current values (not placeholders `--`)
- `us-metrics-current.csv` exists and has data rows
- Check console output for any failed fetches

Report the number of metrics updated and any failures to the user.

## API Sources

| Source | API Endpoint | Metrics | Auth |
|--------|-------------|---------|------|
| **FRED** | api.stlouisfed.org | GDP, CPI, unemployment, rates, etc. | `FRED_API_KEY` |
| **EIA** | api.eia.gov | Gas prices, oil prices | `EIA_API_KEY` |
| **Treasury** | api.fiscaldata.treasury.gov | Federal debt (daily) | None |

## Output Files

### US-Common-Metrics.md

The markdown file gets values populated in the metric tables:

```markdown
| Metric | Value | Period | Updated | Source |
|--------|-------|--------|---------|--------|
| Real GDP | $22.67T | Q3 2024 | 2024-11-27 | BEA/FRED |
| CPI YoY | 2.6% | Oct 2024 | 2024-11-13 | BLS/FRED |
```

### us-metrics-current.csv

```csv
metric_id,metric_name,value,formatted_value,period,updated,source
GDPC1,"Real GDP",22670.532,"$22670.53B",2024-07-01,2024-11-27,"BEA/FRED"
CPIAUCSL,"CPI-U All Items",315.562,"315.562",2024-10-01,2024-11-13,"BLS/FRED"
```

### us-metrics-historical.csv

Appends each update as new rows with timestamp:

```csv
fetch_timestamp,metric_id,value,period
2024-12-01T10:30:00Z,GDPC1,22670.532,2024-07-01
2024-12-01T10:30:00Z,UNRATE,4.1,2024-10-01
```

## Error Handling

- **API failure**: Log which metrics failed, continue with remaining
- **Missing API key**: Warn and skip that source (FRED is required; EIA, Treasury are optional)
- **Rate limit**: Script implements 100ms delays between requests
- **Partial update**: Report which metrics are stale in output

## Trigger Phrases

- "Update US metrics"
- "Refresh the metrics data"
- "Pull latest economic data"
- "Fetch current values"

## Notes

- FRED is the primary aggregator -- most metrics route through FRED even if the original source is BLS/BEA
- Treasury FiscalData is used directly for daily debt figures (more current than FRED)
- EIA is used directly for energy prices (more current than FRED)
- Some annual metrics (population, GINI) only update once per year
