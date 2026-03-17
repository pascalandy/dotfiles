# Plan Review Pipeline Workflow

```mermaid
sequenceDiagram
    autonumber
    participant CEO
    participant PM as Product Manager (PM)
    participant R as Reviewer
    participant Plan as plan.md

    CEO->>PM: Share ideas <br>funds the project
    PM->>Plan: Create from docs/features/feat_template.md
    PM->>Plan: Second pass refinement
    
    Note over PM,R: Round 1 - Reviewer
    PM->>+R: Request review
    R->>Plan: Read plan
    R->>R: Create review-r1-{timestamp}-{suffix}.md
    R-->>-PM: Review complete
    
    PM->>PM: Read review-r1-*.md
    PM->>Plan: Update "Open Questions & Decisions" section<br/>and plan when appropriate
    PM->>PM: Delete review file
    Note right of PM: Commit using a subagent
    PM->>Plan: Commit plan update + review-file deletion
    
    PM-->>CEO: Plan ready for review
    
    Note over CEO,PM: CEO Review - Round 1
    CEO->>CEO: Create review-ceo-r1.md
    CEO->>PM: Review complete
    
    PM->>PM: Read review-ceo-r1.md
    PM->>Plan: Update "Open Questions & Decisions" section<br/>and plan when appropriate
    PM->>PM: Delete review file
    Note right of PM: Commit using a subagent
    PM->>Plan: Commit plan update + review-file deletion
    
    Note over PM,R: Round 2 - Reviewer
    PM->>+R: Request review
    R->>Plan: Read plan
    R->>R: Create review-r2-{timestamp}-{suffix}.md
    R-->>-PM: Review complete
    
    PM->>PM: Read review-r2-*.md
    PM->>Plan: Update "Open Questions & Decisions" section<br/>and plan when appropriate
    PM->>PM: Delete review file
    Note right of PM: Commit using a subagent
    PM->>Plan: Commit plan update + review-file deletion
    
    PM-->>CEO: Plan ready for review
    
    Note over CEO,PM: CEO Review - Round 2
    CEO->>CEO: Create review-ceo-r2.md
    CEO->>PM: Review complete
    
    PM->>PM: Read review-ceo-r2.md
    PM->>Plan: Update "Open Questions & Decisions" section<br/>and plan when appropriate
    PM->>PM: Delete review file
    Note right of PM: Commit using a subagent
    PM->>Plan: Commit plan update + review-file deletion
    
    PM-->>CEO: Final plan
    CEO->>CEO: Review decisions via git diff
    CEO->>PM: Approve plan
    Plan->>Plan: Plan is now deemed final
```

## File Structure

```
docs/features/
├── feat_template.md
└── feat-0004/
    ├── plan_agent-chain-review-artifact-recursive-feedback.md
    ├── workflow-diagram.md
    ├── review-r1-{timestamp}-{suffix}.md
    ├── review-ceo-r1.md
    ├── review-r2-{timestamp}-{suffix}.md
    └── review-ceo-r2.md
```

## Review File Naming Convention

| Reviewer | Pattern | Example |
|----------|---------|---------|
| Reviewer | `review-r{round}-{timestamp}-{suffix}.md` | `review-r1-2026-03-15_12h30_abc.md` |
| CEO | `review-ceo-r{round}.md` | `review-ceo-r1.md`, `review-ceo-r2.md` |
