---
title: "postmortem: atlas-refresh-picker"
type: postmortem
status: completed
date: 2026-03-24
plan: docs/plans/2026-03-24-001-feat-atlas-refresh-picker-plan.md
origin: docs/features/feat-1005/idea-map-filesystem.md
tags: [cli, skill-design, naming, user-experience]
---

# Postmortem: atlas-refresh-picker

## 1. Plan assumed TTY availability — reality broke it immediately

**Memory type: learning**

The plan built everything around `simple-term-menu` as the primary UX. The TTY risk was listed but underestimated — the plan said "OpenCode's Bash tool runs in a persistent shell session that should support this." It doesn't. `stdin.isatty()` returns `False`, `simple-term-menu` crashes with `OSError: Device not configured: '/dev/tty'`.

**Lesson:** When a plan identifies a risk and includes a mitigation (`--all` flag), test the risk first before building the primary path. We tested it in 15 seconds and saved building the entire picker.

**Feedback for agent:** Always validate environmental assumptions (TTY, network, filesystem) before implementing features that depend on them. A 30-second spike test is cheaper than building a feature that can't run.

## 2. Plan missed the user-facing command design entirely

**Memory type: error**

The plan focused on the CLI subcommand (`refresh`) and the orchestration (`map-filesystem.md`), but never asked: "What will the user actually type to trigger this?" The plan treated the command file as a thin dispatcher and the skill as implementation detail.

What actually happened:
- User couldn't figure out what commands were available
- `SKILL.md` was buried in `references/` — wrong location
- No user guide existed
- The `--help` output was empty/unhelpful
- Vocabulary was inconsistent (refresh, batch, map, update — four words for two actions)

What we built that the plan didn't anticipate:
- Proper `SKILL.md` at skill root with frontmatter
- `references/user-guide.md`
- Full `--help` cheat sheet showing both AI and CLI commands
- Three-column quick reference table (use case / CLI / AI command)

**Lesson:** Plans for AI-agent skills need a "user interface" section that defines exactly what the user types and what they see. The plan was written from the implementer's perspective, not the user's.

## 3. Naming went through four iterations because the plan picked a bad verb

**Memory type: decision**

The plan called it `refresh`. We renamed it through: `refresh` -> `list` (because it only lists) -> then separated `list` and `update` as two distinct commands -> then killed `batch` and `map` to unify under just `list` + `update`.

The root cause: the plan conflated "discover directories" with "process directories." One subcommand was supposed to do both (list paths for the agent to process). Separating discovery (`list`) from action (`update`) made everything clearer.

**Lesson:** Name commands by what they *do*, not what they're *for*. `refresh` described the goal but not the action.

## 4. `--all` meant different things in different contexts

**Memory type: learning**

The plan defaulted the scan root to `executive-assistant`. The `--all` flag was designed to "skip the picker and output all paths" — but since the scan root was already scoped to one project, `--all` did nothing different from the default.

After clarifying with the user: the scan root should be `~/Documents/github_local`, default scope is `executive-assistant`, and `--all` expands to the full tree. This is a fundamentally different design than the plan specified.

**Lesson:** When a flag has no observable effect in the default case, the defaults are wrong. The `--all` flag only makes sense when the default is already scoped down.

## 5. stdout/stderr separation was right in the plan but not in the existing code

**Memory type: observation**

The plan correctly identified stdout/stderr separation as critical. But the existing `abstract_gen.py` code used a single `Console()` (stdout) for everything — data, errors, warnings, stats. We fixed this across the entire CLI, not just the new subcommand.

Also discovered: Typer's `CliRunner` mixes stdout and stderr, so tests that check output content need `-q` to suppress stderr messages.

## 6. The plan didn't account for skill structure conventions

**Memory type: error**

The plan said to update `map-filesystem.md` (the command file) with orchestration logic. But:
- `SKILL.md` was in `references/` instead of the skill root — wrong per skill-creator conventions
- The command file should just trigger the skill, not contain orchestration logic
- Orchestration belongs in `SKILL.md` so any agent loading the skill gets it

This required a full restructure that the plan didn't anticipate.

## 7. AI commands don't use `--flags`

**Memory type: observation (user preference)**

The user corrected `/map-filesystem list --all` to `/map-filesystem list all`. AI harness commands use natural language, not CLI flag syntax. The plan assumed CLI syntax would flow through to AI commands.

**Feedback for agent:** When designing commands that work in both CLI and AI contexts, separate the syntax. CLI uses `--flags`, AI uses words.

## Summary: what the plan got right vs wrong

| Got right | Got wrong |
|-----------|-----------|
| `has_both=True` scanner filter | TTY assumption ("should support this") |
| stdout/stderr separation principle | Scan root default (`executive-assistant` vs `github_local`) |
| Deduplication by `dir_path` | Command naming (`refresh` for a list operation) |
| Exit codes | Missing user-facing design (no SKILL.md, no user guide, no help) |
| Test pattern | No separation between list and update actions |
| Output contract (one path per line) | Skill structure (SKILL.md in wrong location) |

**Key takeaway for future plans:** Add a "User Experience" section that defines the exact commands the user types, in both CLI and AI contexts, before writing any implementation details.
