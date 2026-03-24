---
owner: Pascal Andy
status: Draft
date_updated: 2026-03-24
---

# feat-1005: idea-map-filesystem

## Abstract

Add a `refresh` subcommand to `abstract_gen.py` that presents an interactive multi-select picker of projects with existing atlas files, then outputs selected paths for the `map-filesystem` slash command to process sequentially.

## Motivation

Running the `map-filesystem` skill one directory at a time is tedious. The scan already discovers all atlas directories. The missing piece is a selection UI that lets the user pick which projects to refresh, then feeds those paths to the AI agent.

## Scope

### In Scope
- New `refresh` subcommand in `abstract_gen.py`
- Interactive multi-select picker (arrow keys + spacebar)
- Group by root project, children visible but not selectable
- Output selected paths (root + children) to stdout
- Update `map-filesystem.md` command to orchestrate refresh + skill invocation
- Sequential processing

### Out of Scope
- Creating new atlases (separate future command)
- Batch/parallel processing (future enhancement)
- Any changes to the `map-filesystem` SKILL.md itself

## Design

### Flow

```
User runs /map-filesystem in OpenCode
  → command calls: uv run abstract_gen.py refresh [path]
  → script scans for dirs with BOTH .abstract.md + .overview.md
  → groups results by root project (direct children of scan path)
  → displays interactive picker:

      [ ] 03_PROJECTS/  (1 child atlas)
          └ analyse_affaires/
      [ ] some_other_project/

  → user selects with spacebar, confirms with enter
  → script prints all paths (selected roots + their children), one per line
  → command reads paths, runs map-filesystem skill on each sequentially
```

### Root project detection

A "root project" is any direct child directory of the scan path that contains atlas files (either itself or in a descendant). Children with their own atlases are grouped under their root and displayed as indented context — visible but not selectable.

### Picker behavior

- Roots: selectable via spacebar
- Children: displayed indented under their root, not selectable
- Child count shown next to root: `03_PROJECTS/  (1 child atlas)`
- Enter confirms selection
- Output: plain paths to stdout, one per line, root first then children

### Default scan path

`~/Documents/github_local/executive-assistant`

## Files to Modify

| File | Change |
|------|--------|
| `dot_config/ai_templates/skills/utils/map-filesystem/scripts/abstract_gen.py` | Add `refresh` subcommand, add `simple-term-menu` dependency |
| `dot_config/ai_templates/commands/map-filesystem.md` | Update to orchestrate: run refresh picker, then invoke skill per path |

## Implementation Steps

1. Add `simple-term-menu` to inline script dependencies
2. Add `refresh` subcommand that:
   - Accepts `path` argument (default: `~/Documents/github_local/executive-assistant`)
   - Reuses existing `Scanner` with `has_both=True`
   - Groups results by first path component relative to scan root
   - Builds picker entries (roots selectable, children as context)
   - Prints selected paths to stdout
3. Update `map-filesystem.md` command to:
   - Run `uv run abstract_gen.py refresh` and capture output
   - For each path, execute the map-filesystem skill instructions

## Future Considerations

- Batch/parallel processing after the sequential flow is validated
- Separate `create` command for generating new atlases
- `--all` flag to skip the picker and refresh everything
