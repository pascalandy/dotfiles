## Skills

Discovered at startup from ~/.opencode/skill. Entries: name, description, file path. Content not inlined; context stays lean.

Example format:

- skill-name: description (file: ~/.opencode/skill/skill-name/skill.md)

### Naming Convention

Skills use prefixes to indicate their purpose:

| Prefix | Purpose | Examples |
|--------|---------|----------|
| `fct-` | Functional workflows for coding, design, architecture | architect, spec-kit, orchestration |
| `std-` | Standards and conventions to follow | bash, commit, changelog, python |
| `util-` | Utilities and tools (lazy mode execution) | password-generator, transcript, convert-to-md |
| `skill-creator` | Meta skill for creating new skills | — |

- `fct-` skills help accomplish development tasks
- `std-` skills define how code/commits/docs should look
- `util-` skills wrap scripts for quick execution without questions

### Available Skills

#### Functional (`fct-`)

| Skill | Description |
|-------|-------------|
| `brainstorm-a-feat` | Explore user intent, requirements, and design before building. Use when: creating features, adding functionality, building components, or modifying behavior. Run before implementation work. |
| `fct-architect` | Transform functional requirements into technical architecture documents (system design, data models, API specs). Use when: user provides specs needing technical design, asks for architecture, or says "architect this." Not for: task planning or implementation. |
| `fct-ask-questions` | Run structured interviews with up to 7 multiple-choice questions to clarify specs quickly. Use when: requirements are unclear and need rapid clarification. |
| `fct-ask-questions-v2` | Clarify requirements before implementing. Use when: explicitly invoked by user. Not auto-triggered. |
| `fct-frontend-design` | Create distinctive, production-grade frontend interfaces with high design quality. Use when: building web components, pages, dashboards, React components, HTML/CSS layouts, or styling any web UI. Avoids generic AI aesthetics. |
| `fct-mermaid-wip` | Create quality Mermaid diagrams (flowcharts, sequence diagrams, ERDs). Use when: user needs diagrams, visualizations, or mentions Mermaid. |
| `fct-orchestration` | Define orchestration strategy for multi-step workflows. Use when: user triggers orchestration or planning complex task sequences. |

#### Standards (`std-`)

| Skill | Description |
|-------|-------------|
| `std-bash` | Create and refactor Bash scripts following conventions (strict mode, `fct_` naming, quoting). Includes shellcheck linting. Use when: creating shell scripts, refactoring existing scripts, debugging shell errors, or linting scripts. |
| `std-changelog` | Update CHANGELOG.md following project conventions. Use when: adding, fixing, or removing features that need changelog entries. |
| `std-cli-guideline-deep` | Build CLI tools (Python, JS, Bash, Go) following modern best practices. Use when: creating new CLIs, reviewing CLI UX, implementing help/errors/output, or adding flags/args/subcommands. |
| `std-cli-guideline-short` | Design CLI parameters and UX: arguments, flags, subcommands, help text, output formats, error messages, exit codes, config/env precedence. Use when: designing a CLI spec before implementation or refactoring CLI surface area. |
| `std-color-palette-frappe` | Catppuccin Frappé color palette (hex/rgba) for consistent styling. Use when: applying colors to Mermaid diagrams or needing cohesive color references. |
| `std-commit` | Create atomic commits with targeted staging and logical splits. Use when: committing changes to git repositories. Load before any git commit operation. |
| `std-python` | Develop Python projects with uv (PEP 723 inline metadata, venv management, script execution). Use when: user mentions uv, creates Python scripts, or needs Python environment setup. |

#### Utilities (`util-`)

| Skill | Description |
|-------|-------------|
| `util-chezmoi` | Manage dotfiles via chezmoi CLI. Use when: reading, modifying, or adding config files (dotfiles) in user's home directory. Ensures edits happen in chezmoi source (~/.local/share/chezmoi) and apply correctly. |
| `util-extract-repo` | Download GitHub repos as clean source code (no .git history) to WORKDIR. Use when: cloning repos for analysis or modification. Not for: monorepos. |
| `util-nano-banana-pro-3` | Generate or edit images using Gemini 3 Pro via OpenRouter API. Use when: user says "generate image," "create picture," "edit photo," or "make an image." Supports text-to-image, image editing, and compositing. |
| `util-password-generator` | Generate secure passwords using cryptographic randomness. Use when: user asks for a password, passphrase, or secure token. |
| `util-pg-memory` | Store and retrieve memories for AI agents via PostgreSQL. Use when: storing decisions/learnings/observations, retrieving past context, searching memories, or ingesting sources. Triggers: "pgm," "remember this," "store memory," "search memories." |
| `util-project-status` | Orchestrate multi-agent workflow for project status reporting across WORKDIR and IDEATION. Use when: user asks for project status overview, requests a scan, or says "run project status." |
| `util-transcript` | Transcribe YouTube videos via Deepgram (audio to txt/json) with optional Claude summary. Use when: user provides YouTube URL for transcription. |

#### Obsidian

| Skill | Description |
|-------|-------------|
| `obsidian-bases` | Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when: working with .base files, creating database-like views, or user mentions Bases, table views, card views, filters, or formulas in Obsidian. |
| `obsidian-json-canvas` | Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when: working with .canvas files, creating visual canvases, mind maps, flowcharts, or user mentions Canvas in Obsidian. |
| `obsidian-markdown` | Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, and Obsidian-specific syntax. Use when: working with .md files in Obsidian, or user mentions wikilinks, callouts, frontmatter, tags, or embeds. |

#### Web

| Skill | Description |
|-------|-------------|
| `web-copywriting` | Write, rewrite, or improve marketing copy for web pages (homepage, landing, pricing, features, about, product). Use when: user says "write copy for," "improve this copy," "rewrite this page," "marketing copy," "headline help," or "CTA copy." See also: email-sequence, popup-cro. |
| `web-design-guidelines` | Review UI code for Web Interface Guidelines compliance. Use when: user says "review my UI," "check accessibility," "audit design," "review UX," or "check against best practices." |
| `web-seo-audit` | Audit, review, or diagnose SEO issues on websites. Use when: user mentions "SEO audit," "technical SEO," "why am I not ranking," "SEO issues," "on-page SEO," "meta tags review," or "SEO health check." See also: programmatic-seo, schema-markup. |
| `web-ui-ux-pro-max` | UI/UX design intelligence for web and mobile across 13 stacks (React, Next.js, Vue, Svelte, Tailwind, shadcn/ui, etc.). Use when: building, designing, reviewing, or optimizing UI/UX for websites, dashboards, apps. Covers: styles, palettes, fonts, accessibility, animation, layout. |

#### Skill Creation

| Skill | Description |
|-------|-------------|
| `skill-creator` | Create new skills with proper structure, best practices, and progressive disclosure. Use when: building a new skill to extend the agent. |
| `skill-creator-for-a-cli` | Create skills for CLI tools by introspecting help text, man pages, GitHub repos, and documentation. Use when: documenting a command-line tool, creating CLI guidance, or building a skill for terminal commands. |
| `skill-creator-refiner` | Tweak, edit, or verify existing skills before deployment. Use when: modifying skills or checking they work correctly. |

#### Other

| Skill | Description |
|-------|-------------|
| `subagent-selector` | Show available subagents for task delegation in opencode CLI. Use when: orchestrating tasks, selecting agents, planning delegations, or unsure which agent to use. |
| `writing-clearly-concisely` | Apply Strunk's rules for clearer, stronger writing. Use when: writing prose humans will read—documentation, commit messages, error messages, explanations, reports, or UI text. |

### Discovery

- Source of truth: project docs + runtime "## Skills" section
- Skill bodies on disk at listed paths

### Triggers

- Explicit: `$SkillName` or plain text mention → use that skill
- Implicit: task matches skill description → use it
- Multiple mentions → use all
- No carry-over across turns unless re-mentioned
- YAML `description` in SKILL.md = primary trigger signal; clarify if unsure

### Usage (progressive disclosure)

1. Open SKILL.md; read minimum needed
2. `references/` → load only files needed, no bulk
3. `scripts/` → run/patch; avoid retyping
4. `assets/`/templates → reuse, don't recreate
5. Ignore directories starting with a dot. example: `.solution_design`

### Multi-skill

- Minimal set covering request; state order
- Announce skill(s) + reason (one line)
- Skipping obvious skill → state why

### Context hygiene

- Summarize long sections; load extras only when needed
- One-hop refs preferred; avoid deep nesting
- Variants (frameworks/providers/domains) → pick relevant file(s), note choice

### Fallback

- Missing/blocked skill → say so briefly, continue with best alternative
- Unclean apply (missing files, unclear) → state issue, next-best approach, proceed
