# Onboarding Document Generator

> Crawl a repository and generate `ONBOARDING.md` — a document that helps new contributors understand the codebase without requiring the creator to explain it.

## When to Use

- User asks to "create onboarding docs", "generate ONBOARDING.md", "document this project for new developers", "write onboarding documentation", "prepare this repo for a new contributor", "refresh the onboarding doc", or "update ONBOARDING.md".
- A codebase lacks onboarding documentation and the user wants to generate one.
- A new team member needs to be onboarded and a written artifact is required.

This skill always regenerates the document from scratch. It does not read or diff a previous version. If `ONBOARDING.md` already exists, it is overwritten.

## Inputs

- Repository root accessible for reading.
- `scripts/inventory.mjs` script (bundled) for structural analysis.

## Methodology

### Core Principles

1. **Write for humans first** — Clear prose a new developer can read and understand. Agent utility is a side effect of good human writing, not a separate goal.
2. **Show, don't just tell** — Use ASCII diagrams for architecture and flow, markdown tables for structured information, backtick formatting for all file paths, commands, and code references.
3. **Six sections, each earning its place** — Every section answers a question a new contributor will ask in their first hour. No speculative sections. Section 2 may be skipped for pure infrastructure with no consuming audience, producing five sections.
4. **State what you can observe, not what you must infer** — Do not fabricate design rationale or assess fragility. If the code doesn't reveal why a decision was made, don't guess.
5. **Never include secrets** — The document is committed to the repository. Never include API keys, tokens, passwords, connection strings with credentials, or any other secret values. Reference environment variable *names* (`STRIPE_SECRET_KEY`), never their *values*. If a `.env` file contains actual secrets, extract only the variable names.
6. **Link, don't duplicate** — When existing documentation covers a topic well, link to it inline rather than re-explaining.

---

### Phase 1: Gather Inventory

Run the bundled inventory script to get a structural map of the repository without reading every file:

```bash
node scripts/inventory.mjs --root .
```

Parse the JSON output. This provides:
- Project name, languages, frameworks, package manager, test framework.
- Directory structure (top-level + one level into source directories).
- Entry points per detected ecosystem.
- Available scripts/commands.
- Existing documentation files (with first-heading titles for triage).
- Test infrastructure.
- Infrastructure and external dependencies (env files, docker services, detected integrations).
- Monorepo structure (if applicable).

**If the script fails or returns an error field, report the issue to the user and stop.** Do not attempt to write `ONBOARDING.md` from incomplete data.

---

### Phase 2: Read Key Files

Guided by the inventory, read files essential for understanding the codebase. Use the native file-read mechanism (not shell commands).

**What to read and why:**

Read files in parallel batches where there are no dependencies between them. For example, batch `README.md`, entry points, and `AGENTS.md`/`CLAUDE.md` together since none depend on each other's content.

Only read files whose content is needed to write the six sections with concrete, specific detail. The inventory already provides structure, languages, frameworks, scripts, and entry-point paths — don't re-read files just to confirm what the inventory already says. Different repos need different amounts of reading; a small CLI tool might need 4 files, a complex monorepo might need 20. Let the sections drive what you read, not an arbitrary count.

**Priority order:**

1. **`README.md`** (if exists) — for project purpose and setup instructions.
2. **Primary entry points** — files listed in `entryPoints` from the inventory. These reveal what the application does when it starts.
3. **Route/controller files** — look for `routes/`, `app/controllers/`, `src/routes/`, `src/api/`, or similar directories from the inventory structure.
4. **Configuration files that reveal architecture and external dependencies** — `docker-compose.yml`, `.env.example`, `.env.sample`, database config, `next.config.*`, `vite.config.*`, or similar. Only read these if they appear in the inventory. **Never read `.env` itself** — only `.env.example` or `.env.sample` templates. Extract variable names only, never values.
5. **`AGENTS.md` or `CLAUDE.md`** (if exists) — for project conventions and patterns already documented.
6. **Discovered documentation** — the inventory's `docs` list includes each file's title (first heading). Use those titles to decide which docs are relevant without reading them first. Only read the full content of docs whose titles indicate direct relevance. Skip dated brainstorm/plan files unless the focus hint specifically calls for them.

Do not read files speculatively. Every file read should be justified by the inventory output and traceable to a section that needs it.

---

### Phase 3: Write ONBOARDING.md

Synthesize the inventory data and key file contents into the six sections below. Write the file to the repo root.

**Title:** Use `# {Project Name} Onboarding Guide` as the document heading. Derive the project name from the inventory. Do not use the filename as a heading.

**Insert a horizontal rule (`---`) between each `##` section.** These documents are dense and benefit from strong visual breaks.

**Width constraint for code blocks: 80 columns max.** Markdown code blocks render with `white-space: pre` and never wrap. Apply these rules inside all ``` fences:
- **ASCII architecture diagrams**: Stack boxes vertically. Never place more than 2 boxes on the same horizontal line; keep each box label under 20 characters. This caps diagrams at ~60 chars wide.
- **Flow diagrams**: Keep file path + annotation under 80 chars. If a description is too long, move it to the next line or shorten it.
- **Directory trees**: Keep inline `# comments` under 30 characters. Prefer brief role descriptions over exhaustive lists.

#### Writing Style

The document should read like a knowledgeable teammate explaining the project over coffee, not like generated documentation.

**Voice and tone:**
- Write in second person ("you") — speak directly to the new contributor.
- Use active voice and present tense: "The router dispatches requests to handlers" not "Requests are dispatched by the router."
- Be direct. Lead sentences with what matters: "Run `bun dev` to start the server" not "In order to start the development server, you will need to run the following command."
- Match the formality of the codebase. A scrappy prototype gets casual prose; an enterprise system gets more precise language.

**Clarity:**
- Every sentence should teach the reader something or tell them what to do. Cut any sentence that doesn't.
- Prefer concrete over abstract: "`src/services/billing.ts` charges the customer's card" not "The billing module handles payment-related business logic."
- When introducing a term, define it immediately in context.
- Use the simplest word that's accurate. "Use" not "utilize." "Start" not "initialize." "Send" not "transmit."

**What to avoid:**
- Filler: "It's important to note that", "As mentioned above", "In this section we will"
- Vague summarization: "This module handles various aspects of..."
- Hedge words: "This essentially serves as", "This is basically"
- Superlatives and marketing language: "robust", "powerful", "comprehensive", "seamless"
- Meta-commentary: "This document aims to..."

---

#### Section 1: What Is This?

Answer: What does this project do, who is it for, and what problem does it solve?

Draw from `README.md`, manifest descriptions (e.g., `package.json` description field), and what the entry points reveal about the application's purpose.

If the project's purpose cannot be clearly determined from the code, state that plainly: "This project's purpose is not documented. Based on the code structure, it appears to be..."

Keep to 1–3 paragraphs.

---

#### Section 2: How It's Used

Answer: What does it look like to be on the consuming side of this project?

Before a contributor can reason about architecture, they need to understand what the project *does* from the outside. Title this section based on who consumes the project:

- **End-user product** (web app, mobile app, consumer tool) — Title: **"User Experience"**. Describe what the user sees and the primary workflows (e.g., "sign up, create a project, invite collaborators, see real-time updates").
- **Developer tool** (SDK, library, dev CLI, framework) — Title: **"Developer Experience"**. Describe how a developer consumes the tool: installation, a minimal usage example, the 2–3 most common commands or patterns. This is distinct from Section 6 (Developer Guide), which covers *contributing to* this codebase — this section covers *using* what it produces.
- **Both** (platform with consumer product AND developer API/SDK) — Title: **"User and Developer Experience"**. Cover both, starting with the end-user experience.

Keep to 1–3 paragraphs or a short flow per audience. If comprehensive docs exist, link to them and summarize key workflows in a sentence each.

**Skip this section only** for codebases with no consuming audience (pure infrastructure, internal deployment tooling with no direct interaction).

---

#### Section 3: How Is It Organized?

Answer: What is the architecture, what are the key modules, how do they connect, and what does the system depend on externally?

**System architecture diagrams** — Two kinds help new contributors. Use one or both based on complexity:

1. **Architecture diagram** — Components, connections, protocols/transports. Label edges with interaction types (HTTP, WebSocket, bridge, queue, etc.). Start with user-facing surfaces at top, internal plumbing in middle, data stores and external services at bottom.

2. **User interaction flow** — The logical journey a user takes through the product. Not about infrastructure — about what happens from the user's perspective.

**When to use one vs. both:**
- Straightforward systems (single web app, CLI tool, simple API): one diagram is enough — the request path *is* the user flow.
- Multi-surface products (native app + web + API, or multiple distinct user types): include both. The architecture diagram shows how pieces are wired; the user flow shows the logical product experience across those pieces.

Use vertical stacking to keep diagrams under 80 columns.

**Architecture diagram example:**
```
       User / Browser
            |
            |  HTTP / WebSocket
            v
+------------------+    bridge    +------------------+
| Browser Client   |<----------->| Native macOS App |
| (Vite bundle)    |             | (Swift/WKWebView)|
+--------+---------+             +--------+---------+
         |                                |
         |  WebSocket                     |  bridge
         v                               v
+------------------------------------------+
|            Express Server                |
|  routes -> services -> models            |
+--------------------+---------------------+
                     |
                     |  SQL / Yjs sync
                     v
              +--------------+
              | SQLite + Yjs |
              +--------------+
```

**User interaction flow example (same system, different lens):**
```
User opens app
  |
  v
Writes/edits document
  (Milkdown editor)
  |
  v
Changes sync in real-time
  (Yjs CRDT)
  |                \
  v                 v
Document persists   Other connected
  to SQLite         clients see edits
  |
  v
User shares doc
  -> generates link
  |
  v
Recipient opens
  in browser client
```

Skip both diagrams for simple projects (single-purpose libraries, CLI tools) where the directory tree already tells the whole story.

**Internal structure** — Include an ASCII directory tree:
```
project-name/
  src/
    routes/       # HTTP route handlers
    services/     # Business logic
    models/       # Data layer
  tests/          # Test suite
  config/         # Environment and app config
```

Annotate directories with a brief comment. Only include directories that matter — skip build artifacts, config files, and boilerplate.

When modules have clear responsibilities, present them in a table:
```
| Module          | Responsibility                        |
|-----------------|---------------------------------------|
| `src/routes/`   | HTTP request handling and routing     |
| `src/services/` | Core business logic                   |
| `src/models/`   | Database models and queries           |
```

Describe how modules connect — what calls what, where data flows.

**External dependencies and integrations** — Surface everything the system talks to outside its own codebase. Look for signals in: `docker-compose.yml`, env variable references, import statements for client libraries, inventory-detected frameworks. Present as a table when there are multiple:
```
| Dependency | What it's used for    | Configured via       |
|------------|----------------------|----------------------|
| PostgreSQL | Primary data store   | `DATABASE_URL`       |
| Redis      | Session cache        | `REDIS_URL`          |
| Stripe API | Payment processing   | `STRIPE_SECRET_KEY`  |
| S3         | File uploads         | `AWS_*` env vars     |
```

If no external dependencies are detected, state: "This project appears self-contained with no external service dependencies."

---

#### Section 4: Key Concepts and Abstractions

Answer: What vocabulary and patterns does someone need to understand to talk about this codebase?

Cover two things:

**Domain terms** — Project-specific vocabulary: entity names, API resource names, database tables, configuration concepts, and jargon a new reader would not immediately recognize.

**Architectural abstractions** — Structural patterns that shape how code is organized and how a contributor should think about making changes. These are especially important in codebases where patterns may have been introduced by AI or adopted from templates without documentation.

Examples:
- "Business logic lives in the service layer (`src/services/`), not in route handlers"
- "Authentication runs through middleware in `src/middleware/auth.ts` before every protected route"
- "Database access uses the repository pattern — each model has a corresponding repository class"
- "Background jobs are defined in `src/jobs/` and dispatched through a Redis-backed queue"

Present both domain terms and abstractions in a single table:
```
| Concept          | What it means in this codebase                    |
|------------------|---------------------------------------------------|
| `Widget`         | The primary entity users create and manage        |
| `Pipeline`       | A sequence of processing steps on incoming data   |
| Service layer    | Business logic in `src/services/`, not handlers   |
| Middleware chain | Requests flow through `src/middleware/` first     |
```

Aim for 5–15 entries. Include only concepts that would confuse a new reader or that represent non-obvious architectural decisions. Skip universally understood terms.

---

#### Section 5: Primary Flows

Answer: What happens when the main things this app does actually happen?

Trace one flow per distinct surface or user type. A "surface" is a meaningfully different entry path into the system — a native app, a web UI, an API consumer, a CLI user. Each flow should reveal parts of the architecture that previous flows didn't cover. Stop when the next flow would mostly retrace files already shown.

- Simple library or CLI: one flow.
- Full-stack app with web UI and API: two flows.
- Product with native + web + agent surfaces: three flows.

Let the architecture drive the count, not an arbitrary number.

Include an ASCII flow diagram for the most important flow:
```
User Request
  |
  v
src/routes/widgets.ts
  validates input, extracts params
  |
  v
src/services/widget.ts
  applies business rules, calls DB
  |
  v
src/models/widget.ts
  persists to PostgreSQL
  |
  v
Response (201 Created)
```

At each step, reference the specific file path. Keep file path + annotation under 80 characters — put the annotation on the next line if needed.

Additional flows can use a numbered list instead of a full diagram if the first diagram already establishes the structural pattern.

---

#### Section 6: Developer Guide

Answer: How do I set up the project, run it, and make common changes?

Cover these areas:

1. **Setup** — Prerequisites, install steps, environment config. Draw from README and inventory scripts. Format commands in code blocks:
   ```
   bun install
   cp .env.example .env
   bun dev
   ```

2. **Running and testing** — How to start the dev server, run tests, lint. Use the inventory's detected scripts.

3. **Common change patterns** — Where to go for the 2–3 most common types of changes:
   - "To add a new API endpoint, create a route handler in `src/routes/` and register it in `src/routes/index.ts`"
   - "To add a new database model, create a file in `src/models/` and run `bun migrate`"

4. **Key files to start with** (for complex projects) — A table mapping areas of the codebase to specific entry-point files with a brief "why start here" note:
   ```
   | Area          | File                      | Why                          |
   |---------------|---------------------------|------------------------------|
   | Editor core   | `src/editor/index.ts`     | All editor wiring            |
   | Data model    | `src/formats/marks.ts`    | The annotation system        |
   | Server entry  | `server/index.ts`         | Express setup and routes     |
   ```
   Skip for projects with fewer than ~10 source files.

5. **Practical tips** (for complex projects) — Surface areas that are particularly large, complex, or have non-obvious gotchas:
   - "The editor module is ~450KB. Most behavior is wired through plugins in `src/editor/plugins/` — understand the plugin architecture before making editor changes."
   - "The collab subsystem has many guards and epoch checks. Read the test names to understand what invariants are maintained."
   
   Skip for simple projects small enough to hold in your head.

---

#### Inline Documentation Links

While writing each section, check whether any file from the inventory's `docs` list is directly relevant. If so, link inline:

> Authentication uses token-based middleware — see [`docs/solutions/auth-pattern.md`](docs/solutions/auth-pattern.md) for the full pattern.

Do not create a separate references or further-reading section. If no relevant docs exist, the section stands alone.

---

### Phase 4: Quality Check

Before writing the file, verify:

- [ ] Every section answers its question without padding or filler
- [ ] No secrets, API keys, tokens, passwords, or credential values anywhere in the document
- [ ] No fabricated design rationale ("we chose X because...")
- [ ] No fragility or risk assessments
- [ ] File paths referenced correspond to real files from the inventory
- [ ] All file names, paths, commands, code references, and technical terms use backtick formatting
- [ ] Document title uses "# {Project Name} Onboarding Guide" format, not the filename
- [ ] System-level architecture diagram included for multi-surface projects (skipped for simple libraries/CLIs)
- [ ] All code block content (diagrams, trees, flow traces) fits within 80 columns
- [ ] ASCII diagrams are present in the architecture and/or primary flow sections
- [ ] One flow per distinct surface or user type (architecture drives the count)
- [ ] External dependencies and integrations are surfaced in the architecture section (or explicitly noted as absent)
- [ ] Tables are used for module responsibilities, domain terms/abstractions, and external dependencies
- [ ] Markdown styling is consistent throughout (headers, bold, code blocks, tables)
- [ ] Existing docs are linked inline only where directly relevant
- [ ] Writing is direct and concrete — no filler, no hedge words, no meta-commentary
- [ ] Tone matches the codebase (casual for scrappy projects, precise for enterprise)
- [ ] "How It's Used" section present with title adapted to audience (User Experience / Developer Experience / both), skipped only for pure infrastructure
- [ ] Architecture diagram has labeled edges (protocols/transports) and includes a user interaction flow diagram when the system has multiple surfaces or user types

---

### Phase 5: Present Result

After writing, inform the user that `ONBOARDING.md` has been generated. Offer next steps — present numbered options:

1. Open the file for review
2. Share to Proof
3. Done

Based on selection:

**Open for review** → Open `ONBOARDING.md` using the current platform's file-open or editor mechanism.

**Share to Proof** → Upload the document:

```bash
CONTENT=$(cat ONBOARDING.md)
TITLE="Onboarding: <project name from inventory>"
RESPONSE=$(curl -s -X POST https://www.proofeditor.ai/share/markdown \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg title "$TITLE" \
    --arg markdown "$CONTENT" \
    --arg by "ai:compound" \
    '{title: $title, markdown: $markdown, by: $by}')")
PROOF_URL=$(echo "$RESPONSE" | jq -r '.tokenUrl')
```

Display `View & collaborate in Proof: <PROOF_URL>` if successful, then return to the options.

**Done** → No further action.

## Quality Gates

All items in the Phase 4 checklist above must pass before writing the file.

## Outputs

- `ONBOARDING.md` at the repository root, covering all six sections (or five for pure infrastructure).
- Optionally a Proof share URL for collaborative review.

## Feeds Into

- `proof` — for sharing the generated document for team review.
- `ce:compound` — for capturing patterns discovered during the inventory.
