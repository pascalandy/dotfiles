---
date: "2026-03-29"
tags:
  - guide
---
# Testing Dotfile Changes

## Prerequisites
- Changes made to chezmoi source (not directly in `~/`)
- `just` command runner installed

## Steps

### 1. Run quality checks
```bash
just ci
```
This runs:
- gitleaks (secret detection)
- shellcheck (shell script linting)
- shfmt (shell script formatting)
- chezmoi apply dry-run

### 2. Preview changes
```bash
just cm-apply-dry
```
Shows what would change without applying.

### 3. Check for drift
```bash
just cm-status
```
Shows real drift excluding run scripts (which always show `R`).

### 4. Apply changes
```bash
just cm-apply-verbose
```
Applies with verbose output to see exactly what changed.

### 5. Verify specific files
```bash
chezmoi cat ~/.zshrc    # See what chezmoi thinks the file should be
```

## Common problems
- **"R" status on run scripts** — Normal, not drift. Run scripts execute every apply.
- **Changes not appearing** — Ensure you edited chezmoi source, not `~/`
- **Template errors** — Check `.tmpl` files for valid chezmoi syntax
- **Permission denied** — Use `private_` or `executable_` prefixes as needed

## Related
- [[Repository Topology]]
- [[Adding a New Dotfile]]
- [[Chezmoi Apply Automation]]
