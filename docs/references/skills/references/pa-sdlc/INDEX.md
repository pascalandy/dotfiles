---
name: pa-sdlc
description: The Pascal Andy Software Development Lifecycle — 9 `pa-*` skills covering idea, discovery, scoping, direction, architecture, implementation, retrospective, and documentation
aliases:
  - pa-sdlc
  - sdlc
tags:
  - area/ea
  - kind/wiki
  - status/open
  - bucket/pa-sdlc
date_created: 2026-04-11
date_updated: 2026-04-18
---

# pa-sdlc

> Narrative layer for the 9 `pa-*` skills under `dot_config/ai_templates/skills/pa-sdlc/`.
> Each page is a concise summary: what the skill does, when to use it, when not to.
> **Parent index:** [`../../INDEX.md`](../../INDEX.md) | **Total pages:** 10 | **Last updated:** 2026-04-18

## The 9 skills

| Skill | One-line purpose | Page |
|---|---|---|
| `pa-idea` | Write down a rough idea into `docs/references/ideas/` preserving voice and language | [pa-idea.md](references/pa-idea.md) |
| `pa-scout` | Discover and map an unfamiliar surface | [pa-scout.md](references/pa-scout.md) |
| `pa-scope` | Decide what a requested change actually touches | [pa-scope.md](references/pa-scope.md) |
| `pa-vision` | Pressure-test or define where the work is going | [pa-vision.md](references/pa-vision.md) |
| `pa-architect` | Turn settled direction into an execution plan | [pa-architect.md](references/pa-architect.md) |
| `pa-implement` | Apply a bounded change or repair broken behavior | [pa-implement.md](references/pa-implement.md) |
| `pa-postmortem` | Preserve what is worth remembering after work is done | [pa-postmortem.md](references/pa-postmortem.md) |
| `pa-doc-update` | Capture one concrete change, decision, or artifact in docs | [pa-doc-update.md](references/pa-doc-update.md) |
| `pa-doc-cleaner` | Maintain existing docs — drift review, dedup, governance | [pa-doc-cleaner.md](references/pa-doc-cleaner.md) |

## Cross-stage pattern

| Page | What it is |
|---|---|
| [advisor.md](references/advisor.md) | `pa-advisor` cross-stage consultation pattern (executor → advisor via `claude -p`). No matching skill exists in the source tree today — kept as a pattern page. |

## Stage picker

Pick the stage that answers your *current* question.

| Current question | Stage |
|---|---|
| "Let me write this idea down." | `pa-idea` |
| "What is this?" | `pa-scout` |
| "What does this change touch?" | `pa-scope` |
| "Is this the right thing to build?" | `pa-vision` |
| "How do we get there?" | `pa-architect` |
| "Let's build it." / "It's broken." | `pa-implement` |
| "What should we remember from this?" | `pa-postmortem` |
| "What did we just change?" | `pa-doc-update` |
| "Are the docs still true?" | `pa-doc-cleaner` |
| "Am I off track?" | `pa-advisor` (pattern) |

## Lifecycle shape

```
pa-idea  →  pa-scout  →  pa-scope  →  pa-vision  →  pa-architect  →  pa-implement  →  pa-doc-update  →  pa-postmortem
                                                         ↓
                                                pa-advisor (any time)
                                                                                              ↓
                                                                                      pa-doc-cleaner (periodic)
```

Smaller tasks skip stages: a focused bug fix might go `pa-scope → pa-implement → pa-doc-update`. A research question might be `pa-scout` alone. The sequence is a scaffold, not a mandate.

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/doc

| File | Description |
|------|-------------|
| `references/pa-idea.md` | `pa-idea`: idea-capture entry point |
| `references/pa-scout.md` | `pa-scout`: discovery entry point |
| `references/pa-scope.md` | `pa-scope`: scoping entry point |
| `references/pa-vision.md` | `pa-vision`: direction-setting entry point |
| `references/pa-architect.md` | `pa-architect`: execution-design entry point |
| `references/pa-implement.md` | `pa-implement`: execution entry point |
| `references/pa-postmortem.md` | `pa-postmortem`: retrospective entry point |
| `references/pa-doc-update.md` | `pa-doc-update`: documentation entry point |
| `references/pa-doc-cleaner.md` | `pa-doc-cleaner`: documentation maintenance entry point |
| `references/advisor.md` | `pa-advisor`: cross-stage consultation pattern (no matching skill) |

## Related

- [[docs/INDEX.md]] — root catalog
- [[how-to-configure-opencode]] — skills and commands surface per agent
- [[how-ai-templates-are-distributed]] — how `pa-sdlc/` skills fan out to every agent home
