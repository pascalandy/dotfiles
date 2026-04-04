# Basecamp → Markdown Export: Research & Architecture

## Overview

This document captures the full research on the Basecamp 3 API / CLI schema and proposes an architecture for exporting everything as structured markdown files with frontmatter-managed state.

**Source of truth**: `opensrc/repos/github.com/basecamp/basecamp-cli`  
**API docs**: https://github.com/basecamp/bc3-api  
**CLI coverage**: 100% of in-scope endpoints (155/155)

---

## 1. Basecamp Data Model

### The Core Concept: Recordings

Every piece of Basecamp content is a **recording** — todos, messages, comments, documents, uploads, schedule entries, cards, check-in answers. All recordings share:

```
id            int64     unique identifier
type          string    "Todo", "Message", "Vault", "Upload", "Document", etc.
status        string    "active" | "archived" | "trashed"
created_at    ISO 8601
updated_at    ISO 8601
visible_to_clients  bool
inherits_status     bool
creator       Person    {id, name, email, attachable_sgid, ...}
bucket        Project   {id, name, type: "Project"}
parent        Parent?   {id, title, type, url, app_url}
url           string    API URL
app_url       string    Web URL
bookmark_url  string
comments_count  int
boosts_count    int
```

### Resource Hierarchy

```
Account
└── Project (bucket)
    ├── Message Board (dock: "message_board")
    │   └── Message
    │       └── Comments
    ├── To-do Set (dock: "todoset") — exactly one per project
    │   └── To-do List
    │       ├── To-do List Group (optional grouping)
    │       └── Todo
    │           └── Comments
    ├── Docs & Files (dock: "vault")
    │   ├── Vault (subfolder, recursive)
    │   ├── Document (rich text)
    │   └── Upload (binary file)
    ├── Schedule (dock: "schedule")
    │   └── Schedule Entry
    ├── Chat / Campfire (dock: "chat")
    │   └── Chat Line
    ├── Card Table / Kanban (dock: "kanban_board")
    │   └── Column
    │       └── Card
    │           └── Step (checklist item)
    ├── Check-ins (dock: "questionnaire")
    │   └── Question
    │       └── Answer
    └── Email Forwards (dock: "inbox")
        └── Forward
            └── Reply
```

---

## 2. Full Field Schema Per Resource

### Project

```yaml
id: int64
name: string
description: string
status: active | archived | trashed
purpose: topic | (other)
bookmarked: bool
clients_enabled: bool
timesheet_enabled: bool
color: string | null
created_at: ISO 8601
updated_at: ISO 8601
url: string (API)
app_url: string (web)
dock:
  - id: int64
    name: message_board | todoset | vault | chat | schedule | questionnaire | kanban_board | inbox
    title: string
    enabled: bool
    position: int
    url: string
    app_url: string
```

### Todo

```yaml
id: int64
type: Todo
content: string          # title (plain text)
description: string      # HTML body / notes
completed: bool
status: active | archived | trashed
due_on: YYYY-MM-DD | null
starts_on: YYYY-MM-DD | null
position: int
assignees:
  - id: int64
    name: string
creator: Person
parent:
  id: int64
  title: string          # Todolist name
  type: Todolist
bucket:
  id: int64
  name: string
  type: Project
comments_count: int
created_at: ISO 8601
updated_at: ISO 8601
url: string
app_url: string
```

### Todolist

```yaml
id: int64
type: Todolist
name: string
description: string
status: active | archived | trashed
position: int
todos_remaining_count: int
completed_ratio: string   # e.g. "3/5"
creator: Person
parent:
  id: int64
  title: string           # Todoset name
  type: Todoset
bucket: Project ref
created_at: ISO 8601
updated_at: ISO 8601
```

### Message

```yaml
id: int64
type: Message
subject: string          # title
content: string          # HTML rich text
status: active | drafted | archived | trashed
pinned: bool
creator: Person
parent:
  id: int64
  title: Message Board
  type: Message::Board
bucket: Project ref
comments_count: int
boosts_count: int
created_at: ISO 8601
updated_at: ISO 8601
```

### Card

```yaml
id: int64
type: Card
title: string
content: string          # HTML body
description: string
due_on: YYYY-MM-DD | null
completed: bool
status: active | archived | trashed
position: int
assignees: Person[]
steps:
  - id: int64
    title: string
    completed: bool
    due_on: YYYY-MM-DD | null
    assignees: Person[]
    position: int
parent:
  id: int64
  title: string          # Column name
  type: CardTableColumn
bucket: Project ref
created_at: ISO 8601
updated_at: ISO 8601
```

### CardColumn

```yaml
id: int64
title: string
cards_count: int
on_hold:
  id: int64             # sub-column for "on hold" cards
```

### Schedule Entry

```yaml
id: int64
type: ScheduleEntry
summary: string          # title
description: string      # HTML
starts_at: ISO 8601
ends_at: ISO 8601
all_day: bool
notify: bool
participants: Person[]
creator: Person
parent:
  id: int64
  title: string
  type: Schedule
bucket: Project ref
created_at: ISO 8601
updated_at: ISO 8601
```

### Document

```yaml
id: int64
type: Document
title: string
content: string          # HTML rich text
status: active | drafted | archived | trashed
creator: Person
parent:
  id: int64
  title: string          # Vault / folder name
  type: Vault
bucket: Project ref
comments_count: int
created_at: ISO 8601
updated_at: ISO 8601
```

### Upload (File)

```yaml
id: int64
type: Upload
filename: string
byte_size: int64
content_type: string
download_url: string
description: string      # HTML
creator: Person
parent:
  id: int64
  type: Vault
bucket: Project ref
created_at: ISO 8601
updated_at: ISO 8601
```

### Check-in Question

```yaml
id: int64
type: Question
title: string
answers_count: int
schedule:
  frequency: every_day | every_week | every_other_week | every_month | on_certain_days
  days: [0-6]            # 0=Sun
  hour: int
  minute: int
creator: Person
parent:
  id: int64
  type: Questionnaire
bucket: Project ref
```

### Check-in Answer

```yaml
id: int64
type: Question::Answer
content: string          # HTML
group_on: YYYY-MM-DD
creator: Person
parent:
  id: int64
  title: string          # Question title
  type: Question
bucket: Project ref
created_at: ISO 8601
updated_at: ISO 8601
```

### Chat Line

```yaml
id: int64
type: Lines::Line
content: string          # HTML with @mentions
creator: Person
parent:
  id: int64
  title: string          # Campfire name
  type: Campfire
bucket: Project ref
created_at: ISO 8601
```

### Comment

```yaml
id: int64
type: Comment
content: string          # HTML
creator: Person
parent:
  id: int64
  type: string           # parent recording type
bucket: Project ref
created_at: ISO 8601
updated_at: ISO 8601
```

---

## 3. CLI Command Reference (Export-Relevant)

```bash
# Auth
basecamp auth login --scope read
basecamp auth status

# Discovery
basecamp projects list --json          # all projects + dock IDs
basecamp projects show <id> --json     # project detail + dock

# Todos
basecamp todosets show <id> --json     # get todoset from dock
basecamp todolists list --in <project> --json --all
basecamp todos list --in <project> --list <list_id> --json --all
basecamp todos list --in <project> --completed --json --all

# Messages
basecamp messages list --in <project> --json --all

# Cards
basecamp cards list --in <project> --json --all
basecamp cards columns --in <project> --json

# Schedule
basecamp schedule entries --in <project> --json --all

# Files & Docs
basecamp files list --in <project> --json    # tree: folders + docs + uploads
basecamp files documents list --in <project> --json --all
basecamp files uploads list --in <project> --json --all

# Check-ins
basecamp checkins questions --in <project> --json --all
basecamp checkins answers <question_id> --json --all

# Chat
basecamp chat messages --in <project> --json --all

# Comments (per recording)
basecamp comments <recording_id> --json --all

# People
basecamp people list --in <project> --json
basecamp me --json

# Search
basecamp search "query" --json
```

---

## 4. Demo Project / Getting Started

**Basecamp provides a "Basecamp HQ" sample project** that new accounts receive on sign-up. This includes:
- Sample messages in the message board
- A set of todo lists with pre-populated todos
- A few schedule entries
- Documents and file examples

**To explore live:**
```bash
# After auth login
basecamp projects list
# Look for "Basecamp HQ" or the demo project
basecamp projects show <demo_project_id>
```

**Alternative — create a minimal demo project:**
```bash
basecamp projects create "Export Demo" --description "Testing markdown export"
basecamp config set project_id <id>  # in your working repo

# Seed with content
basecamp todo "Design the export schema"
basecamp todo "Implement fetcher"
basecamp todo "Write tests"
basecamp message "Project kickoff" --draft
basecamp schedule create "Team sync" --starts-at "2026-04-07T10:00:00" --ends-at "2026-04-07T11:00:00"
```

---

## 5. Proposed Markdown Export Architecture

### File Structure

```
basecamp-export/
├── _meta/
│   ├── account.md          # account info
│   └── people.md           # people directory
└── projects/
    └── {project-slug}/
        ├── project.md      # project metadata + dock
        ├── messages/
        │   └── {message-slug}.md
        ├── todos/
        │   ├── {list-slug}/
        │   │   ├── _list.md         # todolist metadata
        │   │   └── {todo-slug}.md
        │   └── completed/
        │       └── {todo-slug}.md
        ├── cards/
        │   ├── {column-slug}/
        │   │   └── {card-slug}.md
        │   └── on-hold/
        │       └── {card-slug}.md
        ├── schedule/
        │   └── {date}-{slug}.md
        ├── docs/
        │   ├── {folder-slug}/
        │   │   └── {doc-slug}.md
        │   └── {doc-slug}.md
        ├── checkins/
        │   └── {question-slug}/
        │       └── {date}-{answer-slug}.md
        └── chat/
            └── {date}.md   # daily digest of chat lines
```

### Frontmatter Schema

Every exported file uses YAML frontmatter to capture full state:

```yaml
---
# Universal fields (all resources)
bc_id: 1069478887
bc_type: Todo
bc_project_id: 2085958494
bc_project_name: "My Project"
bc_url: "https://3.basecampapi.com/.../todos/1069478887.json"
bc_app_url: "https://3.basecamp.com/.../todos/1069478887"
status: active                # active | archived | trashed
created_at: "2026-02-21T04:11:00.818Z"
updated_at: "2026-02-21T04:11:00.818Z"
synced_at: "2026-04-04T12:00:00Z"  # when we last pulled from API
creator_id: 270913789
creator_name: "Jason Fried"

# Todo-specific
completed: false
due_on: "2026-04-15"
starts_on: null
assignees:
  - id: 270913789
    name: "Jason Fried"
parent_list_id: 1069478886
parent_list_name: "Launch"

# Message-specific
subject: "Celebrations!"
pinned: false
draft: false

# Card-specific
column_id: 1069478900
column_name: "In Progress"
on_hold: false
steps_total: 3
steps_completed: 1

# Schedule entry-specific
starts_at: "2026-04-07T10:00:00Z"
ends_at: "2026-04-07T11:00:00Z"
all_day: false
participants:
  - id: 270913789
    name: "Jason Fried"

# Document-specific
title: "Welcome to the project"
vault_id: 1069478872
vault_name: "Docs & Files"

# Check-in specific
question_id: 1069478910
question_title: "What did you work on today?"
group_on: "2026-04-04"
---
```

### Document Body

The markdown body contains the rich-text content, converted from Basecamp's HTML. Comments follow as a section at the bottom:

```markdown
---
[frontmatter as above]
---

# Todo Title / Message Subject / Card Title

Full content body here (converted from HTML).

---

## Comments (2)

### Jason Fried — 2026-02-22T10:00:00Z

Comment body here.

### David Heinemeier Hansson — 2026-02-22T11:00:00Z

Reply here.
```

---

## 6. State Management via Frontmatter

The frontmatter fields enable bidirectional sync logic:

| Field | Purpose |
|-------|---------|
| `bc_id` | Primary key for update/delete matching |
| `synced_at` | Detect stale records (re-fetch if older than threshold) |
| `status` | Soft deletes: `trashed` files can be hidden from views |
| `updated_at` | Diff against local `updated_at` to detect upstream changes |
| `completed` | Track todo/card completion without re-fetching |

### Sync Lifecycle

```
1. PULL: basecamp projects list --json
   → Write/update projects/{slug}/project.md

2. PULL: basecamp todos list --in PROJECT --all --json
   → For each todo: write/update projects/{slug}/todos/{list}/{todo}.md
   → Check updated_at: if changed since synced_at → refresh full record

3. PUSH: Read local .md, compare frontmatter to API
   → If bc_id exists and local differs → call update API
   → If no bc_id → call create API → write new bc_id to frontmatter

4. ARCHIVE: If status=trashed in API
   → Move file to todos/archive/ and update frontmatter

5. COMPLETE: If completed=true changed locally
   → Call basecamp done {bc_id}
   → Update frontmatter synced_at
```

---

## 7. Implementation Phases

### Phase 1: Read-only exporter (MVP)

- Auth flow via `basecamp auth login`
- Fetch all projects → write project files
- Fetch todos (all lists, active + completed)
- Fetch messages (active)
- Output: flat `--json` piped through script

**Tool**: Shell script or Go CLI wrapping `basecamp` CLI commands

### Phase 2: Full export

- Cards / Kanban columns
- Schedule entries
- Documents and file metadata (not binary downloads)
- Check-in questions + answers
- Comments on all resources

### Phase 3: Bidirectional sync

- Detect frontmatter changes → push to API
- Incremental sync: only refresh changed records
- Conflict resolution: API wins (with local backup)

### Phase 4: Obsidian integration

- WikiLinks between resources: `[[todos/launch/design-it]]`
- Tags from Basecamp types: `#todo`, `#message`, `#card`
- Dataview queries on frontmatter for kanban views
- Calendar view for schedule entries

---

## 8. Key CLI Patterns for Export

```bash
# JSON envelope shape — use --quiet for data-only
basecamp projects list --quiet | jq '.[].id'

# Breadcrumbs give you next commands
basecamp projects show 12345 --json | jq '.breadcrumbs[].cmd'

# Flat routes work directly
basecamp todos list --list <todolist_id> --json --all

# The dock maps project tools to their container IDs
basecamp projects show 12345 --json | jq '.data.dock[] | select(.name=="todoset")'

# Get ALL todos across all projects (via assignments)
basecamp assignments list --json

# Search for content
basecamp search "keyword" --json
```

---

## 9. Open Questions

1. **Binary files**: Should uploads be downloaded (large) or just linked by URL?
2. **HTML → Markdown conversion**: Need an HTML-to-MD library. `@bc-attachment` tags need special handling.
3. **@mentions**: Convert `[@Name](mention:SGID)` to person's name or a WikiLink?
4. **Incremental sync**: Use `updated_at` or webhooks for change detection?
5. **Demo project**: Confirm what Basecamp provides on trial sign-up; may need to create seed data.
6. **Rich text attachments**: `<bc-attachment>` inline images/files need a strategy (download + embed vs link).
7. **Recurring schedule entries**: Multiple occurrences — one file per occurrence or one file with recurrence rule?

---

## 10. Next Steps

1. **Authenticate**: `basecamp auth login` against a real or trial Basecamp account
2. **Explore live data**: `basecamp projects list` to find a demo project (look for "Basecamp HQ")
3. **Run commands** listed in section 3 against the demo project to validate schema
4. **Build Phase 1 exporter**: script that walks the hierarchy and writes markdown files
5. **Design frontmatter validator**: ensure all required fields present + valid
6. **Test round-trip**: export → edit frontmatter → push back via CLI
