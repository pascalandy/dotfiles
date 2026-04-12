---
name: postmortem
description: Capture lessons learned from incidents, solved problems, and engineering work. Write postmortems, run retrospectives, document solutions, and search past learnings. USE WHEN postmortem, incident review, lessons learned, capture solution, document fix, blameless, root cause analysis, 5 whys, retro, retrospective, weekly review, what did we ship, search solutions, past fixes, similar problem, before I start, that worked, it's fixed, compound knowledge.
keywords: [postmortem, incident-review, lessons-learned, capture, blameless, root-cause, 5-whys, retro, retrospective, search-solutions, past-fixes, compound-knowledge]
---

# Postmortem

> Capture lessons from incidents and solved problems, run retrospectives, and search past learnings -- four specialists routed automatically based on what happened.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Teams solve the same problems repeatedly because lessons don't get captured, postmortems don't get written, and past solutions stay buried. When knowledge stays in someone's head, the team pays the research cost every time. The result:

- **Repeated mistakes** -- the same bug gets debugged three times because nobody documented the first fix
- **Shallow incident reviews** -- postmortems list what happened but never reach the root cause or produce action items
- **Lost patterns** -- engineering trends, hotspots, and work patterns go unnoticed without regular retrospectives
- **Knowledge silos** -- past solutions exist in docs/ but nobody finds them before starting new work

The fundamental issue: capturing lessons is not one activity. It is at least four distinct practices, each with its own methodology, and each triggered by different situations.

---

## The Solution

The Postmortem skill provides four specialists for capturing and retrieving lessons learned:

1. **Capture** -- Document a solved problem into structured knowledge with YAML frontmatter, cross-references, and overlap detection. Two modes: Full (parallel research) and Lightweight (single-pass).

2. **IncidentReview** -- Write formal blameless postmortems after production incidents. Three templates: Standard (full timeline, RCA, action items), 5 Whys (deep causal chain), and Quick (minor incidents). Includes facilitation guide.

3. **Retro** -- Engineering retrospective analyzing git history, work patterns, commit types, session detection, hotspot analysis, and team contributions. Supports configurable time windows and trend tracking.

4. **Research** -- Surface past solutions from the knowledge base before starting new work. Grep-first filtering against YAML frontmatter, relevance scoring, and distilled summaries to prevent repeated mistakes.

The collection `SKILL.md` loads `references/ROUTER.md`, which routes requests to the right specialist based on keyword matching.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | Dispatches requests to the right specialist |
| Capture skill | `references/Capture/MetaSkill.md` | Document solved problems |
| Capture references | `references/Capture/references/` | Resolution template, schema |
| IncidentReview skill | `references/IncidentReview/MetaSkill.md` | Formal blameless postmortems |
| IncidentReview references | `references/IncidentReview/references/` | Standard, 5 Whys, Quick templates |
| Retro skill | `references/Retro/MetaSkill.md` | Engineering retrospectives |
| Retro references | `references/Retro/references/` | Metrics schema, narrative template |
| Research skill | `references/Research/MetaSkill.md` | Search past solutions |

**Summary:**
- **Specialists:** 4 (Capture, IncidentReview, Retro, Research)
- **Templates:** 5 reference files (resolution template, schema, 3 postmortem templates, metrics schema, narrative template)
- **Dependencies:** None (works standalone)

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "that worked, document this fix" | Routes to Capture -- runs Full or Lightweight mode to document the solution |
| "compound this solution" | Routes to Capture -- captures into structured knowledge |
| "write a postmortem for last night's outage" | Routes to IncidentReview -- runs Standard template with timeline and RCA |
| "run a 5 whys on the payment failure" | Routes to IncidentReview -- runs 5 Whys template |
| "quick postmortem for the cache issue" | Routes to IncidentReview -- runs Quick template |
| "weekly retro" | Routes to Retro -- analyzes last 7 days of commits and work patterns |
| "what did we ship this week" | Routes to Retro -- generates engineering retrospective |
| "search for past fixes before I start" | Routes to Research -- surfaces relevant past solutions |
| "have we seen this error before" | Routes to Research -- searches knowledge base for similar problems |

---

## Example Usage

### Capture a Solved Problem

```
User: that worked! document this fix

AI responds:
Running Capture to document this solution...

[Extracts problem, symptoms, root cause, solution from conversation]
[Checks for related docs and overlap]
[Creates structured doc with YAML frontmatter]

File created: docs/solutions/performance-issues/n-plus-one-query.md
Cross-references: 2 related docs found
```

### Incident Review

```
User: write a postmortem for the payment outage last night

AI responds:
Running IncidentReview in Standard template...

Timeline constructed from alerts and logs
Root cause: connection pool exhaustion after config change
5 Whys analysis: traced to missing documentation on connection patterns
Action items: 4 (2 P0, 2 P1) with owners and due dates

Postmortem written with blameless analysis.
```

### Engineering Retro

```
User: /retro

AI responds:
Running Retro for the last 7 days...

47 commits across 3 contributors
Peak hours: 10pm-1am (you), 9am-12pm (team)
Ship of the week: auth middleware rewrite (+1200 LOC)
Focus score: 62% (app/services/)
Test ratio: 41% (+19pp vs last week)
Streak: 47 consecutive shipping days
```

---

## Configuration

No configuration required. All four specialists work immediately after installation.

Optional configuration:

| Customization | Location | Impact |
|--------------|----------|--------|
| Knowledge base path | Per-project `docs/solutions/` | Where captured docs are stored |
| Severity levels | Sub-skill schemas | Adjust severity classification |
| Retro time windows | Retro arguments | 24h, 7d, 14d, 30d, compare mode |
| Postmortem templates | IncidentReview references | Add custom templates |
