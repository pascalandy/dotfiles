# AGENTS.md - Chezmoi Dotfiles Repository


## browsing the public web

do not use web-fetch, use skill `agent-browser`

## Custom tools

When showing gif diff changes, use skill: `hunk-review`

## Exporting a plan

When the user wants to export/save a plan from our conversation to the wiki:

1. Determine the next available ID by checking existing directories in `docs/plans/references/`
2. Create directory: `docs/plans/references/{id}-{title}/`
3. Organise the plan directory as a valid wiki-map (skill)

Example workflow:
- User says "export this plan" or "save the plan to wiki"
- Check: `ls docs/plans/references/ | sort -V | tail -5`
- Create: `docs/plans/references/2912-migration-strategy/`
- Run: skill `wiki-map` to structure the content

## Repository Overview

This is a **chezmoi dotfiles repository** that manages configuration files across machines.
- **Source directory**: `~/.local/share/chezmoi/`
- **Target directory**: `~/` (home directory)
- **Repository**: https://github.com/pascalandy/dotfiles

Chezmoi stores desired state here and syncs to home via `chezmoi apply` (copies, not symlinks).

## Critical Rules

### NEVER Edit Files Under Home Directory

**This is the #1 rule in this repository. No exceptions.**

The source of truth is ALWAYS `~/.local/share/chezmoi/`. Files under `~/` (including `~/.config/`) are **applied copies** that get overwritten on every `chezmoi apply`.

**Before writing or editing ANY file, you MUST check:**

```bash
chezmoi managed | grep <filename>
```

If the file is managed, edit the **chezmoi source** -- never the target. Common mistakes:

| WRONG (applied/target path) | CORRECT (chezmoi source path) |
|------------------------------|-------------------------------|
| `~/.config/opencode/skill/...` | `~/.local/share/chezmoi/dot_config/ai_templates/skills/...` |
| `~/.config/opencode/opencode.json` | `~/.local/share/chezmoi/dot_config/opencode/opencode.json.tmpl` |
| `~/.zshrc` | `~/.local/share/chezmoi/dot_zshrc` |
| `~/.gitconfig` | `~/.local/share/chezmoi/dot_gitconfig` |
| `~/.config/...` | `~/.local/share/chezmoi/dot_config/...` |

**Workflow:**
1. Run `chezmoi managed | grep <filename>` to check if managed
2. If managed: edit under `~/.local/share/chezmoi/` (translate path using `dot_` prefix rules)
3. Run `chezmoi apply -v` to sync changes to home
4. If NOT managed: safe to edit directly, or `chezmoi add` to start managing it

### Chezmoi Naming Conventions

| Prefix/Suffix | Meaning |
|---------------|---------|
| `dot_` | File starts with `.` (e.g., `dot_zshrc` → `.zshrc`) |
| `private_` | Applied with `600`/`700` permissions (still visible in git) |
| `executable_` | Applied with execute permission |
| `symlink_` | Creates a symlink |
| `.tmpl` | Template file (processes `{{ }}` variables) |
| `run_before_` | Script runs before apply |
| `run_after_` | Script runs after every apply |
| `run_once_` | Script runs only on first apply |

## Commands Reference

load skill `chezmoi`

## User Preferences

### Custom Scripts Location

**Preference**: Store user scripts in `~/.local/bin/` (XDG-compliant standard location).

```bash
# Create a new script
code ~/.local/bin/[script-name]

# Make executable and add to chezmoi
chmod +x ~/.local/bin/[script-name]
chezmoi add ~/.local/bin/[script-name]
```

Scripts are stored in chezmoi as: `dot_local/bin/executable_[script-name]`

Ensure `~/.local/bin` is in PATH (add to `.zshrc` if needed):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Note**: Script names should NOT have `.sh` extension for cleaner CLI usage.

## Bash Script Standards

if needed, load skill `bash`

## Source vs Applied Paths

Many AI-related files have two path forms:

- source-tree paths in this repo, for example `dot_config/opencode/plugin/`
- applied runtime paths under `~/.config/...`, for example `~/.config/opencode/plugin/`

When documenting or editing behavior, verify whether the source of truth is the
chezmoi source path or the applied runtime path. Do not edit the applied file
directly if chezmoi manages it.

## Templates and Secrets

Files containing `{{ .variable }}` MUST have `.tmpl` extension:

```bash
# Wrong: Variables won't be processed
opencode.json

# Correct: chezmoi processes templates
opencode.json.tmpl
```

## Testing Changes

```bash
# Run the main local checks
just ci

# Preview what would change (dry run)
just cm-apply-dry

# Apply with verbose output
just cm-apply-verbose

# Verify a specific file
chezmoi cat ~/.zshrc
```

Pre-commit hooks run staged `gitleaks`, `shellcheck`, and `shfmt` via
`lefthook`. GitHub Actions currently runs repository-wide `gitleaks`,
`shellcheck`, and `shfmt`.

## Run Scripts

This repo has two run scripts located in `.chezmoiscripts/` (chezmoi v2.9+ convention):

### `.chezmoiscripts/run_before_sync.sh`
- Syncs VS Code settings/keybindings to chezmoi source
- Updates VS Code extensions list
- Can dump the Brewfile, but that path is currently disabled by default via `SYNC_BREWFILE=false`

### `.chezmoiscripts/run_after_backup.sh`
- Copies selected external backup files into the repo
- Renders `dot_config/ai_templates/` through chezmoi and syncs shared commands/skills to multiple agent homes
- Uses merge behavior for OpenCode shared assets so OpenCode-specific entries can stay managed separately

<!-- opensrc:start -->

## Source Code Reference

Source code for dependencies is available in `opensrc/` for deeper understanding of implementation details.

See `opensrc/sources.json` for the list of available packages and their versions.

Use this source code when you need to understand how a package works internally, not just its types/interface.

### Fetching Additional Source Code

To fetch source code for a package or repository you need to understand, run:

```bash
npx opensrc <package>           # npm package (e.g., npx opensrc zod)
npx opensrc pypi:<package>      # Python package (e.g., npx opensrc pypi:requests)
npx opensrc crates:<package>    # Rust crate (e.g., npx opensrc crates:serde)
npx opensrc <owner>/<repo>      # GitHub repo (e.g., npx opensrc vercel/ai)
```

<!-- opensrc:end -->