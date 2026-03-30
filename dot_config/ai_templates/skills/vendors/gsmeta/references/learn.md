# Learn

> Manage project learnings captured by gstack across sessions: review, search, prune stale entries, export to documentation, and manually add new entries.

## When to Use

- User asks "what have we learned", "show learnings", "what did we figure out before"
- User wonders "didn't we fix this before?" — search learnings first
- After a bug is fixed or pattern discovered — suggest adding it
- Periodically to prune stale learnings after refactors or file moves
- Before starting a new task — search for relevant past patterns
- Proactively after any /review, /ship, /investigate, or /qa run that surfaces new patterns

**Hard gate:** this skill manages learnings only. Do not implement code changes.

## Inputs

- The project slug (auto-detected from repo)
- Learnings database at `~/.gstack/projects/{slug}/learnings.jsonl`
- Optional: search query, specific learning entry to update

## Methodology

### Detect command

Parse user input to determine mode:

| Input | Mode |
|-------|------|
| `/learn` (no args) | Show recent |
| `/learn search <query>` | Search |
| `/learn prune` | Prune stale/contradictory entries |
| `/learn export` | Export as markdown |
| `/learn stats` | Show statistics |
| `/learn add` | Manual add |

---

### Show recent (default)

Run `gstack-learnings-search --limit 20`. Present grouped by type (patterns, pitfalls, preferences, architecture). If no learnings exist yet, tell the user which skills will start populating them (/review, /ship, /investigate, /qa).

---

### Search

Run `gstack-learnings-search --query "USER_QUERY" --limit 20`. Present results clearly with key, insight, confidence score, and source skill.

---

### Prune

1. Run `gstack-learnings-search --limit 100` to get all entries
2. For each learning with a `files` field: check if those files still exist in the repo. Flag any that reference deleted files: "STALE: [key] references deleted file [path]"
3. For each learning key: look for contradicting entries with opposite insights. Flag: "CONFLICT: [key] has contradicting entries — [insight A] vs [insight B]"
4. For each flagged entry, ask the user:
   - A) Remove this learning
   - B) Keep it
   - C) Update it (tell me what to change)
5. For removals: read `learnings.jsonl`, remove the matching line, write back
6. For updates: append a new entry with corrected insight (append-only — latest entry wins)

---

### Export

1. Run `gstack-learnings-search --limit 50`
2. Format as markdown, grouped by type:

```markdown
## Project Learnings

### Patterns
- **[key]**: [insight] (confidence: N/10)

### Pitfalls
- **[key]**: [insight] (confidence: N/10)

### Preferences
- **[key]**: [insight]

### Architecture
- **[key]**: [insight] (confidence: N/10)
```

3. Ask the user: append to CLAUDE.md or save as a separate file?

---

### Stats

Compute from `learnings.jsonl`:
- Total raw entries
- Unique entries after deduplication (latest entry per key wins)
- Count by type (pattern/pitfall/preference/architecture/tool)
- Count by source skill
- Average confidence score

Present as a table.

---

### Manual add

Gather from the user:
1. Type: pattern / pitfall / preference / architecture / tool
2. Key: 2-5 words, kebab-case
3. Insight: one sentence
4. Confidence: 1-10
5. Related files: optional

Then append to the learnings file:
```json
{"skill":"learn","type":"TYPE","key":"KEY","insight":"INSIGHT","confidence":N,"source":"user-stated","files":["FILE1"]}
```

---

### Deduplication rule

Learnings are append-only. The **latest entry** for a given key wins. When displaying or exporting, deduplicate by key before showing counts and insights.

## Quality Gates

- [ ] Correct mode detected from user input
- [ ] Learnings presented grouped by type, not as raw JSONL
- [ ] Prune: all stale file references and conflicts surfaced, user confirmed each decision
- [ ] Export: properly grouped markdown, user directed to CLAUDE.md or separate file
- [ ] Manual add: key is kebab-case, insight is one sentence, confidence is 1-10
- [ ] No code changes made (hard gate)

## Outputs

- Formatted learning summary (show recent / search results)
- Pruned learnings.jsonl with stale/conflicting entries removed
- Exported markdown block for CLAUDE.md or docs
- Stats table (total, unique, by type, by source, avg confidence)
- New entry appended to learnings.jsonl (manual add)

## Feeds Into

- >investigate (search learnings before starting a debug session)
- >review (surfaces existing patterns before code review)
- >ship (confirm no known pitfalls apply to current change)

## Harness Notes

Learnings database lives at `~/.gstack/projects/{slug}/learnings.jsonl`. The slug is derived from the current git repo. Stats computation uses `bun` for JSONL parsing. The file is append-only — never overwrite in place except for pruning, which rewrites the file after explicit user confirmation per entry.
