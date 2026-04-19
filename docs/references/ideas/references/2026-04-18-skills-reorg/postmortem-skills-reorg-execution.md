# Postmortem — Skills Reorg Execution (2026-04-18)

## Context

Pascal had iterated v1→v4 of a skills reorg idea plus a phased plan, then said `go` with both file paths. Executed Phases 1–7: pre-flight, create 7 buckets, 45 `git mv` operations, fix path references, update the bucket list in `run_after_backup.sh`, validate downstream sync, commit, push, open PR. Result: PR #7 on `reorg/skills-v4`, all 8 agent homes verified at 54 flat skills, CI gates green.

## Lessons

- A 3-line pre-flight (`fd SKILL.md | wc -l`, per-bucket counts, duplicate-name check) caught zero drift before any moves. Cheap insurance when shuffling 50+ paths.
- `chezmoi archive` inside `run_after_backup.sh` reads source-of-truth, not target state. That made it safe to bypass `chezmoi apply` when an unrelated zed drift blocked the canonical validation path.
- Lifting a hard-coded list into a single `local -a categories=(…)` array kills the kind of two-loop drift the original 4-bucket-list-twice pattern produced.
- `git mv` rename detection survived all 45 moves at 100% similarity — full file history preserved, no `add`/`rm` fallback needed.

## What To Repeat

- Pre-flight count + duplicate-name gate before any bulk rename.
- Annotate the source idea/plan files with an outcome line in the same commit as the work, so the artifact graph self-documents.
- Patch only the path references that are *actively wrong after* the change. Defer architecture-level doc rewrites (e.g. `how-ai-templates-are-distributed`) to a separate doc-update task.
- Stage the work on a branch + PR for a 533-file diff, even when commit granularity is "one bundled" — reviewability beats main-branch speed here.

## What To Avoid

- Bundling unrelated cleanup into a focused refactor PR. Pre-existing `~/.config/zed/settings.json` drift was tempting to "just fix" — keeping it out kept the diff coherent.
- Forcing a tool past an obstacle when a quieter alternative exists. The zed prompt blocked `cm-apply-verbose`; running the script directly achieved the goal without `--force` overwriting external state.

## Feedback for the Agent

- When a `go` follows a plan whose "Open questions" already list proposed answers, default to those answers and proceed — don't re-ask.
- Bash cwd persists between calls in this harness. Trust `git status` / explicit `pwd` to verify state instead of reasoning about whether `cd` carried over.
- `wc -l` can be intercepted by a `wt` (worktree) CLI alias on this machine. Pipe to `/usr/bin/wc -l` when the result matters.
- For a 45-rename batch, group the `git mv` calls by destination bucket in a single `&&`-chained Bash call — fewer round-trips, cleaner verification.

## Feedback for the User

- The pre-existing `~/.config/zed/settings.json` drift will keep blocking `chezmoi apply` until resolved. Either `chezmoi re-add ~/.config/zed/settings.json` (accept the external change as new source) or `chezmoi apply ~/.config/zed/settings.json --force` (discard external change).
- `docs/references/operations/references/how-ai-templates-are-distributed/*` now describes the stale 4-bucket model. Worth a `pa-doc-update` pass to align it with the new 8-bucket reality before someone learns the wrong thing from it.
- Two stale references in `docs/references/configs/references/how-my-opencode-is-configured.md` (lines 149–151) point at skills that don't exist (`pa-sdlc/delegate`, `specs/use-subagents`, `specs/run-oc`). Pre-existing, not caused by this reorg, but worth cleaning up.
