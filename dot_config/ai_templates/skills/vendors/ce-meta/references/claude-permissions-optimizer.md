# claude-permissions-optimizer

> Analyze Claude Code session history to find safe Bash commands that are causing unnecessary permission prompts, then auto-apply them to `settings.json` — evidence-based, not prescriptive.

## When to Use

- User experiences permission fatigue or too many permission prompts.
- User wants to optimize permissions or set up allowlists.
- Triggers: "optimize permissions", "reduce permission prompts", "allowlist commands", "too many permission prompts", "permission fatigue", "permission setup", complaints about clicking approve too often.

This skill identifies commands safe to auto-allow based on actual session history. It does not handle requests to allowlist specific dangerous commands. If the user asks to allow something destructive (e.g., `rm -rf`, `git push --force`), explain that this skill optimizes for safe commands only, and that manual allowlist changes can be made directly in `settings.json`.

## Inputs

- Access to `~/.claude/` (or `$CLAUDE_CONFIG_DIR`) on the local machine.
- The bundled `extract-commands.mjs` script (located in the skill's `scripts/` directory).
- Optional: a project slug to limit analysis to one project.

## Methodology

### Pre-check: Confirm Environment

Determine whether running inside Claude Code or a different coding agent (Codex, Gemini CLI, Cursor, etc.).

**If running inside Claude Code:** Proceed directly to Step 1.

**If running in a different agent:** Inform the user before proceeding:

> "This skill analyzes Claude Code session history and writes to Claude Code's settings.json. You're currently in [agent name], but I can still optimize your Claude Code permissions from here — the results will apply next time you use Claude Code."

Then proceed to Step 1 normally. The skill works from any environment as long as `~/.claude/` (or `$CLAUDE_CONFIG_DIR`) exists on the machine.

---

### Step 1: Choose Analysis Scope

Prompt the user to choose analysis scope (present as numbered options and wait for a reply if no interactive question tool is available):

1. **All projects** (Recommended) — sessions across every project.
2. **This project only** — sessions for the current working directory.
3. **Custom** — user specifies constraints (time window, session count, etc.).

Default to **All projects** unless the user explicitly asks for a single project. More data produces better recommendations.

---

### Step 2: Run Extraction Script

Run the bundled script. It handles everything: loads the current allowlist, scans recent session transcripts (most recent 500 sessions or last 30 days, whichever is more restrictive), filters already-covered commands, applies a min-count threshold (5+), normalizes into `Bash(pattern)` rules, and pre-classifies each as safe/review/dangerous.

**All projects:**
```bash
node <skill-dir>/scripts/extract-commands.mjs
```

**This project only** — pass the project slug (absolute path with every non-alphanumeric char replaced by `-`, e.g., `/Users/tmchow/Code/my-project` becomes `-Users-tmchow-Code-my-project`):
```bash
node <skill-dir>/scripts/extract-commands.mjs --project-slug <slug>
```

Optional: `--days <N>` to limit to the last N days. Omit to analyze all available sessions.

**Script output JSON structure:**
- `green`: safe patterns to recommend — `{ pattern, count, sessions, examples }`
- `redExamples`: top 5 blocked dangerous patterns — `{ pattern, reason, count }` (or empty array)
- `yellowFootnote`: one-line summary of frequently-used commands that aren't safe to auto-allow (or null)
- `stats`: `totalExtracted`, `alreadyCovered`, `belowThreshold`, `patternsReturned`, `greenRawCount`, `sessionsScanned`, `filesScanned`, `allowPatternsLoaded`, `daysWindow`, `minCount`, `yellowSkipped`, `redBlocked`, `unclassified`

The agent's job is to **present** the script's output, not re-classify.

If the script returns empty results, tell the user their allowlist is already well-optimized or they don't have enough session history yet — suggest re-running after a few more working sessions.

---

### Step 3: Present Results

Present in three parts. Keep the formatting clean and scannable.

#### Part 1: Analysis Summary

Show the work done using the script's `stats`. Reaffirm the scope. Keep it to 4-5 lines.

**Example:**
```
## Analysis (compound-engineering-plugin)

Scanned **24 sessions** for this project.
Found **312 unique Bash commands** across those sessions.

- **245** already covered by your 43 existing allowlist rules (79%)
- **61** used fewer than 5 times (filtered as noise)
- **6 commands** remain that regularly trigger permission prompts
```

#### Part 2: Recommendations

Present `green` patterns as a numbered table. If `yellowFootnote` is not null, include it as a line after the table.

```
### Safe to auto-allow
| # | Pattern | Evidence |
|---|---------|----------|
| 1 | `Bash(bun test *)` | 23 uses across 8 sessions |
| 2 | `Bash(bun run *)` | 18 uses, covers dev/build/lint scripts |
| 3 | `Bash(node *)` | 12 uses across 5 sessions |

Also frequently used: bun install, mkdir (not classified as safe to auto-allow but may be worth reviewing)
```

If `redExamples` is non-empty, show a compact "Blocked" table after the recommendations. Show up to 3 examples.

```
### Blocked from recommendations
| Pattern | Reason | Uses |
|---------|--------|------|
| `rm *` | Irreversible file deletion | 21 |
| `eval *` | Arbitrary code execution | 14 |
| `git reset --hard *` | Destroys uncommitted work | 5 |
```

#### Part 3: Bottom Line

**One sentence only.** Frame the impact relative to current coverage using the script's stats. Nothing else — no pattern names, no usage counts, no elaboration.

**Example:**
```
Adding 22 rules would bring your allowlist coverage from 65% to 93%.
```

Compute the percentages from stats:
- **Before:** `alreadyCovered / totalExtracted * 100`
- **After:** `(alreadyCovered + greenRawCount) / totalExtracted * 100`

Use `greenRawCount` (the number of unique raw commands the green patterns cover), not `patternsReturned` (which is just the number of normalized patterns).

---

### Step 4: Get User Confirmation

Present the decision as numbered options (use a blocking question tool if available, otherwise present and wait for a reply):

1. **Apply all to user settings** (`~/.claude/settings.json`)
2. **Apply all to project settings** (`.claude/settings.json`)
3. **Skip**

If the user wants to exclude specific items, they can reply in free text (e.g., "all except 3 and 7 to user settings"). The numbered table is already visible — no need to re-list items in the confirmation prompt.

---

### Step 5: Apply to Settings

For each target settings file:

1. Read the current file (create `{ "permissions": { "allow": [] } }` if it doesn't exist).
2. Append new patterns to `permissions.allow`, avoiding duplicates.
3. Sort the allow array alphabetically.
4. Write back with 2-space indentation.
5. **Verify the write** — tell the user you're validating the JSON before running this command (e.g., "Verifying settings.json is valid JSON..."):
   ```bash
   node -e "JSON.parse(require('fs').readFileSync('<path>','utf8'))"
   ```
   If this fails, the file is invalid JSON. Immediately restore from the content read in step 1 and report the error. Do not continue to other files.

After successful verification, confirm:
```
Applied N rules to ~/.claude/settings.json
Applied M rules to .claude/settings.json

These commands will no longer trigger permission prompts.
```

If `.claude/settings.json` was modified and is tracked by git, mention that committing it would benefit teammates.

---

### Classification Reference (for understanding script behavior)

The script classifies commands into tiers:

**RED (never allowlisted with wildcards):**
- `rm *` — irreversible file deletion
- `sudo *` — privilege escalation
- `find -delete *`, `find -exec rm *` — destructive find
- `sed -i *` — in-place file edit
- `git push --force *`, `git push -f *` — force push overwrites remote history
- `git reset --hard *`, `git reset --merge *` — destroys uncommitted work
- `git clean -f *` — permanently deletes untracked files
- `git commit --no-verify *` — skips safety hooks
- `git config --system *` — system-wide config change
- `git filter-branch *`, `git filter-repo *` — rewrites repo history
- `git gc --aggressive *` — can remove recoverable objects
- `git reflog expire *` — removes recovery safety net
- `git stash clear *` — removes ALL stash entries permanently
- `git branch -D *` — force-deletes without merge check
- `git checkout -- *`, `git restore *` (without `--staged`) — discards working tree changes
- `npm publish *`, `yarn publish *`, `pnpm publish *` — permanent package publishing
- `npm unpublish *` — permanent package removal
- `cargo publish *`, `cargo yank *` — permanent crate operations
- `gem push *` — permanent gem publishing
- `poetry publish *`, `twine upload *` — permanent package publishing
- `gh release create *` — permanent release creation
- `| sh`, `| bash`, `| zsh` — pipe to shell execution
- `eval *` — arbitrary code execution
- `docker run --privileged *` — full host access
- `docker system prune *` (without `--dry-run`) — removes all unused data
- `docker volume rm *`, `docker volume prune *` — permanent data deletion
- `docker-compose down -v *`, `docker-compose down --volumes *` — removes volumes
- `docker-compose down --rmi *` — removes all images
- `docker rm -f *`, `docker rmi -f *` — force removes
- `reboot`, `shutdown`, `halt` — system operations
- `systemctl stop *`, `systemctl disable *`, `systemctl mask *` — stops system services
- `kill -9 *`, `pkill -9 *` — force kill
- `dd of=*` — raw disk write
- `mkfs *` — formats disk partition
- `chmod 777 *`, `chmod -R *`, `chown -R *` — permission/ownership changes
- `DROP DATABASE`, `DROP TABLE`, `DROP SCHEMA`, `TRUNCATE` — permanent data deletion
- `nc *`, `ncat *` — raw socket access
- `cat .env* |`, `printenv |` — credential exposure
- `pip uninstall *`, `apt remove *`, `brew uninstall *` — package removal
- `ast-grep --rewrite *` — in-place file modification

**GREEN (safe read-only):**
- Base commands: `ls`, `cat`, `head`, `tail`, `wc`, `file`, `tree`, `stat`, `du`, `diff`, `grep`, `rg`, `ag`, `ack`, `which`, `whoami`, `pwd`, `echo`, `printf`, `env`, `printenv`, `uname`, `hostname`, `jq`, `sort`, `uniq`, `tr`, `cut`, `less`, `more`, `man`, `type`, `realpath`, `dirname`, `basename`, `date`, `ps`, `top`, `htop`, `free`, `uptime`, `id`, `groups`, `lsof`, `open`, `xdg-open`
- `--version`, `--help` flags on any command
- `git status`, `git log`, `git diff`, `git show`, `git blame`, `git shortlog`, `git branch -l/-a/-v`, `git remote -v`, `git rev-parse`, `git describe`, `git reflog` (without expire), `git tag -l`, `git stash list/show`
- `npm/bun/pnpm/yarn run test/lint/build/check/typecheck`
- `npm/bun/pnpm/yarn test/lint/audit/outdated/list`
- `npx/bunx vitest/jest/eslint/prettier/tsc`
- `pytest`, `jest`, `cargo test`, `go test`, `rspec`, `bundle exec rspec`, `make test`, `rake rspec`
- `eslint`, `prettier`, `rubocop`, `black`, `flake8`, `cargo clippy/fmt`, `gofmt`, `golangci-lint`, `tsc --noEmit`, `mypy`, `pyright`
- `cargo build/check/doc/bench`, `go build/vet`
- `docker ps/images/logs/inspect/stats/system df`
- `docker-compose ps/logs/config`
- `systemctl status/list-*/show/is-*/cat`
- `journalctl`
- `pg_dump`, `mysqldump` (without `--clean`)
- Any command with `--dry-run`
- `sed -n *`, `sed -e *` (non-destructive sed)
- `ast-grep *` (without `--rewrite`)
- `find -name *`, `find -type *`, `find -path *`, `find -iname *`
- `gh pr/issue/run view/list/status/diff/checks`, `gh repo view/list/clone`, `gh api`

**YELLOW (modifies local state, recoverable — not auto-allowed):**
- `mkdir`, `touch`, `cp`, `mv`, `tee`, `curl`, `wget`, `ssh`, `scp`, `rsync`
- `python`, `python3`, `node`, `ruby`, `perl`, `make`, `just`, `awk`
- Most `git` write operations: `add`, `commit` (without `--no-verify`), `checkout` (without `--`), `switch`, `pull`, `push` (without force), `fetch`, `merge`, `rebase`, `stash`, `branch`, `cherry-pick`, `tag`, `clone`
- `git push --force-with-lease`
- `git restore --staged`
- `git gc` (without `--aggressive`)
- `npm/bun/pnpm/yarn install/add/remove/update`
- `npm/bun/pnpm run start/dev/serve`
- `pip install`, `bundle install`, `cargo add`, `go get`
- `docker build`, `docker run` (without `--privileged`), `docker stop/start`
- `docker-compose up/down` (without `-v`/`--volumes`/`--rmi`)
- `systemctl restart`
- `kill` (without `-9`)
- `rake`
- `gh pr/issue create/edit/comment/close/reopen/merge`, `gh run rerun/cancel/watch`

---

## Edge Cases

- **No project context** (running outside a project): Only offer user-level settings as write target.
- **Settings file doesn't exist**: Create it with `{ "permissions": { "allow": [] } }`. For `.claude/settings.json`, also create the `.claude/` directory if needed.
- **Deny rules**: If a deny rule already blocks a command, warn rather than adding an allow rule (deny takes precedence in Claude Code).
- **Empty results**: Allowlist is already well-optimized, or not enough session history yet — suggest re-running after more working sessions.

## Quality Gates

- [ ] Environment confirmed (Claude Code or other agent).
- [ ] Analysis scope confirmed with user.
- [ ] Script executed and output JSON parsed.
- [ ] Results presented in three parts (summary, recommendations, bottom line).
- [ ] User confirmation obtained before writing any files.
- [ ] Each settings file verified as valid JSON after writing.
- [ ] Restore-on-failure applied if JSON validation fails.
- [ ] Teammate commit reminder given if project settings were modified.

## Outputs

- Updated `~/.claude/settings.json` and/or `.claude/settings.json` with new `Bash(pattern)` allow rules.
- Summary of rules applied and resulting coverage improvement.

## Feeds Into

- Improved development workflow in Claude Code with fewer permission interruptions.
- Optionally committed `.claude/settings.json` to benefit the whole team.
