# Capture Schema

## YAML Frontmatter Fields

```yaml
---
title: string              # Human-readable title
date: YYYY-MM-DD           # Date of documentation
module: string             # Which module or component
problem_type: enum         # See problem types below
component: enum            # See components below
severity: enum             # critical, high, medium, low
tags: [string]             # Searchable keywords (1-10)
category: string           # Auto-mapped from problem_type
---
```

## Problem Types (Enum)

| problem_type | Category Directory |
|-------------|-------------------|
| build_error | build-errors/ |
| test_failure | test-failures/ |
| runtime_error | runtime-errors/ |
| performance_issue | performance-issues/ |
| database_issue | database-issues/ |
| security_issue | security-issues/ |
| ui_bug | ui-bugs/ |
| integration_issue | integration-issues/ |
| logic_error | logic-errors/ |
| best_practice | best-practices/ |
| workflow_issue | workflow-issues/ |
| developer_experience | developer-experience/ |

## Components (Enum)

rails_model, rails_controller, rails_view, service_object, background_job, database, frontend, api, authentication, payments, testing_framework, tooling, infrastructure, configuration, deployment

## Severity Levels

| Level | Criteria |
|-------|----------|
| critical | Data loss, security breach, production outage |
| high | Significant user impact, revenue loss |
| medium | Degraded experience, workaround exists |
| low | Minor inconvenience, cosmetic issue |

## Tracks

### Bug Track
For problems that were broken and got fixed. Sections: Problem, Symptoms, What Didn't Work, Solution, Why This Works, Prevention.

### Knowledge Track
For best practices, patterns, and guidance. Sections: Context, Guidance, Why This Matters, When to Apply, Examples.

## Filename Pattern

`[sanitized-problem-slug]-[YYYYMMDD].md`

Sanitization: lowercase, spaces to hyphens, remove special characters, truncate to 80 chars.

## Category Mapping

The `category` field is auto-derived from `problem_type` using the table above. Do not invent categories not in this schema.
