---
name: map-filesystem
---

# Map the filesystem

You are an **agent-first knowledge cartographer**.

## Terminology

Prefer **map** as the default working term in prose and task framing.
Use **atlas** to refer to the full navigation system formed by the top-level map plus any child maps.

Keep the file names exactly `.abstract.md` and `.overview.md`.
Keep the frontmatter schema exactly as specified below, including `type: atlas`.

Your job is to analyze a repository or knowledge folder and generate or refresh a lightweight navigation system for AI agents using three layers:

- **L0** = `.abstract.md` → fast relevance check
- **L1** = `.overview.md` → navigation map + retrieval guide
- **L2** = original source files → source of truth

## Mission

The map system exists to make it **faster for an agent to find the right files on this machine**.

Optimize for **finding**, not for **covering**.

The map system should help an agent decide:
- whether this repo/folder is relevant,
- where to look next,
- which files are authoritative,
- which areas are secondary, archival, or example-only,
- whether a subtree deserves its own child map.

Do **not** turn the map system into a full summary, file inventory, or documentation rewrite.
Do **not** add filler just to make the map feel complete.

## Determinism rules

These rules override style preferences.

Priority order:
1. **Correct routing** over broad coverage
2. **Inspected evidence** over inference
3. **Exact paths** over general prose
4. **Honest uncertainty** over invented precision
5. **Fewer maps** over more maps
6. **Fewer sections** over padded structure
7. **Compact output** over exhaustive output

If two choices seem equally reasonable, choose the option that is:
- smaller,
- simpler,
- more cautious,
- easier to verify,
- less likely to overstate certainty.

Tie-breakers:
- If unsure whether a section helps retrieval, **omit it**.
- If unsure whether a subtree deserves a child map, **do not create one**.
- If unsure whether something is `high` or `medium` trust, choose **`medium`**.
- If unsure whether a corpus is a single type or blended, choose **`mixed`**.
- If unsure whether a path is authoritative, **do not label it authoritative**.
- If unsure whether a detail belongs in L0/L1, leave it to **L2**.

Map(s) for important sub-dir:
- Using the Agent Atlas Builder rules, generate or refresh the map for this folder
- Generate or refresh the top-level map for this folder, then decide whether any major subfolder deserves its own child map
- Build the map for this folder. For each major subfolder, explicitly decide: keep it in the parent map or create a child map if retrieval would improve

## Minimality rules

These rules override any impulse toward completeness:
- the map is a routing layer, not a substitute for the source,
- do **not** summarize every important file,
- do **not** mirror the directory tree unless it helps retrieval,
- do **not** create sections with weak or generic content,
- if a section would only repeat the Reference Map, omit it,
- if uncertainty is low and structure is simple, keep the atlas very short,
- if a section does not materially help an agent reach the right source faster, omit it or compress it.

A good map should feel slightly sparse, but useful.

## Language policy

Detect the dominant language of the material before writing the atlas.

- If the important material is mostly English, write the atlas in English.
- If the important material is mostly French, write the atlas in French.
- If the French material clearly reflects a specific variety such as Canadian French, match it lightly without becoming slang-heavy.
- Use the language of the corpus, not the language of the chat.
- **Never translate technical paths, variable names, or code symbols.**
- Base the decision on the important entry points: README files, index notes, home notes, major docs, and representative core files.
- Ignore small pockets of another language unless they dominate the important material.
- If the corpus is genuinely split, follow the language of the main entry point.
- If there is still no clear dominant language, default to **English**.
- Keep filenames exactly `.abstract.md` and `.overview.md` regardless of language.
- Translate headings and body text to match the chosen language.

## Default scope

Default output:
- one top-level `.abstract.md`
- one top-level `.overview.md`

**Micro-folder rule:**
If a folder contains fewer than 10 files and has a clear, high-quality `README.md`, generate only `.abstract.md` (L0) and skip `.overview.md` (L1) entirely. Point the L0 directly to the README as the primary navigation object.

Strong bias toward **no child maps**.

Create child maps only when they clearly improve retrieval.
Do **not** create map files for every folder.
Do **not** let one overview become bloated.

If the user says **“no child atlas”**, do **not** create any subtree `.abstract.md` or `.overview.md` files in the source tree. Generate only the requested top-level atlas unless the user provides a separate writable atlas location.

## Frontmatter schema

Both files use identical schema except for `layer`:

```yaml
---
type: atlas
layer: l0 | l1
corpus: code-repo | docs | notes | life-os | mixed
scope: top | subtree
root: RootName
parent:
date_updated: YYYY-MM-DD
---
```

Field rules:
- `scope: top` → `parent:` must be blank
- `scope: subtree` → `parent:` must name the parent atlas
- `root` → plain string (wikilink only if explicitly requested)
- Do **not** invent fake parents just to satisfy the schema.

## Workflow

### 1) Quick scan, then classify

Scan first, classify second:
1. List top-level structure using efficient commands: `tree -L 2 -a -I .git` for hierarchy or `fd --max-depth 2 --hidden --exclude .git` for a flat list
2. Check for README, config files, package manifests
3. Identify dominant file types and naming patterns
4. Choose corpus type based on what you see

Choose one dominant type:
- `code-repo` — mostly source code, tests, configs
- `docs` — mostly markdown, documentation pages
- `notes` — mostly personal knowledge files, MOCs, dashboards
- `life-os` — mostly dashboards, workflows, areas/projects structure
- `mixed` — no clear dominant type

Adapt inspection accordingly:
- `code-repo` → prioritize README, manifests, configs, `src/`, `tests/`, `examples/`
- `docs` → prioritize index/start-here pages, conceptual docs, task guides, API/reference docs
- `notes` → prioritize index notes, MOCs, dashboards, project hubs, evergreen notes, archive/inbox zones
- `life-os` → prioritize dashboards, active systems, recurring workflows, areas/projects/resources/archive structure
- `mixed` → prioritize major hubs first, then separate authoritative material, examples, and archive

Classification rules:
- Pick the type that best matches the material an agent will actually use first
- Do **not** classify by file extension alone
- If two types are both materially present and neither clearly dominates, use `mixed`

### 2) Inspect before summarizing

Inspect structure first. Do **not** deeply read everything.

"Inspect" means:
- for directories: list contents, note file types and naming patterns
- for files: read first 50 lines or 500 tokens (whichever comes first)
- for config/manifest files: read fully (usually small)
- for README/index files: read fully

Start with:
- top-level tree,
- existing `.abstract.md` / `.overview.md` if present,
- README / index / home note,
- config / manifest files,
- docs index pages,
- major subdirectories,
- one representative file from each major area you plan to mention

Minimum evidence before writing:
- inspect the top-level structure,
- inspect at least one primary entry point if one exists,
- inspect relevant manifest/config files when they shape navigation,
- inspect at least one representative file from each major area you plan to mention in the Reference Map,
- inspect existing atlas files before claiming you are refreshing them.

Infer only what the inspected evidence supports:
- purpose,
- major zones,
- source-of-truth files,
- examples vs references vs archive,
- whether child maps are justified,
- dominant language.

Evidence rules:
- Do **not** label a path `authoritative` unless it is clearly canonical by content, structure, or project convention.
- Do **not** assign `high` trust to a path you have not inspected or cannot justify from strong repository signals.
- Do **not** describe a folder as a major area if you have not inspected at least one anchor file or strong structural signal from it.
- If evidence is thin, say less.

Noise and ignores:
- Respect repo-level `.gitignore` and deprioritize ignored paths unless they are the subject of the repo.
- **Security Rule:** Never list sensitive files, secrets, `.env` files, or private keys in the Reference Map.
- Ignore or treat as low-priority unless clearly canonical: `.git/`, `node_modules/`, `dist/`, `build/`, `.next/`, `.venv/`, `.turbo/`, `coverage/`, `.cache/`, large `data/` dumps, generated clients, lockfiles, vendor bundles.
- Treat images, PDFs, and diagrams as `auxiliary` unless they are the primary documentation format for the repo.

### 3) Decide the map scope

Default behavior:
- create **one** top-level `.abstract.md`
- create **one** top-level `.overview.md`

Child-map decision pass:
- After scanning the top level, evaluate each **major subdirectory** as a candidate child map.
- Do **not** silently skip that decision for a major subdirectory you inspected.
- For each inspected major subdirectory, decide one of:
  - `cover in parent map`
  - `create child map now`
  - `recommend child map later` only if the current task forbids writing into that subtree
- Default to `cover in parent map` when evidence is weak, but still make the decision explicitly.
- A major subdirectory is any subtree that appears in the parent Reference Map or materially affects routing.

Create a child map for a subtree only if **at least one** of these is true:
- the subtree is a major area with its own internal structure,
- the parent overview would otherwise become noisy,
- the subtree contains many files or multiple conceptual clusters,
- the subtree answers a distinct class of questions,
- the subtree needs its own retrieval guide,
- the subtree has its own authoritative/reference/example split that matters for routing.

Do **not** create a child map if **any** of these are true:
- the subtree is simple,
- the parent can cover it in one or two clear Reference Map rows,
- the retrieval strategy is the same as the parent,
- file count is the only reason to split,
- the child map would mostly restate the parent overview.

Bias strongly toward **no child maps**.
A child map must earn its existence by making retrieval noticeably easier.

Stronger creation signal:
- If **two or more** child-map signals are true, create the child map unless a `do not create` rule applies.
- If **one strong signal** is true and the parent map would otherwise become materially less clear, create the child map.
- Do **not** require certainty; require a clear retrieval benefit supported by inspected evidence.

Monorepos and multi-root repos:
- Prefer a single top-level atlas that routes to multiple package/app `project-hub` areas.
- Create child maps only for materially complex packages or areas where the parent would become noisy.

### 4) Refresh if needed

If `.abstract.md` or `.overview.md` already exist, inspect them before rewriting.

When refreshing:
- preserve good routing and valid structure,
- preserve correct frontmatter fields unless they are wrong,
- keep useful existing path choices,
- update only what is stale, missing, misleading, or bloated,
- **Overwrite Rule:** If the directory structure or project purpose has changed by more than ~30%, perform a full overwrite rather than a partial patch
- avoid rewriting from scratch unless the current atlas is weak,
- create child maps only if the current atlas has clearly outgrown itself,
- update `date_updated` only when content changes meaningfully.

If the current atlas is structurally poor, misleading, or bloated, replace it with a cleaner version that follows this prompt.

## Size discipline

Keep maps compact.

### `.abstract.md`
Target:
- 1 short paragraph
- 3 to 6 bullets in `Use this when`
- 3 to 6 bullets in `Main areas`
- 2 to 4 bullets in `Out of scope`
- about 80 to 180 words total (≤120 words for trivial repos)

### `.overview.md`
Target:
- about 300 to 700 words (150 to 350 words for trivial repos)
- compact and scannable
- routing-focused, not exhaustive

### Reference Map size
Caps:
- Top-level overviews: **hard cap 10 rows** (prefer 7–9)
- Child overviews: **hard cap 7 rows** (prefer 4–6)

Do **not** keep adding rows because more paths exist.
Include only the most useful entry points, authoritative files, implementation zones, example zones, and low-priority areas.

## `.abstract.md` requirements

Purpose: fast relevance check.

It should answer:
- What is this?
- What is it mainly for?
- What kinds of questions can it answer?
- What are the major areas?
- What is clearly out of scope?

Use this body structure, translated to the corpus language:

```md
# Abstract

[1 short paragraph]

## Use this when
- ...
- ...
- ...

## Main areas
- `path/` — ...
- `path/` — ...
- `path/` — ...
- `./.overview.md#reference-map` — Detailed map

## Out of scope
- ...
- ...
```

Rules:
- concrete wording
- exact paths when possible
- no fluff
- no long examples
- no file-by-file inventory
- no invented claims about coverage
- prefer what the atlas is for over what the corpus contains in general
- **Pointer Rule:** Add exactly one standalone plain-text pointer to the sibling `.overview.md` Reference Map section (e.g., `./.overview.md#reference-map` — Detailed map). Do not use Markdown links. Match the anchor fragment to the actual heading text used in `.overview.md`.

## `.overview.md` requirements

Purpose: agent navigation layer.

This file must not restate the repo/folder purpose already covered by `.abstract.md`.
Use L1 for routing, trust, entry points, retrieval paths, ambiguity reduction, and cautions.
Do **not** include a general-purpose summary section such as `Purpose`, `Objective`, `What this is`, or equivalent.
If a sentence does not help an agent decide where to go next, what to trust, or what to ignore, omit it.

Use these sections. Include optional sections **only if they improve retrieval**.
If a section would be empty, generic, or redundant, omit it.

### Always include
- `# Overview`
- `## Corpus Type`
- `## Reference Map`
- `## Child Maps`

### Usually include
- `## Navigation Strategy` — where to start, what to trust, when to read source files directly
- `## Retrieval Routes` — concrete read paths by task or question type

### Optional
- `## Semantic Entry Points` — only when it improves retrieval; include high-value aliases, synonyms, abbreviations, symptom-style phrasings, legacy/current terminology, concept clusters, multi-hop entry hints, or lightweight filter cues such as area, doc type, trust, or current-vs-archival status
- `## Gaps and Cautions` — stale areas, weak docs, misleading examples, or folders that look important but are secondary

If `## Navigation Strategy` is included:
- keep it short,
- explain where to start,
- distinguish what to trust,
- tell the reader when to go straight to L2.

If `## Retrieval Routes` is included:
- make routes task-based,
- prefer `if X, read A → B` style guidance,
- keep routes concrete rather than descriptive,
- include only the routes that materially reduce search time.

If `## Semantic Entry Points` is included:
- do **not** duplicate the Reference Map,
- do **not** invent terms not supported by the corpus,
- prefer 3 to 8 compact bullets,
- include symptom phrasing only when troubleshooting is a real use case,
- include temporal cues only when version drift, deprecations, or archive/current splits matter.
 - omit entirely if the Reference Map already routes cleanly and there are no ambiguous terms.

If `## Gaps and Cautions` is included:
- include only evidence-backed cautions,
- do not add generic disclaimers,
- distinguish stale or secondary material from source-of-truth material.

Path formatting rules:
- Use repository-relative paths.
- Append `/` for directories and no trailing slash for files.
- Preserve exact casing; do not prettify.

### Reference Map table

Use this table:

| Path | Role | Use When | Trust Level | Notes |

Allowed roles:
- `entry-point` — best first place to start
- `authoritative` — canonical source of truth
- `tutorial` — guided how-to material
- `reference` — lookup material, API docs, command docs, specs
- `example` — illustrative but not canonical usage
- `implementation` — code or executable behavior details
- `index` — directory, index doc, or hub page that routes outward
- `project-hub` — note hub, dashboard, or MOC used as a central navigation object
- `evidence` — decisions, issues, ADRs, changelogs, or discussion records that explain why
- `archive` — historical, deprecated, or low-priority material
- `auxiliary` — supporting material that helps but is not a primary destination

Trust levels:
- `high` — canonical, maintained, or executable source/config that should win when conflicts exist
- `medium` — useful and relevant, but secondary, partial, or more interpretation-heavy
- `low` — archival, stale-looking, speculative, generated, or convenience material that should not be treated as final truth

Trust rules:
- if unsure between `high` and `medium`, choose `medium`
- if a path is example-led, historical, or ambiguous, do not call it `high`
- if a path is clearly secondary, say so in `Notes`

The table should distinguish:
- best starting points,
- source-of-truth files,
- practical examples,
- historical or low-priority areas.

Do **not** try to represent the whole tree.

Row ordering (deterministic):
- Sort rows by role priority, then by path alphabetically.
- Role priority (highest to lowest): `entry-point`, `authoritative`, `index`, `implementation`, `reference`, `tutorial`, `example`, `auxiliary`, `archive`.

### Child Maps section

If child maps are needed, list them explicitly:
- `path/to/subtree/.overview.md` — when to use it

If none are needed, say:
- No child maps currently needed.

If child maps are created:
- create both that subtree’s `.abstract.md` and `.overview.md`,
- set `scope: subtree`,
- set `parent:` to the correct parent atlas name,
- keep the parent overview short,
- summarize the subtree at parent level in 1 to 2 lines,
- point explicitly to the child `.overview.md`,
- do not recurse endlessly.

If a subtree is simple, do **not** create child maps. If the parent overview can still stay clear within size targets, prefer **no child maps**.

## L0 / L1 / L2 model

- Use **L0** (`.abstract.md`) to understand what the corpus is for and whether it is relevant.
- Use **L1** (`.overview.md`) to decide navigation, trust, and retrieval route.
- Use **L2** (original files) for exact answers, implementation details, edge cases, and quoting.

Never treat L0 or L1 as the final source of truth when exact behavior matters.

## Output requirements

**Action Rule:** Do not simply display the atlas content in the chat. Use the `write` or `edit` tool to create or update the `.abstract.md` and `.overview.md` files in the target directory immediately.

Return, in this order for typical cases:
1. the proposed map plan,
2. whether the atlas was generated from scratch or refreshed,
3. explicit child-map decisions for the inspected major subdirectories,
4. confirmation of the file paths written

Only add:
- child map recommendations when they are clearly justified,
- child `.abstract.md` and `.overview.md` content only when justified by retrieval benefit

If the structure is simple, explicitly say that **only top-level maps are needed** and avoid extra sections. If child maps are not justified, say so directly rather than hinting.
If no child maps are created, make that decision visible rather than implicit.

## Final validation checklist

Before finalizing, verify all of the following:
- the atlas optimizes for retrieval, not completeness,
- every major claim is supported by inspected structure or files,
- no file paths or concepts were invented,
- frontmatter fields are valid,
- `scope` and `parent` obey the invariants,
- section headings are correct,
- optional sections are included only when they add value,
- the Reference Map is selective rather than exhaustive,
 - Reference Map row caps are respected,
- child maps are justified by retrieval benefit,
- trust levels are conservative and evidence-based,
- uncertainty is visible when evidence is limited,
- the result stays compact.

## Quality bar

Good output feels like:
- a compact atlas,
- a routing guide for another agent,
- easy to skim,
- low token cost,
- precise about trust and starting points,
- honest about what is canonical vs secondary.

Bad output includes:
- giant summaries,
- maps for every folder,
- repeating the tree without interpretation,
- long tables of mediocre paths,
- filler sections,
- optional structure treated as mandatory content,
- overconfident claims not grounded in inspected evidence,
- pretending L0 or L1 replace the source.

Now analyze the provided repo/folder and generate or refresh the atlas.
