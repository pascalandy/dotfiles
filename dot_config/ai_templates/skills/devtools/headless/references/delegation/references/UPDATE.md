# Update This Skill

## Intro

Triggered when the user says something like "skill headless-delegation, check if we need to update".

This skill is an **orchestrator**. It has no single upstream doc URL. Keep it in sync with the three sibling flag references (`../claude/MetaSkill.md`, `../codex/MetaSkill.md`, `../opencode/MetaSkill.md`) and with observed CLI behavior.

## What to Check For

When updating this skill, verify:

1. **Sibling drift** — did the flag tables in `../claude/MetaSkill.md`, `../codex/MetaSkill.md`, or `../opencode/MetaSkill.md` change in a way that breaks a recipe here?
2. **Execution mode matrix** — does each target CLI still need pty the same way?
   - `claude --print --permission-mode bypassPermissions` should still be the no-pty pattern.
   - `codex exec` and `opencode run` should still require pty.
3. **Permission modes** — did any CLI rename or add permission-mode values?
4. **Trigger robustness** — still strict `use headless-delegation with <cli>`? Still only `{claude, codex, opencode}`?
5. **Boundary with siblings** — is the split with `delegate-to-sub` and `pa-advisor` still crisp?
6. **Gotchas** — any new failure modes observed since last update (e.g., Codex git-repo rule changes, Claude Code pty handling changes)?
7. **New target CLIs** — should `gemini` or `pi` be promoted from out-of-scope to v1?

## Update Checklist

- [ ] Diff the three sibling MetaSkill.md files against the recipes and flag references here.
- [ ] Run `claude --help`, `codex --help`, `opencode --help` and spot-check flags used in the recipes.
- [ ] Smoke test each target CLI (one-shot foreground + one-shot background):
  - [ ] `claude --print --permission-mode plan "echo test"`
  - [ ] `bash pty:true command:"codex exec 'echo test'"` (inside a git repo)
  - [ ] `bash pty:true command:"opencode run 'echo test'"`
- [ ] Confirm the boundary with `delegate-to-sub` and `pa-advisor` still matches the current SKILL.md of each sibling.
- [ ] Update the Gotchas section if new pitfalls are discovered.
- [ ] Bump any recipe that now requires a different flag or permission mode.
