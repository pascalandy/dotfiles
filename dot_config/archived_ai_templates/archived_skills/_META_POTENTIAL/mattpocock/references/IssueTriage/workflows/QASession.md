# QASession

Run an interactive QA session. The user describes problems conversationally while the agent clarifies, explores the codebase for context, and files durable GitHub issues.

## Process

### For Each Issue the User Raises

#### 1. Listen and Lightly Clarify

At most 2-3 short clarifying questions. Do not over-interview. Focus on:
- What they expected vs what actually happened
- Steps to reproduce (if not obvious)
- Whether it is consistent or intermittent

#### 2. Explore the Codebase in the Background

Explore to:
- Learn the domain language used in that area (check `UBIQUITOUS_LANGUAGE.md` if it exists)
- Understand the feature's intended behavior
- Identify the user-facing behavior boundary

Do NOT explore to find a fix. The purpose is context for writing a good issue, not diagnosis.

#### 3. Assess Scope: Single Issue or Breakdown?

**Break down when:**
- Fix spans multiple independent areas (e.g., "the form validation is wrong AND the success message is missing AND the redirect is broken")
- Clearly separable concerns
- Multiple distinct failure modes

**Keep single when:**
- One behavior is wrong in one place
- Symptoms trace to the same root cause

#### 4. File the GitHub Issue(s)

Create with `gh issue create`. Do not ask the user to review first -- file directly.

**Single issue template:**
```markdown
## What Happened
[Describe the actual behavior the user experienced, in plain language]

## What I Expected
[Expected behavior]

## Steps to Reproduce
1. [Step]
2. [Step]
3. Observe: [what goes wrong]

## Additional Context
[Domain context from codebase exploration]
```

**Breakdown template (for each child issue):**
```markdown
**Parent issue:** #<number>

## What's Wrong (This Slice Only)
[One specific behavior]

## What I Expected
[Expected behavior]

## Steps to Reproduce
1. [Step]
2. [Step]

## Blocked By
- #<number>
- Or "None -- can start immediately"

## Additional Context
[Domain context]
```

#### Rules for All Issues

- No file paths or line numbers
- Use the project's domain language (check `UBIQUITOUS_LANGUAGE.md` if it exists)
- Describe behaviors, not code
- Reproduction steps are mandatory
- Keep concise

#### Rules for Breakdowns

- Prefer many thin issues over few thick ones
- Mark blocking relationships honestly
- Create issues in dependency order so you can reference real issue numbers
- Maximize parallelism -- the goal is that multiple people (or agents) can grab different issues simultaneously

#### 5. Continue the Session

After filing, print all issue URLs (with blocking relationships summarized) and ask: "Next issue, or are we done?"

Each issue is independent -- do not batch them.
