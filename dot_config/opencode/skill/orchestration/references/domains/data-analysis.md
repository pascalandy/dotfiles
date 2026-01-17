# Data Analysis Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Data yields insights faster when explored in parallel.    │
│   Multiple dimensions, simultaneous analysis, clear story.  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **AGENT REMINDER**: Only use `@ben`, `@abby`, or `@oracle`.
> See [SKILL.md](../../SKILL.md) for costs and task mapping.
> In examples below, "Agent A/B/C" = parallel `@abby` tasks for analysis or `@ben` for data gathering.

> **Load when**: Exploratory data analysis, data quality, report generation, ETL pipelines, statistical analysis
> **Common patterns**: Multi-Dimensional Exploration, Comprehensive Quality Audit, Hypothesis Testing

## Table of Contents

1. [Exploratory Data Analysis](#exploratory-data-analysis)
2. [Data Quality](#data-quality)
3. [Report Generation](#report-generation)
4. [ETL Pipelines](#etl-pipelines)
5. [Statistical Analysis](#statistical-analysis)

---

## Exploratory Data Analysis

### Pattern: Multi-Dimensional Exploration

```
User Request: "Analyze this dataset"

Phase 1: FAN-OUT (Parallel initial exploration - @ben tasks)
├─ @ben: Schema analysis (columns, types, constraints)
├─ @ben: Statistical summary (distributions, outliers)
├─ @ben: Missing data analysis
├─ @ben: Cardinality and uniqueness analysis
└─ @ben: Sample data examination

Phase 2: REDUCE
└─ @abby: Synthesize initial findings

Phase 3: FAN-OUT (Deep dive based on findings - @ben tasks)
├─ @ben: Correlation analysis
├─ @ben: Time series patterns (if applicable)
└─ @ben: Categorical relationship analysis

Phase 4: REDUCE
└─ @abby: Complete EDA report
```

### Pattern: Question-Driven Analysis

```
User Request: "Why are sales declining?"

Phase 1: EXPLORE
└─ @ben: Understand available data sources

Phase 2: FAN-OUT (Parallel hypothesis investigation - @ben tasks)
├─ @ben: Analyze sales by region
├─ @ben: Analyze sales by product
├─ @ben: Analyze sales by customer segment
├─ @ben: Analyze external factors (seasonality, competition)
└─ @ben: Analyze marketing/promotion effectiveness

Phase 3: REDUCE
└─ @abby: Identify key drivers, recommendations
```

### Pattern: Comparative Analysis

```
Phase 1: FAN-OUT (parallel @ben tasks)
├─ @ben: Analyze dataset A characteristics
├─ @ben: Analyze dataset B characteristics
└─ @ben: Analyze overlap/differences

Phase 2: REDUCE
└─ @abby: Comparison report with insights
```

---

## Data Quality

### Pattern: Comprehensive Quality Audit

```
User Request: "Check data quality for the customer table"

Phase 1: FAN-OUT (Parallel quality dimensions - @ben tasks)
├─ @ben: Completeness (null rates, missing values)
├─ @ben: Accuracy (format validation, range checks)
├─ @ben: Consistency (cross-field validation)
├─ @ben: Timeliness (freshness, update patterns)
├─ @ben: Uniqueness (duplicates, key integrity)
└─ @ben: Validity (business rule compliance)

Phase 2: REDUCE
└─ @abby: Quality scorecard with issues

Phase 3: FAN-OUT (Remediation - @ben tasks)
├─ @ben: Fix completeness issues
├─ @ben: Fix accuracy issues
└─ @ben: Fix consistency issues
```

### Pattern: Anomaly Detection

```
Phase 1: FAN-OUT (parallel @ben tasks)
├─ @ben: Statistical outlier detection
├─ @ben: Business rule violations
├─ @ben: Pattern anomalies (sudden changes)
└─ @ben: Referential integrity issues

Phase 2: REDUCE
└─ @abby: Anomaly report with severity
```

### Pattern: Data Profiling Pipeline

```
Phase 1: PIPELINE
├─ @abby: Extract profiling metrics
├─ @abby: Compare against historical baseline
└─ @abby: Flag deviations

Phase 2: BACKGROUND
└─ @ben: Generate profile report
```

---

## Report Generation

### Pattern: Multi-Section Report

```
User Request: "Generate monthly business report"

Phase 1: FAN-OUT (Parallel section generation - @ben tasks)
├─ @ben: Executive summary section
├─ @ben: Sales performance section
├─ @ben: Customer metrics section
├─ @ben: Product analytics section
├─ @ben: Financial summary section
└─ @ben: Operational metrics section

Phase 2: REDUCE
└─ @abby: Compile sections, add insights

Phase 3: PIPELINE
└─ @abby: Format, add visualizations
```

### Pattern: Automated Dashboard Refresh

```
Phase 1: FAN-OUT (Parallel data refresh)
├─ @ben: Refresh data source 1
├─ @ben: Refresh data source 2
└─ @ben: Refresh data source 3

Phase 2: PIPELINE
├─ @abby: Aggregate refreshed data
└─ @abby: Update dashboard calculations

Phase 3: BACKGROUND
└─ @ben: Generate and distribute report
```

### Pattern: Ad-Hoc Query Report

```
User Request: "Get me sales by region for Q4"

Phase 1: EXPLORE
└─ @ben: Find relevant tables and joins

Phase 2: PIPELINE
├─ @abby: Build and execute query
├─ @abby: Format results
└─ @abby: Add context and insights
```

---

## ETL Pipelines

### Pattern: ETL Development

```
User Request: "Create ETL pipeline for user events"

Phase 1: EXPLORE
└─ @ben: Understand source schema, target requirements

Phase 2: PLAN
└─ @abby: Design ETL architecture

Phase 3: FAN-OUT (Parallel component development - @ben tasks)
├─ @ben: Extract logic (source connectors)
├─ @ben: Transform logic (cleaning, mapping)
├─ @ben: Load logic (target insertion)
└─ @ben: Error handling and logging

Phase 4: PIPELINE
├─ @abby: Wire components
└─ @ben: Test with sample data
```

### Pattern: ETL Debugging

```
User Request: "ETL job is failing"

Phase 1: FAN-OUT (Parallel diagnosis)
├─ @ben: Check job logs
├─ @ben: Check source data quality
├─ @ben: Check target schema compatibility
└─ @ben: Check resource utilization

Phase 2: REDUCE
└─ @abby: Root cause identification

Phase 3: PIPELINE
├─ @abby: Implement fix
└─ @ben: Verify fix with test run
```

### Pattern: Schema Evolution

```
Phase 1: EXPLORE
└─ @ben: Identify schema changes

Phase 2: FAN-OUT (parallel @ben tasks)
├─ @ben: Update extract logic
├─ @ben: Update transform mappings
└─ @ben: Update load targets

Phase 3: PIPELINE
├─ @abby: Migration script
└─ @ben: Backfill historical data
```

---

## Statistical Analysis

### Pattern: Hypothesis Testing

```
User Request: "Did the new feature improve conversion?"

Phase 1: EXPLORE
└─ @ben: Gather pre and post data

Phase 2: FAN-OUT (parallel @ben tasks)
├─ @ben: Descriptive statistics (both groups)
├─ @ben: Distribution analysis
└─ @ben: Confounding variable check

Phase 3: PIPELINE
├─ @abby: Select appropriate test
├─ @abby: Run statistical test
└─ @abby: Interpret results

Phase 4: REDUCE
└─ @abby: Conclusion with confidence
```

### Pattern: Predictive Modeling

```
Phase 1: FAN-OUT (Data preparation - @ben tasks)
├─ @ben: Feature engineering
├─ @ben: Data cleaning
└─ @ben: Train/test split

Phase 2: SPECULATIVE (Model selection - @ben tasks)
├─ @ben: Train model type 1
├─ @ben: Train model type 2
└─ @ben: Train model type 3

Phase 3: REDUCE
└─ @abby: Compare models, select best

Phase 4: PIPELINE
└─ @abby: Final evaluation, documentation
```

### Pattern: Trend Analysis

```
Phase 1: FAN-OUT (parallel @ben tasks)
├─ @ben: Decompose time series
├─ @ben: Identify seasonality patterns
├─ @ben: Detect change points
└─ @ben: Forecast future values

Phase 2: REDUCE
└─ @abby: Trend report with insights
```

---

## Task Management for Data Analysis

Structure data analysis with parallel exploration:

```python
# Create analysis tasks
TaskCreate(subject="Understand data sources", description="Schema, types, relationships...")
TaskCreate(subject="Explore distributions", description="Statistical summaries, outliers...")
TaskCreate(subject="Analyze missing data", description="Null patterns, imputation needs...")
TaskCreate(subject="Check data quality", description="Validation, consistency...")
TaskCreate(subject="Synthesize findings", description="Aggregate insights, recommendations...")
TaskCreate(subject="Generate report", description="Visualizations, documentation...")

# Parallel exploration after understanding
TaskUpdate(taskId="2", addBlockedBy=["1"])
TaskUpdate(taskId="3", addBlockedBy=["1"])
TaskUpdate(taskId="4", addBlockedBy=["1"])
TaskUpdate(taskId="5", addBlockedBy=["2", "3", "4"])
TaskUpdate(taskId="6", addBlockedBy=["5"])

# Spawn parallel analysis agents
Task(subagent_type="@abby", prompt="TaskId 2: Explore distributions...")
Task(subagent_type="@abby", prompt="TaskId 3: Analyze missing data...")
Task(subagent_type="@abby", prompt="TaskId 4: Check data quality...")
```

## Best Practices

1. **Parallelize exploration** across dimensions
2. **Validate data quality** before analysis
3. **Background long queries** to maintain responsiveness
4. **Document assumptions** in reports
5. **Include confidence levels** in statistical conclusions

---

```
─── ◈ Data Analysis ─────────────────────
```
