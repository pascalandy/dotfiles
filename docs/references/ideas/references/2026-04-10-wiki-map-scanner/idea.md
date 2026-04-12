Create a script within the wiki-map skill that scans from the root of any directory to find all existing wiki maps. The script should identify wiki maps by checking for INDEX.md files with the `kind/wiki` tag in their YAML frontmatter.

Context: This repository uses a specific convention to mark wiki maps.

Wiki Map Identification Rule:

A directory qualifies as a wiki map only when it meets all three conditions:
1. Contains a file named INDEX.md (case-sensitive)
2. The INDEX.md has YAML frontmatter with the tag `kind/wiki`
3. Contains a subdirectory named references/ (case-sensitive)

When I say "update all my wiki maps":

1. Search Phase: Find all directories matching the three criteria above
2. Action Phase: For each wiki map directory, trigger the wiki-map skill with the Lint sub-skill's FullSweep workflow to health-check and update the wiki

Specifically:
- Load skill wiki-map
- Route to the Lint operation (health check)
- Run the FullSweep workflow on each wiki map directory
- This checks for: contradictions, provenance gaps, INDEX drift, orphan pages, stale content, weak cross-references, and schema violations

Do NOT:
- Check for references/LOG.md existence before identifying
- Validate the full wiki-map schema before triggering the skill
- Require additional tags beyond kind/wiki
- Skip the skill trigger and try to manually update files

Example workflow:

User: "Please update all my wiki maps"

AI actions:
1. Search for all INDEX.md files with `kind/wiki` tag
2. Verify each has a `references/` subdirectory
3. For each match: trigger wiki-map skill → Lint → FullSweep workflow
4. Report results per wiki map
