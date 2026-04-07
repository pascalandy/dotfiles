---
title: "feat: Add interactive refresh picker to abstract_gen.py"
type: feat
  - status/close
date: 2026-03-24
origin: docs/features/feat-1005/idea-map-filesystem.md
---

# feat: Add interactive refresh picker to abstract_gen.py

## Overview

Add a `refresh` subcommand to `abstract_gen.py` that scans for directories with existing atlas files, presents an interactive multi-select picker grouped by root project, and outputs selected paths to stdout for the `map-filesystem` command to process sequentially.

## Problem Statement

Running `/map-filesystem` one directory at a time is tedious. The Scanner already discovers all atlas directories. The missing piece is a selection UI that lets the user pick which projects to refresh, then feeds those paths to the AI agent. (see origin: `docs/features/feat-1005/idea-map-filesystem.md`)

## Proposed Solution

1. New `refresh` subcommand in `abstract_gen.py` using the existing thin-wrapper pattern
2. Reuse `Scanner` with `has_both=True` to find directories containing both `.abstract.md` and `.overview.md`
3. Group results by root project (first path component relative to scan root)
4. Display interactive picker with `simple-term-menu` — roots selectable, children as indented context
5. Print selected directory paths (absolute, one per line) to stdout
6. Update `map-filesystem.md` command to orchestrate: call refresh, iterate paths, invoke skill per path

## Technical Considerations

### stdout/stderr separation (Critical)

The picker UI **must** render to stderr (`Console(stderr=True)`). Path output goes to raw `print()` on stdout. Without this separation, Rich console output from the picker will corrupt the parseable path list. This is the standard Unix convention for tools whose output is piped.

### TTY passthrough

`simple-term-menu` requires an interactive TTY. OpenCode's Bash tool runs in a persistent shell session that should support this. However, the `--all` flag provides a non-interactive fallback and should ship with v1 to eliminate this risk entirely. The command should default to `--all` when orchestrating, and the picker is available for manual invocations.

### AtlasFile deduplication

`Scanner` with `has_both=True` returns individual `AtlasFile` objects (one per file). A directory with both files produces **two** entries. The refresh logic must deduplicate by `atlas.dir_path` before grouping.

### Scan root handling

If the scan root itself has atlas files, it doesn't fit the "direct child" grouping model. Display it as `. (root)` at the top of the picker, selectable like any root.

### Output contract

- One absolute directory path per line
- No trailing slash
- No Rich markup or decorative output on stdout
- Empty stdout = user cancelled or nothing selected (exit 0)

### Library choice

The idea doc specifies `simple-term-menu`. An alternative is `questionary` (already used in archived `extract_repo.py`) which has native `Choice(disabled=...)` for non-selectable children. Either works; `simple-term-menu` is lighter. Decision: use `simple-term-menu` as specified — non-selectable children can be rendered as styled text entries with a custom format.

## Acceptance Criteria

- [ ] `uv run abstract_gen.py refresh` scans default path and shows picker
- [ ] `uv run abstract_gen.py refresh /custom/path` scans custom path
- [ ] `uv run abstract_gen.py refresh --all` prints all paths without picker
- [ ] Picker groups directories by root project with child count
- [ ] Children displayed indented under root, not selectable
- [ ] Selecting a root outputs that root + all its child atlas directories
- [ ] Paths output as absolute directory paths, one per line, to stdout
- [ ] Picker UI renders to stderr (no stdout pollution)
- [ ] Empty scan results → exit code 2, message to stderr
- [ ] User cancels picker → exit 0, empty stdout
- [ ] Tests pass: `uv run pytest` in scripts directory
- [ ] Updated `map-filesystem.md` command orchestrates refresh → skill loop

## Implementation Phases

### Phase 1: `refresh` subcommand in `abstract_gen.py`

**Files:**

| File | Change |
|------|--------|
| `dot_config/ai_templates/skills/utils/map-filesystem/scripts/abstract_gen.py` | Add `simple-term-menu` to PEP 723 deps, add `refresh` subcommand |

**Tasks:**

1. Add `simple-term-menu` to inline script dependencies (line 6):
   ```python
   # dependencies = [
   #     "typer>=0.9.0",
   #     "rich>=13.0.0",
   #     "pyyaml>=6.0",
   #     "tomli-w>=1.0",
   #     "simple-term-menu>=1.6.0",
   # ]
   ```

2. Add `refresh` subcommand (~40-60 lines) following existing pattern (`validate`/`orphans` are thin wrappers):

   ```python
   # abstract_gen.py — new subcommand
   @app.command()
   def refresh(
       path: Annotated[Path, typer.Argument(help="Directory to scan")] = Path.home() / "Documents/github_local/executive-assistant",
       all_projects: Annotated[bool, typer.Option("--all", help="Skip picker, output all paths")] = False,
       quiet: Annotated[bool, typer.Option("--quiet", "-q")] = False,
   ) -> None:
       """Select projects with existing atlases to refresh."""
       stderr_console = Console(stderr=True)
       resolved = path.expanduser().resolve()
       if not resolved.is_dir():
           stderr_console.print(f"[red]Error:[/red] {resolved} is not a directory")
           raise typer.Exit(1)

       # Scan for dirs with both atlas files
       config = ScannerConfig(root_path=resolved, has_both=True, quiet=quiet)
       scanner = Scanner(config)
       atlases = scanner.scan()
       if not atlases:
           stderr_console.print("[yellow]No directories with both atlas files found.[/yellow]")
           raise typer.Exit(2)

       # Deduplicate by directory
       atlas_dirs = sorted({a.path.parent for a in atlases})

       # Group by root project (first component relative to scan root)
       groups: dict[str, list[Path]] = {}
       for d in atlas_dirs:
           try:
               rel = d.relative_to(resolved)
               root_name = rel.parts[0] if rel.parts else "."
           except ValueError:
               root_name = d.name
           groups.setdefault(root_name, []).append(d)

       if all_projects:
           for d in atlas_dirs:
               print(d)
           raise typer.Exit(0)

       # Build picker entries
       from simple_term_menu import TerminalMenu
       entries = []
       entry_to_root = {}
       for root_name, dirs in sorted(groups.items()):
           children = [d for d in dirs if d != resolved / root_name]
           child_count = f"  ({len(children)} child atlas{'es' if len(children) != 1 else ''})" if children else ""
           entry = f"{root_name}/{child_count}"
           entries.append(entry)
           entry_to_root[len(entries) - 1] = root_name
           for child in children:
               rel_child = child.relative_to(resolved / root_name)
               entries.append(f"    └ {rel_child}")
               # Not mapped in entry_to_root → not selectable

       # Determine which indices are selectable (roots only)
       selectable = list(entry_to_root.keys())

       menu = TerminalMenu(
           entries,
           multi_select=True,
           show_multi_select_hint=True,
           preselected_entries=None,
           accept_keys=("enter",),
           multi_select_select_on_accept=False,
           multi_select_empty_ok=True,
       )
       # Note: simple-term-menu doesn't natively support non-selectable entries.
       # Alternative: use skip indices or a custom approach.
       selected = menu.show()

       if selected is None:
           raise typer.Exit(0)

       # Output paths for selected roots
       selected_indices = selected if isinstance(selected, tuple) else (selected,)
       for idx in selected_indices:
           if idx in entry_to_root:
               root_name = entry_to_root[idx]
               for d in groups[root_name]:
                   print(d)
       raise typer.Exit(0)
   ```

   **Note:** The pseudo-code above illustrates the pattern. The actual implementation should handle `simple-term-menu`'s API for non-selectable entries — this may require using `skip_empty_entries` or prepending non-selectable entries with a marker. If `simple-term-menu` cannot support non-selectable rows cleanly, fall back to showing only root entries (with child counts) and skip displaying children inline.

3. Add tests in `scripts/tests/test_cli.py`:

   ```python
   # test_cli.py — new test class
   class TestRefresh:
       def test_refresh_all(self, tmp_repo: Path) -> None:
           result = runner.invoke(app, ["refresh", str(tmp_repo), "--all"])
           assert result.exit_code == 0
           paths = result.output.strip().split("\n")
           assert len(paths) >= 1

       def test_refresh_empty(self, tmp_path: Path) -> None:
           result = runner.invoke(app, ["refresh", str(tmp_path), "--all"])
           assert result.exit_code == 2

       def test_refresh_nonexistent(self, tmp_path: Path) -> None:
           result = runner.invoke(app, ["refresh", str(tmp_path / "nope")])
           assert result.exit_code == 1
   ```

### Phase 2: Update `map-filesystem.md` command

**File:**

| File | Change |
|------|--------|
| `dot_config/ai_templates/commands/map-filesystem.md` | Add orchestration logic for refresh mode |

Update the command to support two modes:

```markdown
---
name: map-filesystem
metadata:
  author: Pascal Andy
---

## Mode: Refresh (batch)

When the user says "refresh" or wants to update multiple projects:

1. Run `uv run abstract_gen.py refresh --all [path]` to get list of atlas directories
2. For each path in the output:
   - Announce: "Refreshing atlas for: <path>"
   - Execute the map-filesystem skill instructions with that path as the working directory
   - If the skill fails, log the error and continue to the next path
3. After all paths processed, summarize: N succeeded, M failed

## Mode: Single (default)

Execute instructions within the skill: `map-filesystem`
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (or user cancelled picker — empty stdout) |
| 1 | Runtime error (bad path, etc.) |
| 2 | No atlas directories found |

## Dependencies & Risks

| Risk | Mitigation |
|------|------------|
| `simple-term-menu` TTY issues in OpenCode's Bash | `--all` flag bypasses picker entirely; command defaults to `--all` |
| Non-selectable children not natively supported by `simple-term-menu` | Show only roots in picker with child count; skip inline child display if API doesn't support it cleanly |
| Rich output polluting stdout | Use `Console(stderr=True)` for all non-path output |

## Future Considerations

- `--all` flag to skip picker (included in v1 per recommendation)
- Batch/parallel processing after sequential flow is validated
- Separate `create` command for generating new atlases
- Granular child selection in picker
- `--dry-run` to show what would be refreshed without running the skill

## Sources

- **Origin document:** [docs/features/feat-1005/idea-map-filesystem.md](docs/features/feat-1005/idea-map-filesystem.md) — defines the feature scope, design, and implementation steps
- Existing subcommand pattern: `abstract_gen.py:105` (`validate`), `abstract_gen.py:122` (`orphans`)
- Scanner interface: `lib/scanner.py:75` (`ScannerConfig`), `lib/scanner.py:95` (`scan()`)
- Data models: `lib/models.py:44` (`AtlasFile`)
- Archived picker example: `skills_archived/extract-repo/scripts/extract_repo.py:216` (uses `questionary`)
- Test pattern: `scripts/tests/test_cli.py` (uses `typer.testing.CliRunner`)
