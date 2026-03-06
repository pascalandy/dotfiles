# Agent Reference

Doc for the user (not for the agent)

## Agent Tiers

```
A-tier MAIN      High-capability agents for complex work
A-tier ESCALATE  Extended reasoning for hard problems (use after 2 failures)
B-tier MAIN      Standard agents for exploration and quick tasks
B-tier FALLBACK  General-purpose fallback
C-tier MAIN      Verification and testing specialists
```

## Quick Reference

### When to use `@build`
- Task planning and orchestration
- Frontend/UI design and visual layout
- As fallback for most A-tier tasks

### When to use `@abby`
- Implementation: features, bugs, architecture
- Multi-file refactoring
- Code review (can run parallel with @build)
- Security review
- Documentation and specs
- Performance work

### When to use `@explore`
- Deep codebase exploration
- Repo mapping
- Comprehensive search across large codebases

### When to use `@ben`
- Quick codebase exploration
- Doc search
- Quick edits
- Deep-research Q&A

### When to use `@charlie`
- Writing tests
- Running tests
- QA validation
- Visual checks

### When to use `@oracle`
- ONLY after 2 failed attempts with `@abby` or `@build`
- Extended reasoning for exceptionally hard problems

### When to use `@general`
- Fallback for everything else
- When primary agents are unavailable

### When to use `@carole`
- Fallback for `@charlie` when unavailable

## YAML Reference

```yaml
agent_selection:
  - task: planning tasks, orchestrating
    agents: ["@build"]
    tier: "A-tier MAIN"
    fallback: ["@abby"]
  - task: coding, architecture, multi-file refactoring, bugs
    agents: ["@abby"]
    tier: "A-tier MAIN"
    fallback: ["@build"]
  - task: code review
    agents: ["@abby", "@build"]
    mode: "parallel"
    tier: "A-tier MAIN"
    fallback: ["@build"]
  - task: security review
    agents: ["@abby"]
    tier: "A-tier MAIN"
    fallback: ["@build"]
  - task: frontend/UI design, visual layout
    agents: ["@build"]
    tier: "A-tier MAIN"
    fallback: ["@abby"]
  - task: documentation/spec/changelog writing
    agents: ["@abby"]
    tier: "A-tier MAIN"
    fallback: ["@build"]
  - task: performance profiling, benchmark validation
    agents: ["@abby"]
    tier: "A-tier MAIN"
    fallback: ["@build"]
  - task: deep codebase exploration, repo mapping
    agents: ["@explore"]
    tier: "B-tier MAIN"
    fallback: ["@ben"]
  - task: codebase exploration, doc search, quick edits, deep-research Q&A
    agents: ["@ben"]
    tier: "B-tier MAIN"
    fallback: ["@general"]
  - task: tests, QA, validation, visual checks
    agents: ["@charlie"]
    tier: "C-tier MAIN"
    fallback: ["@carole"]
  - task: after 2 failed attempts (from @abby or @build)
    agents: ["@oracle"]
    tier: "A-tier ESCALATE"
    fallback: ["@build"]
  - task: everything else
    agents: ["@general"]
    tier: "B-tier FALLBACK"
    fallback: ["@build"]
```
