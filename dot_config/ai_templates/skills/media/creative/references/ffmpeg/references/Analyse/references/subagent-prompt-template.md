# Sub-Agent Prompt Template

Use this prompt verbatim when spawning a frame-reading sub-agent, substituting the placeholders in `{curly_braces}`.

## Prompt

```
You are analysing frames extracted from a video file.

VIDEO: {filename}
DURATION: {duration}
BATCH: {batch_number} of {total_batches}

Read each frame image listed below using the Read tool (or equivalent file reading
tool that supports images). For each frame, write a structured description.

FRAMES:
{for each frame in batch}
- {absolute_path_to_frame} (timestamp: {MM:SS})
{end for}

For each frame, describe:
1. SCENE: What is visible (layout, UI elements, environment)
2. CONTENT: Text, code, labels, menus, or dialogue visible on screen
3. ACTION: What is happening or has changed since the likely previous frame
4. DETAILS: Any notable specifics (error messages, URLs, file names, button states)

After describing all frames, add a BATCH SUMMARY section with:
- Content type (one of: Screencast, Presentation, Tutorial, Footage, Animation)
- Key events in this batch's time range
- Any text/prompts/commands the user typed (quote exactly)

Write the complete analysis to: {TMPDIR}/batch_{N}_analysis.md

Format the output file as:

# Batch {N} Analysis ({start_timestamp} - {end_timestamp})

## Frame-by-Frame

### Frame {sequence} ({timestamp})
- **Scene**: ...
- **Content**: ...
- **Action**: ...
- **Details**: ...

(repeat for each frame)

## Batch Summary
- **Content Type**: ...
- **Key Events**: ...
- **Quoted Text/Prompts**: ...
```

## Placeholder Values

| Placeholder | Source |
|---|---|
| `{filename}` | The video file name (not full path) |
| `{duration}` | Human-readable (e.g. `4:32`) from ffprobe |
| `{batch_number}` | 1, 2, 3, ... |
| `{total_batches}` | Total batch count from manifest |
| `{absolute_path_to_frame}` | Full path from `$TMPDIR/frame_NNNN.jpg` |
| `{MM:SS}` | Timestamp calculated from frame sequence + extraction rate |
| `{TMPDIR}` | The absolute path to the scratch dir |
| `{N}` | Batch number (matches `{batch_number}`) |
| `{start_timestamp}` | First frame's timestamp in the batch |
| `{end_timestamp}` | Last frame's timestamp in the batch |

## Why This Exact Format Matters

- The **structured frame fields** (Scene / Content / Action / Details) force the sub-agent to separate observation from interpretation
- The **BATCH SUMMARY with Content Type** lets the synthesis workflow aggregate easily
- The **"Quoted Text/Prompts"** field captures anything the viewer typed — critical for tutorial and screencast understanding
- Writing to a **predictable file path** (`batch_N_analysis.md`) lets the main agent glob the results without extra coordination
