# Quickstart

Use this reference for installation, first-run setup, global flags, output shaping, and general CLI behavior.

## Install

```bash
# macOS
brew install gh

# verify
gh --version
```

If the user is on another OS, prefer the official install docs or the platform package manager.

## First authentication steps

```bash
gh auth login
gh auth status
gh auth setup-git
```

Good automation pattern:

```bash
export GH_TOKEN="ghp_xxxxxxxxxxxx"
```

Useful environment variables:

```bash
export GH_TOKEN="..."
export GH_HOST="github.com"
export GH_REPO="owner/repo"
export GH_EDITOR="vim"
export GH_PAGER="less"
export GH_PROMPT_DISABLED=true
```

## Global help pattern

```bash
gh --help
gh help environment
gh help formatting
gh help exit-codes
gh repo --help
gh repo create --help
```

## Global flags to remember

| Flag | Use |
| --- | --- |
| `--repo [HOST/]OWNER/REPO` | target another repository |
| `--hostname HOST` | target GitHub Enterprise host |
| `--json FIELDS` | structured output |
| `--jq EXPRESSION` | filter JSON output |
| `--template STRING` | Go-template formatting |
| `--web` | open in browser |
| `--paginate` | fetch all pages where supported |
| `--verbose` / `--debug` | troubleshooting |

## Structured output

Prefer JSON when another step will consume the result.

```bash
gh repo view owner/repo --json name,description,defaultBranchRef
gh issue list --json number,title,state --jq '.[] | [.number, .title, .state]'
gh pr list --json number,title,author --jq '.[] | {number, title, author: .author.login}'
```

## Practical defaults

- For repeated work in one repo, set `GH_REPO` or run `gh repo set-default owner/repo`.
- For ambiguous syntax, ask the local CLI with `--help` instead of guessing.
- For actions not exposed by top-level subcommands, use `gh api`.
- For scripts, prefer non-interactive flags and machine-readable output.
