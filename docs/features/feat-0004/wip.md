## Summary: Agent Chain Review Pipeline

### Problem

Current workflow stores reviewer feedback inline inside the plan. Over multiple rounds:
- Temporary critique mixes with durable decisions
- Same ideas resurface repeatedly
- No clear separation between "what was considered" and "what was decided"

### Solution

A deterministic review pipeline with clear separation of concerns:

| Aspect | Before | After |
|--------|--------|-------|
| Reviewer output | Inline in plan | Standalone review file |
| Who edits plan | Anyone | PM only |
| Review files | N/A | Created, then deleted after consolidation |
| Decision log | Mixed with feedback | Dedicated "Open Questions & Decisions" section |

### Key Principles

1. **Single source of truth** — The plan file is the only durable memory
2. **Reviewers don't touch the plan** — They create review files only
3. **PM is the gatekeeper** — Sole role that mutates the plan
4. **Audit trail** — Git history preserves review-file creation and deletion
5. **Deterministic processing** — Files processed in lexicographic order

### Workflow

docs/features/feat-0004/workflow-diagram.md

### File Structure

```
docs/features/feat-0004/
├── plan_*.md                              # Durable artifact
├── workflow-diagram.md
├── review-a-r1-{timestamp}-{suffix}.md    # Reviewer A, round 1
├── review-b-r1-{timestamp}-{suffix}.md    # Reviewer B, round 1
├── review-ceo-r1.md                        # CEO, round 1
├── review-c-r2-{timestamp}-{suffix}.md    # Reviewer C, round 2
└── review-ceo-r2.md                        # CEO, round 2

docs/features/feat_template.md
```

### What We Need Reviewed

1. Does the separation of concerns make sense?
2. Is the file naming convention clear and scalable?
3. Any gaps in the workflow?
4. Should review files be deleted after consolidation?
