# Crash Recovery Procedure

Use this file when the applied home-directory state and the chezmoi source tree
seem out of sync.

## First Steps

```bash
# Check chezmoi health
chezmoi doctor

# Check real drift, excluding run scripts
just cm-status
just cm-diff

# Preview an apply
just cm-apply-dry
```

If the preview looks correct, apply:

```bash
just cm-apply-verbose
```

## How This Repo Works

- Source of truth: `~/.local/share/chezmoi/`
- Applied target: `~/`
- Chezmoi copies files into place; it does not use symlinks here.

Important: `chezmoi apply` has side effects in this repo.

- `.chezmoiscripts/run_before_sync.sh`
  Syncs VS Code settings and keybindings back into the repo and refreshes the
  VS Code extensions list. Brewfile dumping exists in the script, but it is
  currently disabled by default.
- `.chezmoiscripts/run_after_backup.sh`
  Copies selected backup files into the repo, renders `dot_config/ai_templates/`
  into target-safe names, and syncs shared commands and skills to multiple
  agent homes.

## Normal Recovery Flow

```bash
# 1. Audit the repo and chezmoi drift
git status -sb
just cm-audit

# 2. If the source looks right, preview the apply
just cm-apply-dry

# 3. Apply if the preview is safe
just cm-apply-verbose

# 4. If a specific managed file is wrong, edit the source file
chezmoi edit ~/.zshrc
```

If you need to add a new managed file:

```bash
chezmoi add ~/.file
just cm-apply-dry
just cm-apply-verbose
```

## Templates and Secrets

Any file containing `{{ variable }}` must keep the `.tmpl` extension.

Example:

```json
"apiKey": "{{ .openrouter_api_key }}"
```

If you see `{{ variable }}` literally in an applied config file, the template
is not being rendered.

## Common Issues

### Literal template variables appear in an applied file

Cause: the source file was renamed or stored without the `.tmpl` suffix.

Fix:

```bash
chezmoi managed | grep opencode
chezmoi edit ~/.config/opencode/opencode.json
just cm-apply-dry
just cm-apply-verbose
```

If the source file itself is missing `.tmpl`, fix that in the chezmoi source
tree before applying again.

### Apply output looks noisy because scripts will run

Cause: chezmoi run scripts show up as script activity, which is expected.

Fix:

```bash
just cm-status
just cm-diff
```

Those commands intentionally exclude scripts so you can inspect real managed
file drift.

### Brewfile churn or apply-loop concerns

Cause: dumping the Brewfile during apply can create feedback loops.

Current behavior: `run_before_sync.sh` keeps Brewfile dumping behind
`SYNC_BREWFILE=false`, so it does not run by default.

## Ignored But Tracked Files

Some tracked files are intentionally excluded from apply through
`.chezmoiignore`. That means a file can exist in the repo without being copied
into `$HOME`.

Examples include:

- repo metadata and documentation such as `README.md`, `AGENTS.md`, and `docs/`
- archived or reference material such as `bienvenue_chez_moi/`
- selected app/runtime files managed outside normal apply flow

If a tracked file is not showing up in `$HOME`, check `.chezmoiignore` before
assuming chezmoi is broken.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `just ci` | Run local checks, including a chezmoi dry-run |
| `just cm-status` | Show real chezmoi drift, excluding scripts |
| `just cm-diff` | Diff managed state against target, excluding scripts |
| `just cm-apply-dry` | Preview an apply |
| `just cm-apply-verbose` | Apply with verbose output |
| `chezmoi doctor` | Check chezmoi health |
| `chezmoi edit ~/.file` | Edit the source file for a managed target |
| `chezmoi add ~/.file` | Add a new file to chezmoi management |

## Official Documentation

https://www.chezmoi.io/user-guide/command-overview/
