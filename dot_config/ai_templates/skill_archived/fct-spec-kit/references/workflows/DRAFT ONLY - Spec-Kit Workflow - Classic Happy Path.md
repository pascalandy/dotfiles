# Spec-Kit Workflow - Classic Happy Path

```mermaid
---
title: Spec-Kit Workflow - Classic Happy Path
---

sequenceDiagram
    autonumber

    participant P as Pascal
    participant AI as Main AI Assistant
    participant EXT as External Review
    participant REPO as Repository

    Note over P,REPO: Phase 1: Specification

    P->>AI: "New feature idea: [description]"
    AI->>AI: Load skill spec-kit
    AI->>P: "Let me create a spec for this feature"

    AI->>REPO: /speckit.specify
    Note over REPO: Creates specs/###-feature/<br/>spec.md + checklist
    REPO-->>AI: spec.md generated

    AI->>P: "Spec ready. Checkpoint suggested for review."
    P->>AI: "Yes, let's do external review"

    AI->>EXT: Export context for review
    Note over EXT: Fresh context validates:<br/>- Completeness<br/>- Clarity<br/>- Scope
    EXT-->>AI: "Spec validated, proceed"

    Note over P,REPO: Phase 2: Planning

    P->>AI: "Create the technical plan"
    AI->>REPO: /speckit.plan
    Note over REPO: Creates plan.md +<br/>artifacts (data-model, contracts...)
    REPO-->>AI: plan.md generated

    AI->>P: "Plan ready. Checkpoint suggested."
    P->>AI: "Review the architecture choices"

    AI->>EXT: Export plan for review
    Note over EXT: Validates:<br/>- Tech choices<br/>- Scalability<br/>- Risks mitigated
    EXT-->>AI: "Plan approved"

    Note over P,REPO: Phase 3: Task Generation

    P->>AI: "Generate the tasks"
    AI->>REPO: /speckit.tasks
    Note over REPO: Creates tasks.md with<br/>ordered, parallelizable items
    REPO-->>AI: tasks.md generated

    AI->>P: "Tasks ready. Review granularity?"
    P->>AI: "Looks good, proceed"

    Note over P,REPO: Phase 4: Implementation

    P->>AI: "Implement the tasks"

    loop For each task
        AI->>REPO: /speckit.implement
        Note over REPO: Code modifications<br/>following plan
        REPO-->>AI: Task completed
        AI->>P: "Task X done, moving to next"
    end

    AI->>P: "All tasks implemented. Feature complete."

    Note over P,P: Feature delivered following SDD workflow
```

## Participants

| Participant       | Role                                                               |
| ----------------- | ------------------------------------------------------------------ |
| Pascal            | Human stakeholder driving the feature                              |
| Main AI Assistant | Orchestrates SDD workflow, executes /speckit.\* commands           |
| External Review   | Fresh context (new session/other AI) for validation at checkpoints |
| Repository        | Storage for all artifacts (specs/, plan.md, tasks.md, code)        |

## Phases

1. **Specification**: Idea becomes structured spec with acceptance criteria
2. **Planning**: Technical decisions, architecture, artifacts
3. **Task Generation**: Breakdown into executable work items
4. **Implementation**: Code generation following the plan
