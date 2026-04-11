# GetCurrentState Workflow

**Skill:** USMetrics > GetCurrentState
**Purpose:** Generate comprehensive U.S. economic overview with multi-timeframe trend analysis

## Overview

This workflow produces a detailed analysis document examining all 68 metrics across 10 categories and multiple time horizons (10 year, 5 year, 2 year, 1 year), identifying patterns, correlations, and research opportunities.

## Data Dependency

This workflow fetches data directly from FRED and EIA APIs. For the best results, ensure API keys are set. Alternatively, run the UpdateData workflow first to populate dataset files, then this workflow can read from those files.

## Execution Steps

### Step 1: Run Analysis Script

Execute the analysis generator:

```bash
bun scripts/GenerateAnalysis.ts
```

To save output to a file:

```bash
bun scripts/GenerateAnalysis.ts --output=US-Economic-State-Analysis.md
```

The script handles all data fetching, trend calculation, and report generation.

### Step 2: Manual Analysis (Alternative)

If running the analysis without the script, follow these steps:

#### 2a: Load Metric Definitions

Read the master metrics document and extract all metrics with their:
- FRED series IDs (or other API identifiers)
- Categories
- Update frequencies
- Current values

#### 2b: Fetch Historical Data

For each metric with a FRED series ID, fetch historical data spanning 10+ years.

**Priority FRED Series:**

| Category | Metric | FRED ID |
|----------|--------|---------|
| GDP | Real GDP | GDPC1 |
| GDP | GDP Growth Rate | A191RL1Q225SBEA |
| Inflation | CPI-U All Items | CPIAUCSL |
| Inflation | Core CPI | CPILFESL |
| Inflation | PCE Price Index | PCEPI |
| Employment | Unemployment Rate | UNRATE |
| Employment | Nonfarm Payrolls | PAYEMS |
| Employment | Initial Jobless Claims | ICSA |
| Housing | Median Home Price | MSPUS |
| Housing | 30-Year Mortgage Rate | MORTGAGE30US |
| Consumer | Consumer Sentiment | UMCSENT |
| Consumer | Personal Saving Rate | PSAVERT |
| Markets | Fed Funds Rate | FEDFUNDS |
| Markets | 10-Year Treasury | DGS10 |
| Markets | 2-Year Treasury | DGS2 |
| Trade | Trade Balance | BOPGSTB |
| Fiscal | Federal Debt | GFDEBTN |

**Non-FRED Data (separate APIs):**
- Gas prices: EIA API (`PET.EMM_EPMR_PTE_NUS_DPG.W`)
- Oil prices: EIA API (`PET.RWTC.W`)
- Federal debt (daily): Treasury FiscalData API

#### 2c: Calculate Trend Statistics

For each metric, calculate:

**Timeframe Analysis:**
- **10-Year:** CAGR, total change, volatility
- **5-Year:** CAGR, total change, comparison to 10-year trend
- **2-Year:** CAGR, total change, recent acceleration/deceleration
- **1-Year:** YoY change, recent momentum, latest value vs. average

**Trend Direction:**
- Rising, Falling, or Stable (threshold: 2% change)
- Acceleration indicator (speeding up vs. slowing down)

**Example:**
```
Unemployment Rate (UNRATE)
  Current: 4.1% (Nov 2024)
  10-Year: 5.8% -> 4.1% (-1.7pp, down trend)
  5-Year: 3.5% -> 4.1% (+0.6pp, up from pre-COVID low)
  2-Year: 3.7% -> 4.1% (+0.4pp, gradual rise)
  1-Year: 3.9% -> 4.1% (+0.2pp, slight increase)
  Assessment: Gradually rising from 50-year lows, still historically low
```

#### 2d: Cross-Category Analysis

Analyze interrelationships between categories:

1. **Inflation vs. Employment** (Phillips Curve dynamics)
   - CPI vs. Unemployment correlation
   - Wage growth vs. inflation relationship

2. **Monetary Policy vs. Economy**
   - Fed Funds Rate impact on mortgage rates, housing
   - Yield curve (10Y-2Y spread) as recession indicator

3. **Consumer Health vs. Economic Output**
   - Sentiment vs. retail sales correlation
   - Saving rate vs. consumer spending

4. **Housing vs. Broader Economy**
   - Home prices vs. inflation
   - Housing starts as leading indicator

5. **Energy vs. Inflation**
   - Oil/gas prices impact on CPI

6. **Fiscal vs. Financial Markets**
   - Debt growth vs. Treasury yields
   - Deficit spending impact on GDP

#### 2e: Pattern Detection

Identify notable patterns:

1. **Regime Changes** -- Pre/post COVID comparison, pre/post rate hike cycle
2. **Divergences** -- Metrics moving opposite to historical correlation
3. **Extremes** -- Metrics at historical highs/lows or multiple standard deviations from mean
4. **Leading Indicator Signals** -- Jobless claims trend, yield curve shape, consumer sentiment direction

#### 2f: Research Recommendations

Based on patterns detected, suggest:
- Areas requiring deeper investigation
- Potential risks to monitor
- Opportunities for analysis
- Data gaps to fill

### Step 3: Compile Output Document

Generate structured markdown report following the output format below.

## Output Format

```markdown
# US Economic State Analysis

**Generated:** [YYYY-MM-DD HH:MM]
**Data Period:** [10 years through current]
**Sources:** FRED, EIA, Treasury FiscalData, BLS, Census

---

## Executive Summary

[3-5 bullet points with the most important findings]

---

## Current Snapshot

| Category | Key Metric | Value | YoY Change | Trend |
|----------|------------|-------|------------|-------|
| Economy | Real GDP Growth | X.X% | +X.X | ... |
| Inflation | CPI YoY | X.X% | -X.X | ... |
| Employment | Unemployment | X.X% | +X.X | ... |

---

## Detailed Trend Analysis

### 1. Economic Output & Growth
| Metric | Current | 10Y | 5Y | 2Y | 1Y |
[Per-metric analysis]

### 2. Inflation & Prices
[...]

[Continue for all 10 categories]

---

## Cross-Metric Analysis

### Inflation-Employment Dynamics
[Phillips curve analysis]

### Yield Curve Status
[10Y-2Y spread, recession signals]

### Housing Affordability
[Home prices vs. mortgage rates]

---

## Pattern Detection

### Regime Changes
### Divergences
### Historical Extremes
### Recent Momentum Shifts

---

## Research Recommendations

### High Priority Investigations
### Risks to Monitor
### Data Gaps

---

## Sources
[FRED, EIA, Treasury, BLS, Census attribution]
```

## Trigger Phrases

- "How is the US economy doing?"
- "Give me an economic overview"
- "What's the current state of US metrics?"
- "Analyze economic trends"
- "US metrics report"

## Error Handling

- If FRED API fails: Note which metrics could not be fetched, proceed with available data
- If API key missing: Prompt user to set the relevant environment variable
- If metric not found: Log missing series, continue with others
