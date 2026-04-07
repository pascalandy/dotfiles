# Update This Skill

Triggered when the user says something like "skill headless-codex, check if we need to update".


To keep this skill current with the latest documentation, check the official docs using `npx nia-docs`.

## Configuration

Set the documentation URL (source of truth):

```bash
DOC_URL="https://developers.openai.com/codex/cli/reference"
```

## Quick Reference

```bash
# Search for a topic
npx nia-docs "$DOC_URL" -c "grep -rl 'topic' ."

# Read a specific page
npx nia-docs "$DOC_URL" -c "cat page-name.md"

# Find all markdown files
npx nia-docs "$DOC_URL" -c "find . -name '*.md'"

# List top-level structure
npx nia-docs "$DOC_URL" -c "tree -L 1"

# Browse interactively
npx nia-docs "$DOC_URL"
```

## Usage Notes

- The shell starts in the docs root
- Use `.` for relative paths
- All standard Unix tools work: `grep`, `find`, `cat`, `tree`, `ls`, `head`, `tail`, `wc`

## What to Check For

When updating this skill, verify:

1. **New flags or options** — check the main CLI/command reference
2. **New subcommands** — look for additions to the command tree
3. **Output format changes** — verify JSON/text output behavior
4. **Configuration changes** — new env vars or config file options
5. **Examples and use cases** — new patterns in the docs

## Update Checklist

- [ ] Run `npx nia-docs "$DOC_URL" -c "cat ./reference.md"` (or main reference file) and compare flags/options
- [ ] Verify all referenced items match the current implementation
- [ ] Check for new examples or use cases in the docs
- [ ] Update the Gotchas section if new pitfalls are discovered
- [ ] Test any new commands before documenting them
