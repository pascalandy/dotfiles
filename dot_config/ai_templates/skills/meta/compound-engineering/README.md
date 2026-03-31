# Compound Engineering

`compound-engineering` is a hierarchical meta-skill: one user-facing entry point, one minimal router, and three lifecycle specialists.

## What It Does

Users describe the work they need in natural language. The collection routes the request to the right specialist automatically:

1. `ShapeWork` for discovery, requirements, planning, and architectural direction
2. `ExecuteWork` for implementation, focused builders, and delivery mechanics
3. `VerifyAndCompound` for review, QA, feedback resolution, and durable documentation

## Structure

```text
compound-engineering/
├── SKILL.md
├── README.md
└── references/
    ├── ROUTER.md
    ├── ShapeWork/
    │   ├── SKILL.md
    │   └── workflows/
    ├── ExecuteWork/
    │   ├── SKILL.md
    │   └── workflows/
    ├── VerifyAndCompound/
    │   ├── SKILL.md
    │   └── workflows/
    └── <bundled specialist skills used by those workflows>
```

## Routing Model

The collection follows progressive disclosure:

1. Load `SKILL.md` for the user-facing overview.
2. Load `references/ROUTER.md` to choose the lifecycle specialist.
3. Load the selected specialist's `SKILL.md`.
4. Load the workflow file that picks the narrowest bundled skill for the request.

## Included Specialists

| Specialist | Owns | Workflows |
|---|---|---|
| `ShapeWork` | Discovery, requirements, planning, architecture | `DiscoverDirection`, `DesignTheApproach`, `ChooseSpecializedPatterns` |
| `ExecuteWork` | Implementation, focused builders, delivery mechanics | `ImplementFromPlan`, `UseFocusedBuilders`, `ManageDelivery` |
| `VerifyAndCompound` | Review, QA, feedback resolution, changelogs, learnings | `ReviewAndValidate`, `ResolveFeedbackAndTrack`, `CaptureAndShare` |

## Portability Rules

- Uses only relative file references inside this folder.
- Does not assume a specific assistant, harness, or installation path.
- Keeps routing logic isolated in `references/ROUTER.md`.
- Lets each sub-skill work standalone if loaded directly.

## Maintenance

To add a new lifecycle specialist:

1. Create `references/<NewMode>/SKILL.md`
2. Add its workflow files under `references/<NewMode>/workflows/`
3. Add one new row in `references/ROUTER.md`
4. Update `SKILL.md` so the collection docs stay accurate
