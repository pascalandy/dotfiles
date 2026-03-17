---
name: commit
description: Create atomic commits with clear, specific messages. Use before any git commit.
---

# Skill: Commit

Create atomic commits: one logical change per commit.

## Rule

If a commit cannot be described in one sentence without "and", split it.

## Required behavior

- Review the entire working tree before committing
- Never combine unrelated changes
- Stage and commit each logical group separately
- Do not push unless the user explicitly asks
- Use a commit body for any non-trivial commit
- When splitting commits, never use `git add .` or `git add -A`

## Workflow

1. Run `git status` and `git diff --stat`
2. Group all changes by logical purpose
3. Split by purpose, feature, type, or rollback boundary
4. Stage only the paths for one group with `git add <paths>`
5. Commit each group in order
6. Push only if requested

## Split when

- Changes serve different purposes
- Changes belong to different features
- Changes use different commit types
- Changes would not be reverted together
- Docs/config/tooling changes are unrelated to the code change

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

## Format

```text
<emoji> <type>: <scope>: <imperative summary>

- Purpose: <why this change exists>
- Impact: <effect on users, system, or future work>
```

Use these optional fields when helpful:
- `File(s) changed:` for multi-file or non-obvious commits
- `Nature of changes:` when the category needs clarification

## Writing style

- Use imperative mood
- Use active voice
- Be specific and concrete
- Cut filler
- Avoid vague claims like `improve`, `enhance`, `streamline`, `optimize` unless made concrete
- Keep the subject under 72 characters
- Do not end body lines with periods

## Final check

Before committing, confirm:
- one logical change
- no unrelated files staged
- subject says what changed
- body says why it matters
