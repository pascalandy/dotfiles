---
name: gstack
description: "Unified gstack routing across planning, active work, and shipping. USE WHEN idea, brainstorm, wedge, founder review, office hours, architecture review, data flow, edge cases, test plan, design system, visual direction, debug, broken flow, root cause, investigate, inspect, browser, Chrome, review diff, review branch, QA, test and fix, QA report only, security review, threat model, OWASP, benchmark, performance baseline, codex review, codex challenge, second opinion, consult codex, ship, open PR, push, release, deploy, canary, setup deploy, safety mode, freeze, guard, unfreeze, import cookies, update docs after shipping, retro, learn, upgrade gstack."
---

# gstack

## Routing

| Phase | Request Pattern | Route To | Use When |
|---|---|---|---|
| Plan | idea, brainstorm, worth building, office hours, wedge | `office-hours/SKILL.md` | The user needs product framing, wedge definition, or prioritization help |
| Plan | founder review, think bigger, challenge the scope | `plan-ceo-review/SKILL.md` | The user wants a founder-level challenge to ambition or scope |
| Plan | run the full planning review loop | `autoplan/SKILL.md` | The user wants a broader planning workflow rather than one narrow review |
| Plan | architecture review, data flow, edge cases, test plan | `plan-eng-review/SKILL.md` | The user needs engineering review of structure, dependencies, and verification |
| Plan | design review of the plan itself, planned UX critique | `plan-design-review/SKILL.md` | The user wants planned UX or design quality reviewed before implementation |
| Plan | design system, brand, visual direction | `design-consultation/SKILL.md` | The user needs a coherent design system or visual language |
| Plan | explore multiple design options | `design-shotgun/SKILL.md` | The user wants multiple design directions before choosing one |
| Work | bug, broken flow, root cause, investigate | `investigate/SKILL.md` | The user needs systematic debugging and root-cause analysis |
| Work | inspect the page, click through, capture evidence | `browse/SKILL.md` | The user needs fast browser interaction and evidence capture |
| Work | use real Chrome or side panel control | `connect-chrome/SKILL.md` | The user needs real-browser control beyond the default browser workflow |
| Work | generate production HTML from an approved mockup | `design-html/SKILL.md` | The user has approved design output that now needs production-ready HTML |
| Work | review this diff, review the branch | `review/SKILL.md` | The user wants a code-review style defect and risk pass |
| Work | QA the site, test and fix | `qa/SKILL.md` | The user wants bugs found and fixed in one loop |
| Work | QA report only | `qa-only/SKILL.md` | The user wants evidence and reporting without code changes |
| Work | polish the live UI with fixes | `design-review/SKILL.md` | The user wants visual QA plus direct UI corrections |
| Work | security review, threat model, OWASP | `cso/SKILL.md` | The user needs security posture, threat, or abuse-case analysis |
| Work | benchmark, compare before and after, performance baseline | `benchmark/SKILL.md` | The user needs measured performance comparison or baseline capture |
| Work | codex review, codex challenge, second opinion, consult codex | `codex/SKILL.md` | The user wants an independent Codex-powered code review, adversarial challenge, or consultation |
| Ship | ship, open PR, push, prepare release | `ship/SKILL.md` | The user wants the standard shipping workflow |
| Ship | merge and deploy, verify production | `land-and-deploy/SKILL.md` | The user wants merge-to-prod execution plus verification |
| Ship | watch rollout, canary check | `canary/SKILL.md` | The user wants rollout observation after deployment |
| Ship | configure deploy flow before first use | `setup-deploy/SKILL.md` | The user needs deploy workflow setup before shipping normally |
| Ship | be careful, safety mode | `careful/SKILL.md` | The user wants extra warnings before risky actions |
| Ship | freeze this directory | `freeze/SKILL.md` | The user wants hard edit restrictions on a path |
| Ship | guard mode | `guard/SKILL.md` | The user wants both warnings and path restrictions together |
| Ship | remove freeze | `unfreeze/SKILL.md` | The user wants existing path restrictions removed |
| Ship | import cookies for authenticated testing | `setup-browser-cookies/SKILL.md` | The user needs auth state for browser testing workflows |
| Ship | update docs after shipping | `document-release/SKILL.md` | The user wants shipped behavior reflected in docs |
| Ship | weekly retro | `retro/SKILL.md` | The user wants an iteration or team retrospective |
| Ship | manage learnings | `learn/SKILL.md` | The user wants lessons captured and organized |
| Ship | upgrade gstack | `gstack-upgrade/SKILL.md` | The user wants the gstack installation refreshed |
