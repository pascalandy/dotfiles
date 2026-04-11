---
name: mattpocock
description: Matt Pocock's engineering methodology -- product planning (PRDs, plans, issues), architecture design (deep modules, interfaces, refactoring, DDD), test-driven development (red-green-refactor vertical slices), issue triage (bug investigation, QA sessions, GitHub workflow), and technical writing (articles, skills). USE WHEN write PRD, product requirements, plan feature, create issues, vertical slices, tracer bullets, grill me, design interface, design it twice, deep modules, improve architecture, refactor plan, ubiquitous language, DDD, TDD, red-green-refactor, test-first, triage, investigate bug, QA session, root cause, edit article, write skill.
keywords: [PRD, product-requirements, plan, issues, vertical-slices, tracer-bullets, grill, design-interface, deep-modules, architecture, refactor, ubiquitous-language, DDD, TDD, red-green-refactor, test-first, triage, bug, QA, root-cause, edit-article, write-skill]
---

# Matt Pocock's Engineering Methodology

> Fourteen engineering workflows in five domains -- from writing PRDs through architecture design to test-driven development, routed automatically based on what you need.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Building software well requires different disciplines at different stages. Writing a PRD demands relentless interviewing to reach shared understanding. Breaking that PRD into work requires tracer-bullet vertical slices, not horizontal layers. Designing module interfaces requires generating radically different options and comparing trade-offs. Coding requires test-driven vertical slices with deep modules. Triaging bugs requires systematic root cause investigation before filing issues. But most engineering workflows either cover one stage well and ignore the rest, or try to cover everything with generic advice. You end up:

- **Planning without rigor** -- PRDs that skip the hard questions, plans that slice horizontally instead of vertically, issues that lack acceptance criteria
- **Designing without comparison** -- picking the first interface that comes to mind instead of generating radically different options
- **Coding without tests driving design** -- writing tests after code, testing implementation details instead of behavior, mocking internal collaborators
- **Triaging without investigation** -- filing vague bug reports without root cause analysis, missing the TDD fix plan
- **Losing domain knowledge** -- no ubiquitous language, no institutional memory of rejected features, no durable agent briefs

The fundamental issue: each stage of engineering has its own methodology, and doing any stage well requires structured workflows, not just good intentions.

---

## The Solution

The Matt Pocock skill provides fourteen workflows across five engineering domains, each grounded in specific principles:

1. **ProductPlanning** -- The full pipeline from problem to work items. Write PRDs through relentless user interviews. Convert PRDs to phased implementation plans using tracer-bullet vertical slices. Break plans into independently-grabbable GitHub issues. Stress-test any plan with exhaustive grilling sessions. Four workflows: WritePRD, PRDToPlan, PRDToIssues, GrillMe.

2. **ArchitectureDesign** -- Module interface design and codebase improvement. Generate multiple radically different interface designs via parallel agents (inspired by "Design It Twice" from Ousterhout's "A Philosophy of Software Design"). Explore codebases for architectural friction and propose deep-module refactors. Plan refactors as sequences of tiny commits (Martin Fowler). Extract DDD-style ubiquitous language glossaries. Four workflows: DesignInterface, ImproveArchitecture, RequestRefactor, UbiquitousLanguage.

3. **TDD** -- Test-driven development with vertical-slice red-green-refactor loops. Tests verify behavior through public interfaces, not implementation details. Integration-style tests over mocks. Boundary-only mocking. Deep module design for testability. One workflow with five supporting references: RedGreenRefactor, plus TestPhilosophy, InterfaceDesign, Mocking, Refactoring, DeepModules.

4. **IssueTriage** -- Bug investigation and issue management. Full GitHub issue triage via label-based state machine with grilling sessions and agent briefs. Investigate bugs by exploring the codebase for root cause, then file issues with TDD fix plans. Run interactive QA sessions where bugs are reported conversationally and filed as durable GitHub issues. Three workflows: GithubTriage, TriageIssue, QASession.

5. **Writing** -- Technical writing and skill creation. Edit articles by restructuring sections for information dependency ordering and tightening prose. Create new agent skills with proper structure, progressive disclosure, and bundled resources. Two workflows: EditArticle, WriteASkill.

The collection loads the router, which dispatches to the right domain based on keyword matching. Each domain has its own workflows and supporting references.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | Dispatches requests to the right engineering domain |
| ProductPlanning skill | `references/ProductPlanning/MetaSkill.md` | PRD writing, planning, issue creation, design grilling |
| ProductPlanning workflows | `references/ProductPlanning/workflows/` | 4 workflows: WritePRD, PRDToPlan, PRDToIssues, GrillMe |
| ArchitectureDesign skill | `references/ArchitectureDesign/MetaSkill.md` | Interface design, architecture improvement, refactoring, DDD |
| ArchitectureDesign workflows | `references/ArchitectureDesign/workflows/` | 4 workflows: DesignInterface, ImproveArchitecture, RequestRefactor, UbiquitousLanguage |
| ArchitectureDesign references | `references/ArchitectureDesign/references/` | Deep module philosophy, dependency categories |
| TDD skill | `references/TDD/MetaSkill.md` | Test-driven development with vertical slices |
| TDD workflows | `references/TDD/workflows/` | 1 workflow: RedGreenRefactor |
| TDD references | `references/TDD/references/` | TestPhilosophy, InterfaceDesign, Mocking, Refactoring, DeepModules |
| IssueTriage skill | `references/IssueTriage/MetaSkill.md` | Bug investigation, issue management, QA sessions |
| IssueTriage workflows | `references/IssueTriage/workflows/` | 3 workflows: GithubTriage, TriageIssue, QASession |
| IssueTriage references | `references/IssueTriage/references/` | Agent brief format, out-of-scope knowledge base |
| Writing skill | `references/Writing/MetaSkill.md` | Article editing and skill creation |
| Writing workflows | `references/Writing/workflows/` | 2 workflows: EditArticle, WriteASkill |

**Summary:**
- **Domains:** 5 (ProductPlanning, ArchitectureDesign, TDD, IssueTriage, Writing)
- **Workflows:** 14 across all domains
- **Supporting references:** 8 reference files
- **Dependencies:** None (works standalone, uses `gh` CLI for GitHub operations when available)

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "write a PRD for this feature" | Routes to ProductPlanning -- runs WritePRD workflow |
| "break this PRD into a plan" | Routes to ProductPlanning -- runs PRDToPlan workflow |
| "create issues from this PRD" | Routes to ProductPlanning -- runs PRDToIssues workflow |
| "grill me on this design" | Routes to ProductPlanning -- runs GrillMe workflow |
| "design the interface for this module" | Routes to ArchitectureDesign -- runs DesignInterface workflow |
| "find architecture improvements" | Routes to ArchitectureDesign -- runs ImproveArchitecture workflow |
| "plan this refactor" | Routes to ArchitectureDesign -- runs RequestRefactor workflow |
| "extract the ubiquitous language" | Routes to ArchitectureDesign -- runs UbiquitousLanguage workflow |
| "build this feature with TDD" | Routes to TDD -- runs RedGreenRefactor workflow |
| "triage the incoming issues" | Routes to IssueTriage -- runs GithubTriage workflow |
| "investigate this bug" | Routes to IssueTriage -- runs TriageIssue workflow |
| "let's do a QA session" | Routes to IssueTriage -- runs QASession workflow |
| "edit this article" | Routes to Writing -- runs EditArticle workflow |
| "help me write a new skill" | Routes to Writing -- runs WriteASkill workflow |

---

## Example Usage

### Writing a PRD

```
User: write a PRD for adding real-time collaboration to the editor

AI responds:
Running the WritePRD workflow...

[Asks for detailed problem description]
[Explores codebase to verify assertions]
[Interviews relentlessly about every design branch]
[Sketches major modules, identifies deep module opportunities]
[Creates GitHub issue with: Problem Statement, Solution, User Stories,
 Implementation Decisions, Testing Decisions, Out of Scope]
```

### Designing an Interface

```
User: design the interface for the payment processing module

AI responds:
Running the DesignInterface workflow...

[Gathers requirements: problem, callers, operations, constraints]
[Spawns 3+ parallel agents with different design constraints]
  - Agent 1: Minimize method count (1-3 methods max)
  - Agent 2: Maximize flexibility
  - Agent 3: Optimize for the most common case
[Presents each design with signature, usage examples, what it hides]
[Compares on: simplicity, generality, efficiency, depth, misuse risk]
[Synthesizes best elements into recommended interface]
```

### Test-Driven Development

```
User: implement the notification system using TDD

AI responds:
Running the RedGreenRefactor workflow...

Planning: confirm interfaces, behaviors to test, deep module opportunities
Tracer Bullet (Slice 1):
  RED: Write test for "send notification to single user" -> fails
  GREEN: Minimal implementation -> passes
Slice 2:
  RED: Write test for "batch notifications" -> fails
  GREEN: Extend implementation -> passes
...
REFACTOR: Extract duplication, deepen modules, all tests still pass.
```

---

## Key Principles

These principles from Matt Pocock's methodology run through all five domains:

- **Vertical slices over horizontal layers** -- Every plan, every TDD cycle, every issue is a thin end-to-end slice through all integration layers, not a horizontal cut at one layer
- **Deep modules over shallow modules** -- Small interfaces hiding significant complexity (Ousterhout). Prefer fewer methods, simpler params, more hidden internals
- **Design it twice** -- Your first idea is unlikely to be the best. Generate radically different options before choosing
- **Tiny commits** -- Each refactoring step as small as possible (Fowler). Each commit leaves the codebase working
- **Behavior over implementation** -- Tests verify what the system does through public interfaces, not how it does it internally
- **Durable descriptions** -- No file paths or line numbers in issues or briefs. Describe interfaces, types, and behavioral contracts that survive refactors
- **Relentless interviewing** -- Walk every branch of the decision tree. If a question can be answered by exploring the codebase, explore instead of asking

---

## What Makes This Different

This sounds similar to generic project management or code review skills. What makes this approach different?

These are not templates or checklists -- they are complete methodologies with specific, opinionated workflows. When you ask to design an interface, the skill spawns multiple parallel agents with radically different design constraints and produces a structured comparison. When you triage an issue, a label-based state machine tracks the issue through grilling sessions to agent briefs. When you write a PRD, the interview process walks every branch of the decision tree until shared understanding is reached.

Key differentiators:
- **Vertical slices everywhere** -- plans, issues, TDD cycles all slice through every integration layer end-to-end, never horizontally
- **Parallel sub-agents for design** -- interface design and architecture improvement spawn 3+ agents with different constraints, not just one answer
- **Label-based state machine** -- issue triage uses a formal state machine with specific transitions and outcome actions
- **Agent briefs** -- issues marked `ready-for-agent` get structured, durable specifications an autonomous agent can work from
- **Institutional memory** -- rejected features are tracked in an out-of-scope knowledge base to prevent relitigating decisions
- **TDD fix plans** -- every bug investigation produces concrete RED-GREEN cycles, not just "fix the bug"

---

## Configuration

No configuration required. All five domains work immediately.

Optional: `gh` CLI for GitHub operations (issue creation, triage workflows). Without it, issue content is presented for manual creation.

---

## Credits

- **Original skills:** Matt Pocock -- [mattpocock/skills](https://github.com/mattpocock/skills)
- **Key influences:** John Ousterhout ("A Philosophy of Software Design"), Martin Fowler (refactoring), Eric Evans (DDD), Andy Hunt & Dave Thomas (tracer bullets)

---

## Changelog

### 1.0.0

- Initial release
- Five domains: ProductPlanning, ArchitectureDesign, TDD, IssueTriage, Writing
- 14 workflows across all domains
- 8 supporting reference files
- TypeScript code examples in TDD references
- Complete worked examples in AgentBrief, OutOfScope, and UbiquitousLanguage
- Label-based state machine for GitHub issue triage
- Source: Matt Pocock's [skills collection](https://github.com/mattpocock/skills)
