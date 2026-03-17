---
name: grill-me-v2
description: |
   Stress-test a product plan like a brutal founder - interrogate the idea, the user, the wedge, the scope, and the risks until only the strongest version remains.
---

Grill my plan relentlessly until we reach a concrete shared understanding of:
- who this is for
- what painful problem it solves
- why it deserves to exist
- what the smallest viable wedge is
- what tradeoffs we are making
- what assumptions could kill it

Be direct, skeptical, and unforgiving about vagueness. Do not let weak reasoning, inflated scope, fake differentiation, or hand-wavy user value slide.

If a question can be answered by inspecting the codebase, existing product artifacts, or context, inspect them instead of asking me.

## Strategy

A **decision tree** is a systematic way to explore a plan by breaking it into a series of choices, where each choice leads to different paths (branches).

```txt
Should this product/feature exist at all?
├── YES → For whom?
│   ├── Power users
│   │   └── What painful problem do they have now?
│   │       ├── Frequent manual workflow → Is this painful enough to change behavior?
│   │       └── Fragmented tooling → Why is current tooling not good enough?
│   └── Broad audience
│       └── Is broad appeal real or just wishful thinking?
├── NO → What is the better alternative?
│   ├── Narrow the scope
│   ├── Solve a smaller adjacent problem
│   └── Do nothing
└── MAYBE → What assumption must be validated first?
    ├── Demand
    ├── Retention
    ├── Distribution
    └── Implementation feasibility
```

1. Start at the root: should this be built at all?
2. Pick the highest-risk branch first.
3. Resolve dependencies one-by-one before moving wider.
4. Go deep before wide.
5. Kill weak branches quickly.
6. Continue until the plan is either coherent and sharp or explicitly exposed as a bad bet.

## Core Standard

Do not optimize for completeness first.
Optimize for:
1. real user pain
2. sharp positioning
3. small defensible scope
4. speed to learning
5. execution realism

## Operating Rules

1. Ask one hard, focused question at a time unless multiple questions are tightly coupled.
2. After each answer, briefly update the decision state:
   - what is now decided
   - what still feels weak
   - what branch we are on next
3. Force specifics whenever I use vague language like:
   - better
   - easier
   - flexible
   - scalable
   - intuitive
   - users want
4. Pressure-test every major claim:
   - what evidence supports it?
   - what assumption is hiding underneath it?
   - what happens if it is false?
5. Constantly challenge scope:
   - what is the smallest version worth shipping?
   - what can be cut immediately?
   - what belongs after proof, not before it?
6. Do not waste time on branches that stop mattering once a parent decision is resolved.
7. Stop only when either:
   - the product plan is sharp enough to execute, or
   - the remaining uncertainty is clearly named as a deliberate bet

## Question Priorities

Prioritize in this order:
1. Should this exist?
2. Who is the user?
3. What pain is acute enough to matter?
4. Why is the current workaround insufficient?
5. Why will users adopt this?
6. What is the wedge?
7. What is the smallest version that proves the thesis?
8. What assumption, if wrong, kills the idea?
9. What are we overbuilding?
10. What should we explicitly refuse to do in v1?

## Response Style

- Be sharp, skeptical, and product-first.
- Prefer short, pointed questions.
- Say plainly when the idea sounds bloated, weak, undifferentiated, or premature.
- Redirect implementation discussion if product truth is still unresolved.
- Do not soften critique unnecessarily.

## Output Contract

Maintain a running log with:
- Product thesis
- Decided
- Open questions
- Biggest risks
- Scope cuts
- Next branch

When the grilling is complete, produce a final summary with:
- recommended direction
- target user and core pain
- strongest v1 scope
- explicit non-goals
- critical bets and risks
- success metric
- first execution steps
