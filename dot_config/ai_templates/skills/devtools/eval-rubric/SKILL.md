---
name: eval-rubric
description: Structured scoring rubric for evaluating artifacts against acceptance criteria. Use when reviewing, scoring, or doing due diligence on any artifact with defined criteria.
---

# Skill: Eval Rubric

When evaluating an artifact against acceptance criteria, judge one criterion at a time. Only inspect the final observable result. Do not reward hidden reasoning, effort, or intent.

## Rating System

| Score | Label                 | Meaning                                                                                                  | Final answer |
| ----- | --------------------- | -------------------------------------------------------------------------------------------------------- | ------------ |
| 4     | Strong pass           | Clearly meets the criterion with strong observable evidence                                              | yes          |
| 3     | Pass                  | Meets the criterion; only minor non-material issues are allowed                                          | yes          |
| 2     | Insufficient evidence | The criterion is not clearly met, or the final artifact provides partial, ambiguous, or missing evidence | no           |
| 1     | Clear fail            | Clearly does not meet the criterion                                                                      | no           |
| 0     | Not applicable        | The criterion cannot be judged from the final artifact or does not apply to this context                 | skip         |

## Evaluation Logic

For each criterion:

1. Does this criterion apply to this artifact? If not applicable or cannot be judged → `0` (skip).
2. Does the artifact clearly fail this criterion? If yes → `1`.
3. Is evidence partial, ambiguous, or missing? If yes → `2`.
4. Does it meet the criterion with only minor non-material issues? → `3`.
5. Does it meet the criterion with strong, clean evidence? → `4`.

## Output Format

For each criterion, produce exactly:

- **Score**: `0`-`4`
- **Decision**: `yes`, `no`, or `n/a`
- **Justification**: One sentence citing observable evidence from the artifact (or why the criterion does not apply).

## Key Design Rules

- The binary decision is the real output. The numeric score is a structured judgment that feeds that decision.
- The important threshold is `2` vs `3`.
- `3` = "it passes, stop arguing." `4` = "it passes cleanly and convincingly." Both map to `yes`. This prevents withholding top scores for unimportant reasons and avoids unnecessary retry loops.
- `3` should be the normal passing score. Do not make `4` mandatory.
- `2` is a strict fail. Borderline must not sneak through.
- `0` means "not applicable" -- the criterion is excluded from the pass/fail tally entirely. It does not count as a failure.
- Hard blockers should be metadata on the criterion, not part of the score itself. If a blocker gets `no`, the whole artifact fails.
- Never average scores across criteria. The decision is per-criterion: count pass/fail, do not blend. Criteria scored `0` are excluded from the count.
