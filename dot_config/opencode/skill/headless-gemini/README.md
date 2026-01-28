# Gemini CLI Reference

Extended reference for the headless-gemini skill. Main documentation in SKILL.md.

## Model Comparison

| Model | Context | Best For | Cost |
|-------|---------|----------|------|
| `gemini-3-pro-preview` | 1M in / 64k out | Complex reasoning, coding | $2-4/M |
| `gemini-3-flash` | 1M in / 64k out | Speed-critical tasks | Lower |
| `gemini-2.5-pro` | 1M in / 65k out | Stable general use | Mid |
| `gemini-2.5-flash` | 1M in / 65k out | High-volume processing | $0.15/M |
| `gemini-2.5-flash-lite` | 1M in / 65k out | Maximum throughput | Lowest |

## Approval Mode Details

| Mode | Description | Use When |
|------|-------------|----------|
| `default` | Prompts for each tool | Interactive terminal only |
| `auto_edit` | Auto-approves file edits | Code review with suggestions |
| `yolo` | Auto-approves everything | Background, CI/CD, automation |

## Troubleshooting

### Hung Process Diagnosis

```bash
# Detailed process info
ps -o pid,etime,pcpu,stat,command -p <PID>

# Check network activity (0 = hung)
lsof -p <PID> 2>/dev/null | grep -E "(TCP|ESTABLISHED)" | wc -l
```

### Out of Memory

- Switch to `gemini-3-flash`
- Use `--include-directories` to limit scope
- Break analysis into chunks

## Prompt Templates

### Security Review
```
Review for OWASP Top 10 vulnerabilities, JWT handling, session management, rate limiting, and password hashing.
```

### Architecture Analysis
```
Analyze architecture, patterns, technical debt, and refactoring opportunities.
```

### Code Quality
```
Review code quality: naming, structure, error handling, test coverage, documentation.
```
