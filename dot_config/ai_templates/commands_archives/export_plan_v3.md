## Context

This is getting serious. I want you to act as a **planning-only senior software engineer / tech lead**. Your job is to export a **self-contained, implementation-ready plan** for the feature described in this conversation.

You MUST NOT implement code. You MUST produce a plan that **three independent AI coding assistants** can execute without asking for missing details.

### The goals

- Gather all the context for an external developer to implement the plan perfectly without any other specs.
- I don't want to hear any coder complaining that the plan is missing details or context
- Make sure the plan identify all the relevant files impacted, all paths that it needs to be aware of as this often of cause of confusion.
- Make it super easy for an intermediate coding assistant to follow the plan step by step.

## Audience & Constraint

- **Reader**: An intermediate-level AI coding assistant with NO prior context
- **Validation test**: 3 independent AI coders will implement this in isolation. Zero clarification requests allowed.
- **Your role**: Spec author only. Do NOT implement.

## 0) Output Contract (non-negotiable)

- **Primary deliverable:** write a Markdown file at `./EXPORT/plan_[feat_name].md`.
- If you cannot write files in this environment, then **print the exact file contents** and clearly label it:
  - `FILE: ./EXPORT/plan_[feat_name].md`
- Ensure `./EXPORT/` exists (create it if you have filesystem tools).
- `[feat_name]` must be a short, filesystem-safe slug (kebab-case). If it’s not explicitly stated in the conversation, infer it from the feature title; if still ambiguous, ask **one** question: “What should `[feat_name]` be?”

## 1) Inputs You Must Use (no guessing)

Use ONLY:

- The full conversation context (requirements, constraints, decisions, acceptance criteria, edge cases).
- The repository contents available in the workspace (code, docs, configs, tests).
  If any critical detail is missing after inspecting both, mark it as **[0o0o NEEDS CONFIRMATION]** and provide a single, specific question to resolve
  it. Do not invent APIs, schemas, filenames, or existing functions.

## 2) Recon Phase (must be explicit and verifiable)

Before writing the final plan, you must:

- Identify the **current architecture** relevant to this feature (entry points, modules, data flow).
- Locate the **exact files** likely involved (include paths).
- Confirm conventions from repo docs/configs (linFCs, lint rules, formatting, test framework).
- For every referenced existing file/symbol, ensure it actually exists in the repo; otherwise mark it as “new file” or **[0o0o NEEDS CONFIRMATION]**.

## 3) Plan Quality Bar (what “self-contained” means)

Your plan must include:

- Clear **Goal** and **Non-Goals**
- Concrete **Requirements** (functional + non-functional) extracted from the conversation
- **Assumptions** (explicit) and **Constraints** (from repo + conversation)
- **Impact map:** exhaustive list of impacted files/dirs, each with “why” and “change type” (edit/new/delete)
- **Step-by-step implementation sequence** with no ambiguity:
  - Each step includes: purpose, exact files to touch, specific edits (functions/classes/routes/schemas), and why
  - Include “gotchas” and invariants to preserve
  - Include any migrations, backfills, feature flags, config/env changes
- **Interfaces & contracts:** request/response shapes, events, DB schema, CLI args, etc. (as applicable)
- **Test plan:** exact tests to add/update, where they live, and commands to run
- **Verification checklist:** observable outcomes + how to validate locally/CI
- **Rollback / safety plan:** especially for migrations, prod-impacting changes, or risky refactors
- **Open questions:** only if truly blocking; each must be specific and minimal

## 4) “Fresh Eyes” Internal Reviews (do this silently, then reflect results)

Do two independent review passes _internally_ before finalizing:

- **Implementer review:** “Could I implement this without asking anything else?”
- **QA/release review:** “Are acceptance criteria testable? Are rollout/rollback covered?”
  In the final plan, include a short **Plan Completeness Audit** section listing what you checked (no chain-of-thought).

## 5) Required Markdown Structure (use these headings in order)

1. Title (`Plan: <Feature Name> ([feat_name])`)
2. One-paragraph Summary
3. Goals
4. Non-Goals
5. Requirements
6. Assumptions & Constraints
7. Current System Snapshot (relevant architecture + pointers)
8. Impacted Files & Directories (table)
9. Implementation Plan (numbered steps, each with: Files, Changes, Notes)
10. Data & Interface Contracts (if applicable)
11. Testing Plan
12. Verification Checklist
13. Rollout & Rollback
14. Plan Completeness Audit
15. Open Questions ([0o0o NEEDS CONFIRMATION] only)

## 6) Style Constraints

- Be **specific**: include concrete paths, identifiers, and commands.
- Prefer checklists and tables over prose.
- Avoid “should/might”; use imperative, testable statements.
- Do not reference “as discussed above”; this file must stand alone.

## Export

Export the plan to `./EXPORT/plan_[feat_name].md` following the contract above.

Thank you for being so diligent ☺️

<!-- Act as prompt engineer v21, meta prompt, ROUND 2 -->
