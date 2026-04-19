# Plan — Skills Reorg (2026-04-18)

Source: `idea-skills-reorg-v4.md`. v4 confirmed 54 skills on disk map 1:1 to 54 skills in the target layout across 8 buckets, with 45 moves and 9 stays.

## Scope

- Source of truth: `dot_config/ai_templates/skills/` (chezmoi source).
- Applied copies at `~/.config/*/skill/` and `~/.{claude,codex,gemini,factory,pi}/skills/` are downstream — never edited directly.
- Downstream layout is **flat** (per `fct_compile_assets` in `.chezmoiscripts/run_after_backup.sh`): bucket names are purely organizational in chezmoi source. No downstream path migration needed.

## Open questions (confirm before Phase 1)

1. Branch or main? (proposed: `reorg/skills-v4` → PR)
2. Commit granularity — one bundled commit, or per-bucket? (proposed: one bundled; it's a pure rename batch)
3. Reference-hunt scope — this repo only, or also external configs in `~/.claude/` and `~/.codex/`? (proposed: this repo only, since downstream is flat)

## Phase 1 — Pre-flight (read-only)

1. Re-count: `fd SKILL.md dot_config/ai_templates/skills/ | wc -l` must equal **54**.
2. Diff the on-disk list against v4's target map — zero drift expected.
3. Reference hunt for hard-coded paths:
   - `rg "skills/(pa-sdlc|meta|specs|utils)/" dot_config/ docs/ .chezmoiscripts/`
   - Inspect `.chezmoiscripts/run_after_backup.sh` (known hit: lines 84, 93).
   - Inspect `ROUTER.md` files inside `headless/` and `distill-prompt/` for any relative `../` paths that would break after a bucket move.
4. Working tree clean; branch off `main`.

## Phase 2 — Create 7 new buckets

`pa-sdlc/` already exists. Create under `dot_config/ai_templates/skills/`:

- `devtools/`
- `think/`
- `knowledge/`
- `web/`
- `distill/`
- `diagram/`
- `media/`

## Phase 3 — Move skills (45 moves, `git mv`)

Per v4 map. Use `git mv` to preserve history.

| New bucket | Count | Source | Notes |
|---|---|---|---|
| pa-sdlc | 9 | pa-sdlc/ | stay (no-op) |
| devtools | 12 | pa-sdlc/, specs/, utils/ | includes `headless/` meta-skill |
| think | 4 | meta/, specs/ | |
| knowledge | 9 | pa-sdlc/, utils/ | |
| web | 7 | meta/, utils/ | |
| distill | 6 | pa-sdlc/, meta/, utils/ | includes `distill-prompt/` meta-skill |
| diagram | 2 | utils/ | |
| media | 5 | meta/, specs/, utils/ | |

**Meta-skills** (`headless/`, `distill-prompt/`): `git mv` the entire directory tree (ROUTER.md + all `references/` subdirs) in one operation. Do NOT move `SKILL.md` alone.

After moves, the old `meta/`, `specs/`, `utils/` directories should be empty — remove them.

## Phase 4 — Fix internal references

- Apply edits to any path hits from Phase 1 step 3.
- Verify `headless/ROUTER.md` and `distill-prompt/ROUTER.md` still resolve sub-skills (relative paths inside the moved subtree should be unaffected; confirm).
- Supersede or annotate `idea-skills-reorg-v4.md` with an outcome note pointing to the final commit.

## Phase 5 — Adjust `.chezmoiscripts/run_after_backup.sh`

### Why this step matters

The chezmoi source uses bucketed subdirectories (`pa-sdlc/`, `devtools/`, `think/`, …) for human organization. But downstream agents have heterogeneous rules about skill layout:

- Some agents (Claude Code, Codex, several others) expect skills at the **top level** of their skills directory. They do not recurse into subdirectories — a skill nested under `skills/devtools/commit/SKILL.md` is invisible to them; it must appear as `skills/commit/SKILL.md`.
- Other agents tolerate either structure.

To keep one organized source of truth and still satisfy the strictest agents, the sync script **flattens** bucket subdirectories into a single flat directory before copying to each agent home. Bucket names exist only in the chezmoi source — they never appear in any agent's skills tree.

### How the current script flattens

`fct_compile_assets()` (lines 75–102 of `run_after_backup.sh`) implements this:

1. Looks for any of the known bucket subdirectories under `skills_src`.
2. If found (“categorized” mode): copies the **contents** of each bucket (`$src_dir/$category/*`) into a flat tempdir — bucket directories themselves are stripped.
3. If none found (“flat” mode): copies `$src_dir/*` directly.
4. `fct_sync_agent_assets()` then rsyncs that flat tempdir to all 8 agent homes (`~/.config/opencode/skills`, `~/.pi/agent/skills`, `~/.claude/skills`, `~/.codex/skills`, `~/.gemini/skills`, `~/.config/amp/skills`, `~/.config/agents/skills`, `~/.factory/skills`).

### What must change

The bucket list is hard-coded **twice** inside `fct_compile_assets`:

- Line 84 — detection loop (decides whether source is categorized).
- Line 93 — compile loop (iterates buckets to copy).

Both must enumerate the new 8-bucket set. Replace:

```bash
for category in meta pa-sdlc specs utils; do
```

with:

```bash
for category in pa-sdlc devtools think knowledge web distill diagram media; do
```

Order matches v4's workflow arc (lifecycle spine → code-adjacent tooling → reasoning → memory → external research → transformation → visualization → creative output). Order is cosmetic for the flatten step but keeps the script legible against v4.

### Pre-flatten collision check (critical)

Because flattening strips the bucket name, two skills with the same directory name in different buckets would collide — the second `cp -r` would overwrite the first, silently. v4 claims zero drift, but before Phase 6 run:

```bash
fd -t d -d 1 . dot_config/ai_templates/skills/{pa-sdlc,devtools,think,knowledge,web,distill,diagram,media} \
  | awk -F/ '{print $NF}' | sort | uniq -d
```

Expected output: empty. Any lines returned are duplicate skill names across buckets — resolve before syncing (rename one, or keep both in the same bucket).

### Post-flatten validation

After `just cm-apply-verbose`:

```bash
# Each agent home should contain exactly 54 top-level entries, zero bucket dirs.
for d in ~/.config/opencode/skills ~/.claude/skills ~/.codex/skills \
         ~/.gemini/skills ~/.config/amp/skills ~/.config/agents/skills \
         ~/.factory/skills ~/.pi/agent/skills; do
  count=$(fd -t d -d 1 . "$d" | wc -l | tr -d ' ')
  printf '%s -> %s dirs\n' "$d" "$count"
done
```

Every line should report **54**. Any number other than 54 means either a bucket leaked through (script didn't strip it) or a skill was lost in the move.

### Script-code cleanup (optional, same commit)

The `meta pa-sdlc specs utils` list duplicates itself on two adjacent loops. Worth lifting into a local array at the top of `fct_compile_assets` so the 8-bucket list lives in one place:

```bash
local -a categories=(pa-sdlc devtools think knowledge web distill diagram media)
```

Low risk, clearly in scope, avoids future drift. Skip if you prefer a minimal diff.

## Phase 6 — Validate & sync

1. `just cm-apply-dry` — review diff.
2. `just cm-apply-verbose` — sync to all 8 agent homes.
3. Spot-check: `ls ~/.claude/skills/ | wc -l` should still return 54. Repeat for at least one other agent home (`~/.codex/skills`, `~/.config/opencode/skills`).
4. Invoke a skill from each new bucket to confirm discovery still works (at least one skill per bucket).
5. `just ci` (gitleaks, shellcheck, shfmt).

## Phase 7 — Commit & PR

- Bundled commit (proposed): `♻️ refactor(skills): reorganize into 8 workflow-arc buckets`.
- Commit body references `idea-skills-reorg-v4.md` and this plan.
- Open PR against `main` if Phase 1 answer was "branch".

## Rollback

Pre-reorg state is one `git reset --hard <sha>` away. Downstream copies are regenerated by `chezmoi apply`, so rollback = revert + reapply.

## Stats

- SKILL.md on disk: **54**
- Moves: **45** · Stays: **9**
- New directories to create: **7**
- Old directories to remove after moves: **3** (`meta/`, `specs/`, `utils/`)
- Scripts to adjust: **1** (`.chezmoiscripts/run_after_backup.sh`, 2 lines)
- Meta-skills to preserve intact: **2** (`headless/`, `distill-prompt/`)
