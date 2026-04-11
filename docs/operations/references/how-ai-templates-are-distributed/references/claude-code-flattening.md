---
name: Claude Code Flattening Gotcha
description: How `~/.claude/skills/` is produced by four rsync calls into a shared destination and why, in the current script, only the last subtree survives
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-ai-templates-are-distributed
---

This is the most surprising page in this wiki. The fan-out script *intends* to flatten four source subtrees (`meta/`, `pa-sdlc/`, `specs/`, `utils/`) into `~/.claude/skills/` so Claude Code's loader, which expects skills directly under its skills directory, can find them all. **In the committed script that intent is not achieved.** Only the `utils/` subtree survives a full apply.

Read the verification in this page before trusting any other claim about flattening behavior in this repo.

> **Work in progress.** As of 2026-04-11, the repo's working tree has an uncommitted refactor to `.chezmoiscripts/run_after_backup.sh` that replaces the four-call pattern described here with a new `fct_compile_assets` function. The refactor pre-compiles all four subtrees into a single flat directory via additive `cp -r`, then each agent receives one rsync call from that compiled directory. When committed and applied, this fix eliminates the "only `utils/` survives" bug and **applies the flattening uniformly to every agent home**, not just Claude Code. This page still documents committed behavior; see [wip-compile-refactor](#wip-compile-refactor) at the bottom for the in-flight change.

## The four calls

From `.chezmoiscripts/run_after_backup.sh:88-92`:

```bash
# Claude Code
fct_copy_dir "$commands_src" "$HOME/.claude/commands"
fct_copy_dir "$skills_src/meta"    "$HOME/.claude/skills"
fct_copy_dir "$skills_src/pa-sdlc" "$HOME/.claude/skills"
fct_copy_dir "$skills_src/specs"   "$HOME/.claude/skills"
fct_copy_dir "$skills_src/utils"   "$HOME/.claude/skills"
```

Every call routes through `fct_copy_dir` with the default `sync_mode=delete`, which expands to:

```bash
rsync -a --exclude '.DS_Store' --delete --delete-excluded --force \
  "$skills_src/<subtree>/" "$HOME/.claude/skills/"
```

The trailing slashes on both sides mean rsync copies the *contents* of the subtree into `~/.claude/skills/` rather than the subtree directory itself. Each call also runs with `--delete`, which removes destination files that are not present in the current source.

## Why the merge does not actually happen

Because all four calls share a destination and each one runs `--delete`, every call wipes the previous call's contribution. The sequence is:

1. **Call 1 (`meta/`)** copies meta contents into `~/.claude/skills/`, deletes anything already there. After this call: `~/.claude/skills/` = contents of `meta/`.
2. **Call 2 (`pa-sdlc/`)** copies pa-sdlc contents into `~/.claude/skills/`, deletes anything not in `pa-sdlc/`. This removes the meta contents from step 1. After this call: `~/.claude/skills/` = contents of `pa-sdlc/`.
3. **Call 3 (`specs/`)** does the same again. After: `~/.claude/skills/` = contents of `specs/`.
4. **Call 4 (`utils/`)** runs last. After: `~/.claude/skills/` = contents of `utils/`.

The last call wins, unconditionally. The order in `.chezmoiscripts/run_after_backup.sh:89-92` puts `utils/` last, so `utils/` is the only subtree that survives.

## Verification

As of 2026-04-11, on this machine:

```bash
# Compare ~/.claude/skills/ to each source subtree
diff <(ls ~/.claude/skills/) <(ls ~/.local/share/chezmoi/dot_config/ai_templates/skills/utils/)
# → empty output: ~/.claude/skills/ is exactly equal to utils/
```

Every entry in `~/.claude/skills/` — `agent-browser`, `beads`, `browser-use`, `byterover`, `cass`, `cm`, `defuddle`, `edit-note`, `headless-claude`, `headless-codex`, `headless-opencode`, `last30days`, `map-filesystem-abstract`, `mermaid`, `mermaid-og`, `meta-skill-creator`, `nano-banana-sk`, `nia-docs`, `pg-memory`, `plantuml-ascii`, `shorthand-interpreter`, `single-skill-creator`, `tavily`, `transcript-sk`, `trello`, `voxtral`, `writer-sk` — is a child of `utils/`. None of the `meta/`, `pa-sdlc/`, or `specs/` skills are present.

The same behavior can be reproduced in isolation:

```bash
# Two source trees with different contents, rsync each into the same destination
mkdir -p /tmp/claudeflat/{src1/a,src2/b,dst}
touch /tmp/claudeflat/src1/a/file1 /tmp/claudeflat/src2/b/file2
rsync -a --delete /tmp/claudeflat/src1/ /tmp/claudeflat/dst/
rsync -a --delete /tmp/claudeflat/src2/ /tmp/claudeflat/dst/
ls /tmp/claudeflat/dst/
# → only `b` remains; `a` was deleted by the second rsync
```

This matches the reproduction used while writing this page.

## Implications

1. **Every `pa-sdlc/*` skill (including every `pa-*` stage skill) is invisible to Claude Code** under the current script. The source files exist in `dot_config/ai_templates/skills/pa-sdlc/`; they ship correctly to OpenCode, Pi, Codex, Amp, Agents, and Factory; Claude Code sees nothing.
2. **Every `meta/*` and `specs/*` skill is also invisible to Claude Code.**
3. **Skill naming collisions between subtrees are not the problem to worry about.** The real problem is that three of the four subtrees are wiped before Claude Code ever reads them.
4. **The CLAUDE.md and this repo's prior documentation describe the intended merge behavior, not the actual one.** The code in `.chezmoiscripts/run_after_backup.sh:89-92` contradicts it.

## Fixes (not applied by this wiki)

Three approaches would restore the intended merge. Any one of them would work; this wiki only documents the options.

1. **Switch the four calls to `sync_mode=merge`.** Pass a fourth argument of `merge` (or any non-`delete` string) to `fct_copy_dir` so the rsync omits `--delete`. The function's design supports this at `.chezmoiscripts/run_after_backup.sh:24-33` — the mode is parameterized — but the current calls pass only the first two arguments and inherit the default. Downside: a deleted skill in the source will no longer be pruned from `~/.claude/skills/` on apply, and orphaned copies would accumulate.
2. **Collapse the four calls into one.** Build an intermediate directory that already has all four subtrees flattened (e.g. `cp -a $skills_src/{meta,pa-sdlc,specs,utils}/* $tmp/`) and run a single `rsync --delete` from that staging directory to `~/.claude/skills/`. Preserves `--delete` semantics and prunes deleted source skills correctly. Requires handling name collisions explicitly because two sources with the same skill name will overwrite each other in the staging copy.
3. **Use rsync's `--link-dest` or stacked `--include`/`--exclude` rules** to express "mirror all four subtrees into one destination" in a single call. More complex; not obviously simpler than option 2.

None of these fixes are made in this documentation pass. This wiki only describes current behavior. A decision and a fix should be handled in a separate task. See the LOG entry on this wiki for the discovery date and context.

## Temporary workaround for the human operator

If you need a pa-sdlc skill in Claude Code *today*, the fastest unblock is to manually `cp -a` the subtree into `~/.claude/skills/` after every apply. This is a workaround, not a fix — it will survive until the next apply, at which point the `utils/` rsync call will delete it again.

A slightly more durable workaround is to temporarily rename the source subtree so that pa-sdlc skills live under `dot_config/ai_templates/skills/utils/pa-sdlc-<name>/`. Then they ride along with the `utils/` call and survive every apply. This also leaks the rename into every other agent home, where the subtree split is respected — so do it only if you are willing to see `pa-sdlc-<name>` appear under `~/.config/opencode/skills/utils/` and similar. This workaround collides with this repo's existing skill-organization conventions.

## WIP compile refactor

A staged, uncommitted change in `.chezmoiscripts/run_after_backup.sh` replaces the four-call pattern with a pre-compile step. The new shape is:

```bash
fct_compile_assets() {
    local src_dir="$1"
    local compile_dir="$2"

    mkdir -p "$compile_dir"
    # If src has category subdirs, additively cp -r each into compile_dir.
    # Otherwise cp -r flat contents directly.
    ...
}
```

`fct_sync_agent_assets` creates two `mktemp -d` compile directories (one for commands, one for skills), calls `fct_compile_assets` on each rendered source, and then hands the compiled directories to a *single* `fct_copy_dir` call per agent. The key changes:

1. **Additive compilation.** `cp -r "$src_dir/$category/"* "$compile_dir/"` runs once per category with no `--delete`. All four subtrees land as peers in the compile directory.
2. **One rsync per agent.** Each agent's `~/<agent>/skills/` receives one `fct_copy_dir --delete` call against the compile directory. The shared-destination problem goes away because no agent target is written to more than once per apply.
3. **Uniform flattening for every agent.** The compiled skills directory is the same for OpenCode, Pi, Claude Code, Codex, Gemini, Amp, Agents, and Factory. **Every agent now sees the flat shape**, not just Claude Code. The subtree organization (`meta/`, `pa-sdlc/`, `specs/`, `utils/`) becomes source-only metadata — it disappears in every agent home.
4. **Gemini now receives skills.** The old script sent only commands to Gemini. The new script fans out skills to Gemini as well.

Collision handling under the new shape: if two source subtrees contain a skill with the same directory name, the four per-category `cp -r` calls run in order (`meta`, `pa-sdlc`, `specs`, `utils`), and the later one overwrites the earlier one. `cp -r "$src/$category/"*` is lenient enough to not fail on file collisions, but the result is still "last write wins". Naming collisions are still a real concern under the refactor — they are just newly relevant to *every* agent instead of Claude Code alone.

The refactor is not yet committed. The filesystem state verified earlier in this page (`~/.claude/skills/` == `utils/`) reflects the *committed* script, which is the one that ran the last `chezmoi apply`. Once the refactor is committed and applied, the verification will change to reflect the new uniform flattening.

## Related

- [[overview]]
- [[fan-out-targets]]
- [[rsync-semantics]]
- [[troubleshooting]]
