# First impression — five delegation / headless skills

Five skills. Three are CLI primitives (`headless-claude`, `headless-codex`, `headless-opencode`). Two are orchestration layers (`delegate`, `delegate-claude`). Each does one thing well, but the set has friction.

## The primitives

The `headless-*` trio is symmetric: one reference card per CLI. They document *how* to invoke each CLI in non-interactive mode. Clean, useful standalone, reference-only, no opinions. Nothing to fix here.

## The delegate pair does two different things

Despite the shared prefix, these skills are not variants of one idea:

- `delegate` is an **OpenCode sub-agent routing matrix**. Main agent `1-kimi` spawns numbered sub-agents for review passes (2/3/4-pass). It is a task-routing dispatcher.
- `delegate-claude` is a **CLI-agnostic executor→advisor pattern**. The current CLI — any CLI — consults Claude Opus for strategic guidance via `claude -p`. It is a client-side simulation of Anthropic's advisor-tool primitive.

An executor that calls an advisor is not delegating work — it keeps the work and asks for advice. Calling both "delegate" confuses the mental model.

## Asymmetry

`delegate-claude` exists, but not `delegate-codex`, `delegate-opencode`, or `delegate-gemini`. The executor→advisor pattern is model-agnostic in spirit but wired to Opus in practice. If advisory perspective is the goal, a Codex or Gemini advisor is sometimes cheaper and just as valid.

## Cross-linking is partial

`delegate-claude` cites `headless-claude` for flag conventions — good. `delegate` never cites `headless-opencode`, even though it literally routes OpenCode sub-agents.

## What the set is missing

1. **A unified delegation grammar.** Two axes: role (executor / advisor / reviewer / sub-agent) × CLI (claude / codex / opencode / gemini). The five skills partially cover the grid; a meta-skill could route cleanly.
2. **The reverse direction.** `delegate-claude` goes any-CLI → Claude. Nothing goes Claude → any-CLI (e.g., a Claude Code session calling Codex for a second opinion).
3. **Cache optimization in `delegate-claude`.** No mention of `--exclude-dynamic-system-prompt-sections`, which would sharply improve cache hits in a tight advisor loop.
4. **A session-aware variant.** The `<PRIOR_ADVICE>` manual re-pasting is a direct consequence of `--no-session-persistence`. When the executor *is* Claude Code, trading CLI-agnosticism for context reuse makes sense — add a variant that uses `-c` or named sessions.

## First move

Rename `delegate-claude` to `consult-claude` or `advisor-claude`. Scope `delegate` to what it actually is: an OpenCode review-pass router. Then decide whether the grid deserves a meta-skill.
