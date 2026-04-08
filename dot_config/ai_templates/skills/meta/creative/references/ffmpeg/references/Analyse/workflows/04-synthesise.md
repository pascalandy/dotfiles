# 04 — Synthesise Final Output

Using only the text from the batch analysis files, perform synthesis in the main context and produce the final user-facing report.

## Synthesis Steps

1. **Merge frame descriptions** into a single chronological timeline
2. **Group frames** into natural segments (same scene, slide, or screen)
3. **Detect dominant content type** across all batches
4. **Identify 3-7 key moments** — the highest-information-density frames
5. **Extract quoted text** — any prompts, commands, or dialogue the user typed/spoke
6. **Write a 2-5 sentence narrative summary**

## Content Type Detection

From the sub-agent batch reports' "Content Type" line, pick the dominant type:

| Type | Signals |
|---|---|
| **Screencast** | UI elements, terminal windows, code editors, cursor movement |
| **Presentation** | Slides, bullet lists, minimal motion, static backgrounds |
| **Tutorial** | Narration over screencast or presentation, step-by-step structure |
| **Footage** | Real-world scenes, camera motion, no UI elements |
| **Animation** | Motion graphics, character animation, non-photographic style |

If batches disagree, report the most common type and note the minority.

## Output Format

```markdown
# Video Analysis: [filename]

## Metadata
| Property | Value |
|---|---|
| Duration | M:SS |
| Resolution | WxH |
| FPS | N |
| Content Type | [detected] |
| Frames Analysed | N |

## Timeline
### [Segment Title] (M:SS - M:SS)
Description of what happens in this segment.

### [Segment Title] (M:SS - M:SS)
Description of what happens in this segment.

## Key Moments
1. **[M:SS] Title**: Description
2. **[M:SS] Title**: Description
3. **[M:SS] Title**: Description

## Summary
[2-5 sentence narrative paragraph summarising the entire video]
```

## Segment Identification Heuristics

- **Screen transitions** — look for "scene change" or "new window" in batch reports
- **Topic changes** — look for different headlines, titles, or code files
- **Time gaps** — segments rarely exceed 60-90s; split if one would
- **Content type shifts** — presentation → demo → presentation is two or three segments

Aim for 3-8 segments for a typical 5-20 minute video. More than 10 means you're segmenting too finely.

## Key Moments vs Timeline Segments

- **Timeline segments** describe *what happens in each phase* — continuous narrative
- **Key moments** highlight *the most important individual frames* — the "aha" points a viewer would want to jump to

A 10-minute tutorial might have 5 timeline segments but 7 key moments if there are several critical code-on-screen frames within the same segment.

## After Delivering the Report

Go to the cleanup section of `../SKILL.md` — remove `$TMPDIR` unless the user asked to keep the frames.
