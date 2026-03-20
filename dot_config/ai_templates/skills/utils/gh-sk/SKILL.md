---
name: gh-sk
description: >
  Use only when the user explicitly say "gh-sk" to use the GitHub cli when the AI assistant hits an edge case or is not working as expected or need to know advance commands. Load it to troubleshoot unexpected behavior, syntax gaps, auth issues, API gaps, or cases where general `gh` knowledge is not enough.
compatibility: Requires GitHub CLI (`gh`) installed and authenticated when live GitHub access is needed.
---

# GitHub CLI (`gh`)

Use this skill to operate GitHub from the terminal and to find the right `gh` command quickly.

## Principle

Treat this file as the index.
Read only the reference file that matches the task instead of loading the whole command catalog.
If syntax is uncertain, or the local CLI version may differ, trust local help output:

```bash
gh --help
gh <group> --help
gh <group> <command> --help
```

## Fast workflow

1. Identify the task area:
   - auth and config
   - repos, issues, or PRs
   - Actions, projects, or releases
   - search, API, org, admin, or extensions
2. Read the matching file in `references/`
3. Prefer the smallest command that solves the task.
4. For automation or structured output, prefer `--json`, `--jq`, and `gh api` when needed.
5. If the task changes remote state, name the target repo, org, or environment before you run anything.

## Reference map

- `references/00-quickstart.md`
  - install, auth, global flags, JSON output, help patterns, environment variables
- `references/10-auth-and-config.md`
  - `gh auth`, `gh config`, credential setup, tokens, host switching
- `references/20-repos-issues-prs.md`
  - `gh repo`, `gh issue`, `gh pr`, labels, common review workflows
- `references/30-actions-projects-releases.md`
  - `gh run`, `gh workflow`, `gh cache`, `gh secret`, `gh variable`, `gh project`, `gh release`
- `references/40-search-api-and-admin.md`
  - `gh search`, `gh api`, `gh org`, `gh gist`, `gh codespace`, `gh extension`, aliases, keys, rulesets, attestations, browse, status

## Defaults and best practices

- Run `gh auth status` before you assume the CLI is ready.
- Use `gh repo set-default owner/repo` for repeated work in one repo.
- Prefer `--json` with `--jq` for machine-readable output.
- Use `gh api` for edge cases that lack a first-class subcommand.
- Read one reference file at a time. Open more only when the task spans multiple areas.
- For destructive commands such as `delete`, `close`, `merge`, secret changes, or repo setting changes, verify scope first.
- When the user asks for broad GitHub automation, combine `gh` with shell pipelines carefully and keep repo or org names explicit.

## Common command triage

- “log in,” “switch account,” “set token,” “configure gh” → `references/10-auth-and-config.md`
- “create repo,” “open issue,” “make PR,” “review PR,” “sync fork” → `references/20-repos-issues-prs.md`
- “rerun workflow,” “inspect Actions,” “manage release,” “project board,” “secrets” → `references/30-actions-projects-releases.md`
- “search GitHub,” “call GraphQL,” “manage org,” “gist,” “Codespace,” “extension” → `references/40-search-api-and-admin.md`

## Help and sources

Start with local CLI help for exact syntax. Use the official manual only when needed.

- Manual: https://cli.github.com/manual/
- GitHub Docs: https://docs.github.com/en/github-cli
- REST API: https://docs.github.com/en/rest
- GraphQL API: https://docs.github.com/en/graphql
