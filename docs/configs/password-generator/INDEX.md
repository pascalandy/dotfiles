---
name: Password Generator
description: Secure password generator configuration and documentation
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Password Generator

> Content catalog for password generator configuration and documentation.
> Read this first to find relevant pages for any query.
> **Total pages:** 3 | **Last updated:** 2026-04-11

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/doc

| File | Description |
|------|-------------|
| `references/readme.md` | Password generator usage and options documentation |
| `references/source.md` | Source reference for the password generator |

### Scripts

| File | Description |
|------|-------------|
| `scripts/password_generator.py` | Secure password generator Python script |

## Quick Reference

Run command: `passgen` anywhere in your terminal.

For agents:
- Run script with defaults: `uv run scripts/password_generator.py`
- Use defaults, do not ask user questions

## Dependencies

> **Warning:** The `passgen` CLI command depends on this script being at the expected path.
> 
> The wrapper script `dot_local/bin/executable_passgen` (applied to `~/.local/bin/passgen`) calls:
> ```bash
> uv run ~/.local/share/chezmoi/docs/configs/password-generator/scripts/password_generator.py
> ```
> 
> If this directory structure changes, the `passgen` command will break. Update the wrapper script if moving files.
