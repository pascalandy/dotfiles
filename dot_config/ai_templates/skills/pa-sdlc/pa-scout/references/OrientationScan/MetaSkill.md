---
name: OrientationScan
description: Fast first-pass discovery of an unfamiliar repository, workspace, content system, project surface, knowledge base, or personal context. USE WHEN the user wants a quick orientation, broad first pass, or high-signal summary before deeper work.
---

# OrientationScan

## When To Use

Use this mode for the first pass over an unfamiliar system when the main question is broad:

- What is this thing?
- Who uses it?
- How is it organized?
- Where should I look first?

This is the default Scout mode when breadth matters more than depth.

This mode should feel like a situational brief, not a training document.

## Core Method

1. Identify the subject type from visible evidence.
2. Read the highest-signal artifacts first.
3. Build a lightweight structure map.
4. Surface conventions, dependencies, and unknowns.
5. End with the best next scout step.

## Subject Adaptation Rules

- For code repositories, prioritize manifests, top-level docs, config, entry points, and structure.
- For content systems, prioritize editorial models, page hierarchy, templates, publishing docs, and governance artifacts.
- For PM workspaces, prioritize board structure, status definitions, templates, ownership rules, and recurring artifacts.
- For knowledge systems, prioritize indexes, maps, naming conventions, folders, tags, and linkage patterns.

## Workflow

1. Detect the subject type.
2. Find the top-level organizing artifacts.
3. Read only the highest-signal sources required to answer the broad questions.
4. Produce a concise system summary grounded in evidence.
5. Highlight the most useful next area for deeper inquiry.

## Output Format

Produce a concise scout brief with these sections:

1. `What This Is`
2. `Who It Serves`
3. `How It Is Organized`
4. `Key Entry Points`
5. `Conventions And Patterns`
6. `Evidence`
7. `Unknowns`
8. `Recommended Next Scout Step`

## Examples

- "What is this repo and where should I start?"
- "Give me a first-pass map of this workspace."

## Boundaries

- Do not read everything.
- Do not produce a full onboarding artifact unless the user asks for one.
- Do not optimize for teaching a newcomer step by step; that belongs to `StructuredOnboarding`.
- Do not drift into planning or implementation advice.
