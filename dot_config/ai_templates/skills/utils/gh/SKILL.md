---
name: gh
description: >
  Use this skill whenever the user wants exact GitHub CLI (`gh`) commands,
  command syntax, or terminal workflows for GitHub: auth/setup, repository
  management, issues, pull requests, Actions runs/workflows, releases, projects,
  search, `gh api` / GraphQL, secrets, variables, gists, codespaces,
  organizations, rulesets, keys, aliases, or extensions. Trigger even if the
  user does not say “gh” explicitly and instead asks things like “what command
  do I use,” “how do I do this from the terminal,” “give me the GitHub CLI
  command,” “script this with gh,” or “show me the flags/subcommand.” Prefer
  this skill for GitHub command lookup and `gh`-native automation, but not for
  writing workflow YAML, rewriting PR text, explaining GitHub concepts without
  CLI usage, or generic local git/repo tasks that do not need `gh`.
compatibility: Requires GitHub CLI (`gh`) installed and authenticated when live GitHub access is needed.
---

# GitHub CLI (`gh`)

Use this skill to operate GitHub from the terminal and to look up the right `gh` command shape quickly.

## Principle

Keep this file as the index.
Read only the reference file that matches the user’s task instead of loading the whole command catalog.
If syntax is uncertain or the local CLI version may differ, trust local help output:

```bash
gh --help
gh <group> --help
gh <group> <command> --help
```

## Fast workflow

1. Confirm whether the task is:
   - auth/config
   - repo / issue / PR work
   - Actions / projects / releases
   - search / API / org / admin / extensions
2. Read the matching reference file from `references/`.
3. Prefer the smallest command that solves the task.
4. For automation or structured output, prefer `--json`, `--jq`, and `gh api` when needed.
5. If the task changes remote state, mention the target repo/org/environment clearly before running commands.

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
  - `gh search`, `gh api`, `gh org`, `gh gist`, `gh codespace`, `gh extension`, aliases, keys, rulesets, attestations, browse/status

## Defaults and best practices

- Prefer `gh auth status` before assuming the CLI is ready.
- Prefer `gh repo set-default owner/repo` for repeated work in one repo.
- Prefer `--json` + `--jq` for machine-readable output.
- Prefer `gh api` for edge cases not covered by a first-class subcommand.
- Prefer reading one reference file at a time; only open more if the task spans multiple domains.
- When a command is destructive (`delete`, `close`, `merge`, secret changes, repo settings), verify scope first.
- When the user asks for broad GitHub automation, combine `gh` commands with shell pipelines carefully and keep repo/org names explicit.

## Common command triage

- “log in / switch account / set token / configure gh” → read `references/10-auth-and-config.md`
- “create repo / open issue / make PR / review PR / sync fork” → read `references/20-repos-issues-prs.md`
- “rerun workflow / inspect Actions / manage release / project board / secrets” → read `references/30-actions-projects-releases.md`
- “search GitHub / call GraphQL / manage org / gist / codespace / extension” → read `references/40-search-api-and-admin.md`

## Help and sources

Start with local CLI help for exact syntax. Use the official manual only as a secondary source when needed.

- Manual: https://cli.github.com/manual/
- GitHub Docs: https://docs.github.com/en/github-cli
- REST API: https://docs.github.com/en/rest
- GraphQL API: https://docs.github.com/en/graphql
