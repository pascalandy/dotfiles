# Config, hooks, and automation

Use this file when the task is about Worktrunk config, shell integration, hook setup, approvals, or automation.

## Show config

```bash
wt config show
wt config show --full
```

Use this to inspect:

- user config
- project config
- system config when present
- diagnostics with `--full`

## Shell integration

```bash
wt config shell install
```

If shell integration is missing, Worktrunk can print the target directory but cannot change the parent shell directory automatically.

That is the first thing to check when `wt switch` seems to work but the shell stays in the old directory.

## Important config ideas

### User config

Typical location:

- `~/.config/worktrunk/config.toml`

Contains personal defaults such as:

- worktree path template
- LLM commit generation settings
- user hooks
- per-project overrides

### Project config

Typical location:

- `.config/wt.toml`

Contains shared repo settings such as:

- hooks
- URL display for `wt list`
- aliases
- CI settings

## Hook lifecycle

Common hook types:

- `post-create`
- `post-start`
- `pre-commit`
- `pre-merge`
- `pre-remove`
- `post-remove`
- `post-merge`

Inspect or run hooks with:

```bash
wt hook --help
wt hook show
wt hook pre-merge
```

## `wt step`

Use `wt step` when the user wants individual pieces of the merge workflow instead of the full `wt merge` pipeline.

Examples:

```bash
wt step commit
wt step squash
wt step rebase
wt step push
wt step diff
wt step copy-ignored
```

`wt step` also supports project aliases.

## Good cases for this file

- “why didn’t `wt switch` cd into the worktree?”
- “show me my Worktrunk config”
- “how do I add tests before merge?”
- “what hook should install dependencies?”
- “can I run only the pre-merge checks?”
