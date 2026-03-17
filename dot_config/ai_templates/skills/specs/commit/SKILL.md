---
name: commit
description: Create atomic commits with clear, specific messages. Use before any git commit.
---

# Skill: Commit

Create truly atomic commits: one logical change per commit.

## Core rule

A commit must be describable in one sentence without using "and".
If not, split it.

## Non-negotiables

- Never combine unrelated changes
- Always analyze the full working tree before committing
- Use a commit body for any non-trivial commit
- When splitting commits, never use `git add .` or `git add -A`

## Required workflow

1. Inspect all changes with `git status` and `git diff --stat`
2. Group changes by logical purpose across the entire working tree
3. Split when changes differ by purpose, feature, commit type, or rollback boundary
4. Stage only the files for one group with specific `git add <paths>`
5. Commit each group in sequence
6. Push only if the user asked

## Split rule

Split commits when changes involve:
- Different purposes
- Different features
- Different commit types (`feat`, `fix`, `docs`, `refactor`, etc.)
- Code and docs that are not part of the same logical change
- Changes that would not be reverted together

## Commit types

- `✨ feat`
- `🚑 fix`
- `♻️ refactor`
- `📚 docs`
- `🧪 test`
- `🎨 style`
- `⚡️ perf`
- `🧑‍💻 chore`
- `🧹 remove`
- `🔒 security`
- `🚧 wip`

## Message format

```text
<emoji> <type>: <scope>: <imperative summary>

- Purpose: <why this change exists>
- Impact: <user, system, or developer effect>
```

Optional:
- Add `(context)` after scope when useful
- Add `File(s) changed` for multi-file or non-obvious commits
- Trivial changes may use a minimal body

## Writing rules

- Use imperative mood: `Add`, `Fix`, `Remove`
- Use active voice
- Be specific and concrete
- Omit needless words
- Avoid puffery like `improve`, `enhance`, `streamline`, `optimize` unless followed by a measurable detail
- Keep the subject under 72 characters
- Do not end body lines with periods

## Quality check

Before committing, verify:
- This commit contains one logical change
- The message describes that change precisely
- The body explains why it matters
- No unrelated files are staged
