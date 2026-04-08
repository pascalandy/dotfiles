# 03 — Delegate Frame Analysis to Sub-Agents

**This is the critical context-saving step.** Do NOT read frame images in the main conversation. Instead, split frames into batches and delegate each batch to a sub-agent. Each sub-agent loads the images into its disposable context, writes a text analysis file, and terminates — the image content never enters the main context.

## Step 1: Prepare Batch Manifest

Split the extracted frame file list into batches of **8-10 frames each**. For each batch, record:

- Batch number (1, 2, 3, ...)
- Frame file paths (absolute)
- Frame timestamps (calculated in previous workflow)
- Output file path: `$TMPDIR/batch_N_analysis.md`

## Step 2: Spawn Sub-Agents

For each batch, spawn a sub-agent with the prompt from `../references/subagent-prompt-template.md`.

**Launch all batches in parallel where the harness supports it.** The batches are fully independent with no shared state.

## Step 3: Collect Results

After all sub-agents complete, read only the text analysis files. These are lightweight markdown — no images enter the main context.

```bash
ls "$TMPDIR"/batch_*_analysis.md
```

Read each `batch_N_analysis.md` file **in order**. Typical file sizes are 2-5 KB each.

## Harness-Agnostic Notes

Your harness may call the delegation mechanism something different. What matters is that each sub-agent can:

1. **Read image files** (the frame JPEGs)
2. **Write a text file** (the batch analysis markdown)

### If your harness has no sub-agent mechanism

Fall back to reading frames directly in the main context, but:

- Limit to **20 frames maximum**
- Warn the user about context usage ("Reading frames inline — this will consume significant context. For longer videos, a harness with sub-agent support is recommended.")
- Produce the same batch_N_analysis.md output format so the synthesis workflow still works

## Error Handling

| Problem | Mitigation |
|---|---|
| Sub-agent times out on a batch | Re-spawn for just that batch; if it times out twice, read the batch inline as a fallback |
| Sub-agent returns empty file | Spawn a replacement with a direct file-write instruction |
| A frame file fails to read | Sub-agent should note a gap in the batch file and continue with the rest |
| Wildcard batch-id collision on re-run | Use fresh `$TMPDIR` per invocation (already timestamped) |

## Next

Move to `workflows/04-synthesise.md` with all batch_N_analysis.md files collected.
