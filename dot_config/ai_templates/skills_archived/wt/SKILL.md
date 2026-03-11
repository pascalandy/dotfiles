---
name: wt
description: >
  Use this skill before coding, editing, or updating files in a Git repo when
  branch safety matters. Always check whether the current branch is `main` or
  `master` before making changes. If it is, do not work there: use Worktrunk
  (`wt`) to create or switch to a feature worktree, confirm the active location
  with `wt list`, do the work there, and merge back with `wt merge` when ready.
  Also trigger when the user mentions Worktrunk, `wt`, git worktrees, protected
  main branches, branch hygiene, feature branches, merge-and-cleanup workflows,
  shell integration, hooks, or wants the exact command for creating, listing,
  removing, or merging worktrees. Prefer this skill even when the user simply
  asks to “make this change” in a repo, because the first decision should be
  whether the work belongs in a fresh worktree instead of `main` or `master`.
compatibility: Requires Git and Worktrunk (`wt`). Shell integration is recommended for automatic directory switching.
---

# Worktrunk (`wt`)

Use this skill to keep implementation work off `main` and `master`, and to find the right `wt` command quickly.

## Principle

Treat this file as the index.
Read only the reference file that matches the task instead of loading every Worktrunk detail at once.
If syntax is uncertain, trust local CLI help over memory:

```bash
wt --help
wt <command> --help
```

## Mandatory pre-edit check

Before editing tracked files in a Git repo:

1. Confirm you are in a Git repo.
2. Check the current branch.
3. If the branch is `main` or `master`, move to a feature worktree before editing.
4. If already on a non-mainline feature branch, continue unless the user wants worktree cleanup or reorganization.
5. If `git branch --show-current` is empty, treat it as detached HEAD and pause to clarify.

Use:

```bash
git rev-parse --show-toplevel
git branch --show-current
```

If `git rev-parse --show-toplevel` fails, this skill does not apply.

## Fast workflow

1. Check repo and branch first.
2. If on `main` or `master`, create or switch to a feature worktree.
3. Confirm location with `wt list`.
4. Do the work in that worktree.
5. Merge back with `wt merge` when the user is happy.

## Default safe flow

```bash
git rev-parse --show-toplevel
git branch --show-current
wt switch --create <feature-name>
wt list
# do the work in that worktree
wt merge main
wt list
```

If the repo still uses `master`, merge to `master` instead.
If the repo default branch is known and the target is obvious, plain `wt merge` is acceptable.

## Behavior rules

- Prefer `wt` over raw `git worktree` for normal workflows.
- If the user explicitly asks for raw `git worktree` commands, answer that request, but note that `wt` is the preferred workflow in this environment.
- Do not silently edit on `main` or `master`.
- Keep responses short and operational: say what you checked, where you switched, and what command comes next.
- When the feature branch name is unclear, ask for one instead of inventing a vague name.

## Reference map

- `references/00-quickstart.md`
  - repo check, branch check, default flow, command triage
- `references/10-core-guardrail.md`
  - when to leave `main` or `master`, detached HEAD, feature-branch behavior
- `references/20-switch-and-list.md`
  - `wt switch`, `wt list`, `--create`, `--base`, JSON output, status checks
- `references/30-merge-and-remove.md`
  - `wt merge`, `wt remove`, cleanup behavior, merge semantics, useful flags
- `references/40-config-hooks-and-automation.md`
  - `wt config show`, shell integration, hooks, approvals, `wt step`, automation
- `references/50-faq-and-troubleshooting.md`
  - branch switching vs worktrees, default-branch cache, common failure cases, docs-backed rationale

## Common triage

- “make this change in the repo” → start with `references/10-core-guardrail.md`
- “create a worktree / branch / switch me over” → `references/20-switch-and-list.md`
- “what do I run to merge this back?” → `references/30-merge-and-remove.md`
- “why didn’t wt cd into the worktree?” or “show config” → `references/40-config-hooks-and-automation.md`
- “why wt instead of branch switching?” or “what does the FAQ say?” → `references/50-faq-and-troubleshooting.md`

## Response pattern

When you apply this skill, include the relevant facts directly:

- repo check result
- current branch before edits
- whether you had to leave `main` or `master`
- the feature branch or worktree you created or switched to
- confirmation step, usually `wt list`
- merge target when relevant

## Help and sources

Start with local CLI help for exact syntax. Use the official docs when you need rationale, edge cases, or config details.

- Docs: https://worktrunk.dev/
- FAQ: https://worktrunk.dev/faq/
- Switch: https://worktrunk.dev/switch/
- List: https://worktrunk.dev/list/
- Merge: https://worktrunk.dev/merge/
- Remove: https://worktrunk.dev/remove/
- Config: https://worktrunk.dev/config/
- Hook: https://worktrunk.dev/hook/
- Step: https://worktrunk.dev/step/
- Tips: https://worktrunk.dev/tips-patterns/
- Claude Code integration: https://worktrunk.dev/claude-code/
- LLM commits: https://worktrunk.dev/llm-commits/
