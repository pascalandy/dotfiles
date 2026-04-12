# Alignment Draft: Wiki-Map Scanner

## Request Or Decision

Create a scanner mechanism that finds all wiki-map directories from the current working directory and triggers health-check updates on each. The user invokes this via natural language ("wiki-map update" or "wiki-update") and the system discovers, validates, and maintains all wikis automatically.

## Current State

**Existing wiki-map skill:**
- Located at `dot_config/ai_templates/skills/pa-sdlc/wiki-map/`
- Has three sub-skills: Ingest, Query, Lint
- Lint sub-skill has FullSweep workflow for comprehensive health checks
- Wiki identification requires: `INDEX.md` + `kind/wiki` tag + `references/` subdirectory
- No automated discovery mechanism exists — user must manually specify which wiki to operate on

**Existing scripts pattern:**
- User scripts stored in `dot_local/bin/` with `executable_` prefix
- Scripts follow bash strict mode (`set -euo pipefail`)
- CLI conventions: `--help`, `--version`, `-v` verbose, `--dry-run`
- Scripts are added to PATH via `~/.local/bin`
- **Skill scripts pattern:** Skills can have `scripts/` subdirectory (e.g., `password-generator/scripts/`), with thin wrapper in `dot_local/bin/` that delegates to skill script

**Current wiki locations:**
- `docs/plans/references/2026-04-10-wiki-map-scanner/` is itself a wiki map
- Multiple wiki maps likely exist across the chezmoi repository
- No central registry or index of all wikis exists

## Observed Constraints

1. **Chezmoi source vs applied paths:** All work must happen in `~/.local/share/chezmoi/` (source), not `~/.config/` (applied)
2. **Script naming convention:** Must use `dot_local/bin/executable_` prefix for chezmoi to apply execute permissions
3. **Dual invocation requirement:** Must work as both `wiki-update` and `wiki-map update`
4. **YAML parsing:** No guarantee `yq` is installed; may need fallback parsing
5. **Current directory as root:** Scan starts from `$PWD`, not a fixed location
6. **Skill routing:** "wiki-map update" must route through existing skill system

## Desired End State

**User experience:**
```
User: wiki-map update

AI: Scanning for wiki maps from /Users/andy16/projects...
Found 3 wiki maps (deepest first):
  1. /Users/andy16/projects/docs/plans/subprojects/wiki (depth 5)
  2. /Users/andy16/projects/docs/plans (depth 3)
  3. /Users/andy16/projects/research/health (depth 3)

Running health check on docs/plans/subprojects/wiki...
[FullSweep results]

Running health check on docs/plans...
[FullSweep results]

Running health check on research/health...
[FullSweep results]

Summary: 3 wikis checked, 0 critical, 2 warnings, 5 info
```

**System state:**
- Main script lives in skill: `dot_config/ai_templates/skills/pa-sdlc/wiki-map/scripts/scan-wikis`
- Alias in PATH: `dot_local/bin/executable_wiki-update` (thin wrapper calling skill script)
- `wiki-map` symlink points to `wiki-update`
- Scanner correctly identifies wikis using the three-rule validation
- Skill router handles "wiki-map update" → scanner → FullSweep per wiki
- Script outputs machine-parseable paths (line-separated or JSON)

## Proposed Interaction Or Behavior

**Invocation paths:**

| User says | What happens |
|-----------|--------------|
| "wiki-map update" | AI loads skill → routes to UpdateAll workflow → executes scanner → loops through results → runs FullSweep on each |
| "wiki-update" | Same as above (direct command invocation) |
| "update all my wiki maps" | Same as above (natural language trigger) |
| "wiki-update --json" | Script outputs JSON array of paths, no AI skill trigger |
| "wiki-update --dry-run" | Script shows what it would scan, doesn't execute skill |

**Scanner behavior:**
1. Start from `$PWD`
2. Use `find` to locate all `INDEX.md` files
3. For each INDEX.md found:
   - Check if parent directory contains `references/` subdirectory
   - Parse frontmatter for `kind/wiki` tag
   - If all three conditions met: record absolute path and calculate depth
4. Sort results by depth (deepest first) — children before parents
5. Output sorted paths (deepest to shallowest)
6. Exit 0 if wikis found, exit 1 if none found, exit 2 on error

**Why deepest-first matters:**
- Wiki maps can be nested (parent contains child wiki maps as subdirectories)
- Child wiki content may affect parent wiki links/indexes
- Updating children first ensures parent lint sees current child state
- Example: `/docs/wiki/` (parent) contains `/docs/wiki/projects/wiki/` (child)
  → Update child first, then parent can correctly reference child's current structure

**AI layer behavior:**
1. Capture scanner output (paths already sorted deepest-first)
2. For each path in order: trigger wiki-map skill → Lint → FullSweep
3. Aggregate health reports
4. Present summary to user

**Why order matters:**
- Child wiki maps may contain content referenced by parent wiki maps
- Updating child first ensures parent's FullSweep sees current child state
- Example: Parent INDEX.md links to child wiki pages; child must be linted first

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Script in skill's `scripts/` subdirectory | Best practice for skills; keeps logic with skill; reusable across contexts |
| Thin alias in `dot_local/bin/` | PATH-accessible entry point; follows `passgen` pattern; delegates to skill script |
| Bash (not Python/JS) | Matches existing scripts; no runtime dependencies; fast startup |
| Line-separated paths default | Easy for humans to read; easy for AI to parse with `read` |
| `--json` optional flag | Enables programmatic use without complicating default output |
| Symlink for dual entry | Single source of truth; both commands behave identically |
| Scanner only outputs paths | Separation of concerns: scanner finds, AI acts; script stays simple |
| Three-rule validation hardcoded | Matches idea.md specification exactly; no configuration needed |
| Deepest-first ordering | Nested wiki maps: children must be updated before parents because child content affects parent links/indexes |

## Patterns To Follow

1. **Skill scripts location:** Place main script in `skills/pa-sdlc/wiki-map/scripts/scan-wikis`
2. **Thin wrapper pattern:** `dot_local/bin/executable_wiki-update` just calls skill script (like `passgen`)
3. **Bash strict mode:** `set -euo pipefail` in all scripts
4. **Chezmoi naming:** `dot_local/bin/executable_wiki-update`
5. **CLI conventions:** `--help`, `--version`, `-v` `--dry-run`, `--json`
6. **Function prefixing:** `fct_` prefix for all functions (matches `voxtral.tmpl`)
7. **Error handling:** `fct_die()` for fatal errors with exit codes
8. **Cleanup trap:** `trap 'fct_cleanup' EXIT` for temp files
9. **Skill routing:** Add to wiki-map ROUTER.md, not standalone skill
10. **Progressive disclosure:** Script works standalone; AI adds orchestration layer
11. **Depth calculation:** Calculate directory depth for each found wiki (path component count)
12. **Deepest-first ordering:** Sort by depth descending so children are processed before parents

## Patterns To Avoid

1. **Don't edit applied paths:** Never touch `~/.config/...` directly
2. **Don't duplicate FullSweep logic:** Script finds wikis; skill does health checks
3. **Don't require yq:** Must work without external YAML dependencies if possible
4. **Don't hardcode scan root:** Must use `$PWD`, not fixed path like `~/.local/share/chezmoi`
5. **Don't modify wiki content:** Scanner is read-only; skill handles modifications
6. **Don't create global registry:** Discovery is dynamic, not a maintained list

## Success Signals

| Signal | How to verify |
|--------|---------------|
| Command exists | `which wiki-update` returns path |
| Command runs | `wiki-update --version` shows version |
| Finds wikis | From chezmoi root, finds at least the idea.md wiki |
| Respects rules | Test dir with INDEX.md but no `kind/wiki` tag is excluded |
| Dual entry works | `wiki-map --help` shows same help |
| Depth ordering | Nested wikis output deepest first (child before parent) |
| Skill integration | "wiki-map update" triggers scanner + FullSweep in correct order |
| No regressions | Existing wiki-map workflows still function |

## Open Questions And Risks

**Questions:**
1. Is `yq` available on target systems, or do we need a pure-bash YAML frontmatter parser?
2. Should the scanner follow symlinks when recursing directories?
3. How should the script behave if run from a directory with no wikis (exit 0 with empty output, or exit 1)?
4. Should there be a `--max-depth` limit to prevent runaway scans?
5. How common are nested wiki maps? Should we optimize for flat or nested structures?

**Risks:**
1. **YAML parsing brittleness:** Frontmatter extraction without proper YAML parser could fail on edge cases
2. **Performance on large trees:** Deep directory structures could make scanning slow
3. **Skill routing collision:** "update" is a common word; could trigger unexpectedly
4. **False positives:** Malformed INDEX.md files might be misidentified as wikis
5. **Nested wiki complexity:** Parent-child relationships could create circular dependencies or ordering edge cases

**Mitigations:**
- Use `find` with `-maxdepth` option (configurable, default unlimited but warned)
- Implement basic frontmatter extraction with awk as fallback
- Test routing patterns thoroughly against existing triggers
- Validate all three rules strictly before reporting a wiki
- Calculate depth using path component count and sort descending (deepest first)
- Document that circular nesting (child referencing parent as child) is not supported

## What Needs Human Review

1. **Script name in skill:** `scan-wikis` or alternative? (e.g., `wiki-scan`, `find-wikis`, `discover`)
2. **Command naming:** Is `wiki-update` the right name for the alias? Alternatives: `wm-update`, `wiki-scan`, `wmap`?
3. **Exit code behavior:** Should "no wikis found" be exit 0 (success, just empty) or exit 1 (error condition)?
4. **Output format default:** Line-separated paths, or JSON as default for easier AI parsing?
5. **YAML dependency:** Accept `yq` as requirement, or implement pure-bash fallback?
6. **Max depth:** Should there be a default depth limit (e.g., 10 levels) or scan unlimited?
7. **Skill routing:** Should "wiki-map update" route to this, or should it be a separate sub-skill like `wiki-map/UpdateAll/`?

## Recommended Next Phase

`pa-architect` — Once alignment is confirmed on:
- Command names and invocation patterns
- Output format and exit codes
- YAML parsing strategy
- Skill routing approach

Then proceed to execution planning with phases for: (1) core scanner script in skill `scripts/` directory, (2) thin wrapper alias in `dot_local/bin/`, (3) dual entry point symlink, (4) skill integration, (5) polish.
