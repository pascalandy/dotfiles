---
description: add_memory into pg-memory memories table
---

# STEPS TO FOLLOW

### Step 1: Post-mortem

See this as a mini post-mortem.

Please reverse engineer our conversation by keeping in mind this question : 
What is worth remembering if the future ?

MEMORY TYPE: What type of memory is this?
1) observation - Something noticed (user preference, pattern) (recommended)
2) decision - A choice made with rationale
3) learning - A lesson learned
4) error - Something that went wrong
5) action - Something you did
6) thought - Internal reasoning worth preserving
7) project_status - Status snapshot
8) command_summary - Slash command execution summary

- what did we learn
- what went wrong
- what what did we discovered
- the fix
- feedback for the agent 
- feedback for the user 

There might more many type from our conversation

thank you for be so diligent

P.S. If there's nothing, don't be shy to say there's nothing

### Step 2: Gather context silently

Collect without asking:

| Field         | Command                                                                       |
| ------------- | ----------------------------------------------------------------------------- |
| `provider_id` | Current LLM provider (e.g., `anthropic`)                                      |
| `model_id`    | Current LLM model (e.g., `claude-opus-4-5`)                                   |
| `repo_name`   | `basename $(git rev-parse --show-toplevel 2>/dev/null)` or NULL               |
| `repo_path`   | `realpath --relative-to="$HOME" $(git rev-parse --show-toplevel)` or NULL     |
| `git_branch`  | `git branch --show-current 2>/dev/null` or NULL                               |
| `git_commit`  | `git rev-parse --short HEAD 2>/dev/null` or NULL                              |

### Step 3: Load skill

Load: `pg-memory`

### Step 4: Extract and package memories

From the conversation context, identify memories worth storing. For each memory:

1. **Infer content** - Extract the key insight, decision, or observation
2. **Infer type** - Pick the most appropriate type
3. **Infer importance** - Estimate 0-7 based on impact
4. **Infer tags** - Generate 2-5 relevant lowercase tags (hyphens for multi-word)

### Step 5: Present memories for approval

Display each memory in a compact numbered format:

```
Ready to add 3 memories:

1. [observation] importance:5 tags:[coding, preference]
   "User prefers tabs over spaces for indentation .."

2. [decision] importance:6 tags:[architecture, database]
   "Chose PostgreSQL over SQLite for JSONB support .."

3. [learning] importance:4 tags:[git, workflow]
   "Always run tests before committing to main .."

---
Commands:
  y        → approve all
  1 y      → approve #1 only
  1 2 y    → approve #1 and #2
  1 n      → reject #1
  3 +tag   → add tag to #3 (e.g., "3 +best-practice")
  3 -tag   → remove tag from #3
  3 type:X → change type (e.g., "3 type:decision")
  3 imp:X  → change importance (e.g., "3 imp:6")
  edit 2   → edit content of #2
  n        → cancel all
```

### Step 6: Process user commands

Parse user input and apply modifications:

- `y` or `go` → approve all memories
- `1 y` → approve only memory #1
- `1 2 3 y` → approve memories 1, 2, 3
- `1 n` → reject memory #1 (remove from list)
- `3 +tag-name` → add tag to memory #3
- `3 -tag-name` → remove tag from memory #3
- `3 type:learning` → change type of #3
- `3 imp:6` → change importance of #3
- `edit 2` → prompt user for new content for #2
- `n` or `cancel` → abort all

After modifications, re-display updated list if changes were made.

### Step 7: Execute approved INSERTs

For each approved memory, run:

```sql
INSERT INTO memories (
  user_id, provider_id, model_id,
  repo_name, repo_path, git_branch, git_commit,
  type, content, importance, tags
)
VALUES (
  'pascalandy',
  '{provider_id}',
  '{model_id}',
  '{repo_name}',
  '{repo_path}',
  '{git_branch}',
  '{git_commit}',
  '{type}',
  $content${content}$content$,
  {importance},
  '{tags_json}'
)
RETURNING id, type, importance, created_at;
```

### Step 8: Report results

Show compact summary:

```
Added 2 memories:

1. ID: 019400a0-... | observation | imp:5 | [coding, preference]
   "User prefers tabs over spaces"

2. ID: 019400a1-... | decision | imp:6 | [architecture, database]
   "Chose PostgreSQL over SQLite for JSONB support"

Skipped: 1 (rejected by user)
```

---

## MEMORY TYPES

| Type              | Use for                             |
| ----------------- | ----------------------------------- |
| `observation`     | User preference, pattern noticed    |
| `decision`        | Choice made with rationale          |
| `learning`        | Lesson learned                      |
| `error`           | Something that went wrong           |
| `action`          | Something the agent did             |
| `thought`         | Internal reasoning worth preserving |
| `project_status`  | Status snapshot                     |
| `command_summary` | Slash command execution summary     |

## IMPORTANCE SCALE

| Score | Meaning                                    |
| ----- | ------------------------------------------ |
| 7     | Perfect, flawless                          |
| 6     | Excellent, life-changing                   |
| 5     | Good, would recommend                      |
| 4     | Fine, neutral                              |
| 3     | Meh, wouldn't recommend                    |
| 2     | Disappointing                              |
| 1     | Avoid                                      |
| 0     | Unrated                                    |

---

## CRITICAL RULES

1. **AI pre-packages** - Extract memories from context, don't ask what to remember
2. **Compact display** - One line per memory, details inline
3. **Batch approval** - Support approving multiple with single command
4. **Inline edits** - `+tag`, `-tag`, `type:X`, `imp:X` modify without re-prompting
5. **Dollar quoting** - Always use `$content$...$content$` for content field
6. **Lowercase tags** - Hyphens for multi-word, no special chars
7. **Silent context** - Gather git/model info without asking

---

## Finally

- There might one or many types of memories from our conversation.
- P.S. If there's nothing, don't be shy to say there's nothing
- thank you for be so diligent!