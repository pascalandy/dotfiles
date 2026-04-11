---
name: ChangeApplication
description: Default implementation mode for applying a bounded change through demonstrable vertical slices. USE WHEN the work is ready to execute, one first slice can be named clearly, and the change should be carried out with TDD by default for behavior-bearing software work or with an equivalent proof-first slice discipline in non-software contexts.
---

# ChangeApplication

## Purpose

Apply a bounded change by finishing one demonstrable slice at a time.

This is the default Implement mode. It owns normal execution once the work is ready.

## Core Method

Use this default sequence:

1. Confirm the execution boundary.
2. Define the smallest user-recognizable slice.
3. Choose the proof mechanism for that slice.
4. Build only what the slice needs across every relevant layer.
5. Verify the slice end to end.
6. Checkpoint before starting the next slice.

## Completion Loops

`ChangeApplication` owns the finish-the-change loops that are still part of bounded implementation:

1. targeted review when the slice needs defect-finding or requirement-completeness checks
2. targeted QA or hardening when the slice needs stronger proof before it is credibly done
3. bounded review-feedback follow-through when external comments require another implementation pass

These are part of implementation when they stay tied to the current bounded change. They are not separate open-ended review campaigns.

## Default Posture

For behavior-bearing software work, default to `TDD`:

1. write one failing test for one behavior
2. write the minimal implementation to pass it
3. refactor only after green

Use integration-style tests through public interfaces whenever possible.

For non-software work, preserve the same proof-first posture:

1. define one demonstrable outcome
2. build the thinnest end-to-end path that makes it real
3. verify it in a way a stakeholder would recognize
4. checkpoint before expanding

## Vertical Slice Rules

1. One slice equals one user-recognizable outcome.
2. Slice 1 must touch every relevant layer the final system will touch.
3. Order slices by risk and unknowns, not by layer dependency.
4. Build for slice N, not slice N+2.
5. Do not create speculative scaffolding for future slices.
6. Do not polish one layer before the end-to-end path exists.

## Execution Checks

Before starting a slice:

1. Can the slice be named as an outcome rather than a component?
2. Will this slice be runnable, readable, or otherwise demonstrable on its own?
3. Does it touch every relevant layer, even if some parts are stubbed?

Before declaring a slice done:

1. Was it actually run or otherwise observed end to end?
2. Could a non-expert recognize what changed?
3. Could this slice be kept or reverted without leaving the system broken?
4. Does the output contain only what this slice needs?

## Output Contract

For any structured artifact, use this exact shape. For a very small request, compress the same six anchors into prose without renaming them:

1. `Requested Change Or Problem`
2. `Execution Boundary`
3. `Work Performed Or Planned`
   Include `Current Slice`, `Proof Mechanism`, and `Work Applied` here.
4. `Verification Performed`
5. `Risks Or Unresolved Items`
6. `Recommended Next Phase`

## Handoffs

- Hand off to `pa-scope` when the change surface is still unclear.
- Hand off to `pa-scout` when broad orientation is still missing.
- Hand off to `pa-vision` when the desired outcome or value is still unsettled.
- Hand off to `pa-architect` when execution structure is still unresolved.
- Hand off to `RootCauseRepair` when the real job is debugging a failure rather than applying a planned change.

## Non-Goals

Do not treat these as primary ownership here:

- broad discovery
- scope mapping
- product direction
- plan design
- generalized QA or review sweeps beyond the current bounded change
- PR-thread management that is not directly tied to the current implementation pass
