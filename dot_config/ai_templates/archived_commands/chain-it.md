---
description: chain-it Run a Pi subagent chain and write results into a feature folder
---

Use the `subagent` tool with the `chain` parameter.

The feature id is:
$ARGUMENTS

Follow these rules exactly:
- Treat `$ARGUMENTS` as the feature folder name, for example `feat-4321`.
- This workflow targets pi subagents.
- Set `chainDir` to `/Users/andy16/.local/share/chezmoi/docs/features/$ARGUMENTS` so relative outputs are written into that repository folder instead of a temporary artifact directory.
- In chain steps, only rely on supported Pi subagent variables: `{task}`, `{previous}`, and `{chain_dir}`.
- Do not use unsupported placeholders such as `{step_id}`.
- Because some agents may define default reads in frontmatter, set `reads: false` on any step that should not inherit them.
- After the chain finishes, confirm the files that were written.

Use this chain:

STEP 1
- Agent: `general`
- `reads: false`
- `output: opencode-config-summary.en.md`
- Task: tell me what I should know about `docs/features/opencode/opencode-configurations.md` in 2 to 3 sentences.

STEP 2
- Agent: `general`
- `reads: false`
- `output: opencode-config-summary.fr.md`
- Task: translate `{previous}` into French.

Execute it as a chain with `clarify: false`.