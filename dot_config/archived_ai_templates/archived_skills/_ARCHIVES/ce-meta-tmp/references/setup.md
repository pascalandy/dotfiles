# Compound Engineering Setup

> Configure project-level settings for compound-engineering workflows.

## When to Use

- A user explicitly invokes the setup skill to configure compound-engineering for their project
- A user asks how to configure review agents or project-level compound-engineering settings

## Inputs

None required.

## Methodology

### Current State

Review agent selection is handled automatically by the `ce:review` skill, which uses intelligent tiered selection based on diff content. No per-project configuration is needed for code reviews.

When this skill is invoked, inform the user:

> Review agent configuration is no longer needed — `ce:review` automatically selects the right reviewers based on your diff. Project-specific review context (e.g., "we serve 10k req/s" or "watch for N+1 queries") belongs in your project's `CLAUDE.md` or `AGENTS.md`, where all agents already read it.

### Future Use

This skill is reserved for future project-level configuration needs beyond review agent selection.

## Quality Gates

- User understands that no manual review agent configuration is required
- User is directed to `CLAUDE.md` / `AGENTS.md` for project-specific context

## Outputs

An informational message directing the user to the correct configuration approach.

## Feeds Into

- `ce:review` (reads `CLAUDE.md` / `AGENTS.md` automatically for project context)
