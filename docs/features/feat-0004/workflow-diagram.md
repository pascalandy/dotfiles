# Plan Review Pipeline Workflow

```mermaid
sequenceDiagram
    autonumber
    participant CEO
    participant PM as Product Manager
    participant RA as Reviewer A
    participant RB as Reviewer B
    participant RC as Reviewer C
    participant Plan as plan.md

    CEO->>PM: Share idea
    PM->>Plan: Create from docs/features/feat_template.md
    PM->>Plan: Second pass refinement
    
    Note over PM,RA: Round 1 - Reviewer A
    PM->>+RA: Request review
    RA->>Plan: Read plan
    RA->>RA: Create review-a-r1-{timestamp}-{suffix}.md
    RA-->>-PM: Review complete
    
    PM->>PM: Read review-a-r1-*.md
    PM->>Plan: Update "Open Questions & Decisions" section<br/>and plan when appropriate
    PM->>PM: Commit changes
    PM->>PM: Clear review file, sign "Plan updated [date/time]"
    
    Note over PM,RB: Round 1 - Reviewer B
    PM->>+RB: Request review
    RB->>Plan: Read plan
    RB->>RB: Create review-b-r1-{timestamp}-{suffix}.md
    RB-->>-PM: Review complete
    
    PM->>PM: Read review-b-r1-*.md
    PM->>Plan: Update "Open Questions & Decisions" section<br/>and plan when appropriate
    PM->>PM: Commit changes
    PM->>PM: Clear review file, sign "Plan updated [date/time]"
    
    PM-->>CEO: Plan ready for review
    
    Note over CEO,PM: CEO Review - Round 1
    CEO->>CEO: Create review-ceo-r1.md
    CEO->>PM: Review complete
    
    PM->>PM: Read review-ceo-r1.md
    PM->>Plan: Update "Open Questions & Decisions" section<br/>and plan when appropriate
    PM->>PM: Commit changes
    PM->>PM: Clear review file, sign "Plan updated [date/time]"
    
    Note over PM,RC: Round 2 - Reviewer C
    PM->>+RC: Request review
    RC->>Plan: Read plan
    RC->>RC: Create review-c-r2-{timestamp}-{suffix}.md
    RC-->>-PM: Review complete
    
    PM->>PM: Read review-c-r2-*.md
    PM->>Plan: Update "Open Questions & Decisions" section<br/>and plan when appropriate
    PM->>PM: Commit changes
    PM->>PM: Clear review file, sign "Plan updated [date/time]"
    
    PM-->>CEO: Plan ready for review
    
    Note over CEO,PM: CEO Review - Round 2
    CEO->>CEO: Create review-ceo-r2.md
    CEO->>PM: Review complete
    
    PM->>PM: Read review-ceo-r2.md
    PM->>Plan: Update "Open Questions & Decisions" section<br/>and plan when appropriate
    PM->>PM: Commit changes
    PM->>PM: Clear review file, sign "Plan updated [date/time]"
    
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
    ├── review-a-r1-{timestamp}-{suffix}.md
    ├── review-b-r1-{timestamp}-{suffix}.md
    ├── review-ceo-r1.md
    ├── review-c-r2-{timestamp}-{suffix}.md
    ├── review-ceo-r2.md
    └── workflow-diagram.md
```

## Review File Naming Convention

| Reviewer | Pattern | Example |
|----------|---------|---------|
| Reviewer A | `review-a-r{round}-{timestamp}-{suffix}.md` | `review-a-r1-2026-03-15_12h30_abc.md` |
| Reviewer B | `review-b-r{round}-{timestamp}-{suffix}.md` | `review-b-r1-2026-03-15_14h00_xyz.md` |
| Reviewer C | `review-c-r{round}-{timestamp}-{suffix}.md` | `review-c-r2-2026-03-15_16h30_def.md` |
| CEO | `review-ceo-r{round}.md` | `review-ceo-r1.md`, `review-ceo-r2.md` |
