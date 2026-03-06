---
name: headless-gemini
description: Use when running Gemini CLI for code review, plan review, or large context (>200k tokens) processing in background/non-interactive shells.
---

# Gemini CLI Skill

## When to Use

- User asks to run Gemini CLI
- Code review across multiple files
- Plan/architecture review
- Context exceeds 200k tokens
- Multi-file pattern analysis

## Critical: Background Mode

**NEVER use `--approval-mode default` in non-interactive shells.** It hangs waiting for approval.

| Context | Approval Mode |
|---------|---------------|
| Background/automated | `yolo` (required) |
| Interactive terminal | `default` or `auto_edit` |

## Workflow

1. **Ask user for model** (single prompt):
   - `gemini-3-pro-preview` - flagship, 76.2% SWE-bench
   - `gemini-3-flash` - sub-second latency
   - `gemini-2.5-pro` - legacy stable
   - `gemini-2.5-flash` - cost-efficient ($0.15/M)

2. **Set approval mode** based on context (background = yolo)

3. **Run command**:
   ```bash
   gemini -m gemini-3-pro-preview --approval-mode yolo "Review this codebase for security issues"
   ```

4. **Add timeout for safety**:
   ```bash
   timeout 300 gemini -m gemini-3-pro-preview --approval-mode yolo "..."
   ```

## Quick Reference

| Flag | Purpose |
|------|---------|
| `-m MODEL` | Select model |
| `--approval-mode yolo` | Auto-approve all (background) |
| `--approval-mode auto_edit` | Auto-approve edits only |
| `-i "prompt"` | Interactive with initial prompt |
| `--include-directories DIR` | Add directories to context |
| `-s` | Sandbox mode |

## Hung Process Recovery

**Symptoms**: 20+ min runtime, 0% CPU, state 'S' (sleeping)

```bash
# Detect
ps aux | grep gemini | grep -v grep

# Kill
pkill -9 -f "gemini.*gemini-3"
```

## Common Use Cases

```bash
# Background code review
gemini -m gemini-3-pro-preview --approval-mode yolo \
  "Review for security vulnerabilities and code quality"

# Multi-directory analysis
gemini -m gemini-3-pro-preview --approval-mode yolo \
  --include-directories /backend --include-directories /frontend \
  "Analyze full-stack architecture"
```

## Error Handling

- Non-zero exit: report failure, ask for direction
- High-impact flags (`yolo`, `sandbox`): confirm with user first
- Partial results: summarize warnings, ask how to adjust

## Requirements

Gemini CLI v0.16.0+ for Gemini 3 support. Check: `gemini --version`
