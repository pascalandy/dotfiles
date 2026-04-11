---
name: Providers and Effort
description: The three providers distill supports, their model allowlists, the canonical effort vocabulary, and the vendor-flag ETL
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - distill
---

distill's provider layer is deliberately thin. Each provider is a shell-out to a CLI, a resolved model string from an allowlist, and a canonical effort level that gets translated to whatever flag vocabulary that CLI actually accepts. Nothing else is negotiated. This page documents every constant that governs the three providers, where it lives in the source, and why the exceptions exist.

## The three providers

Defined as string constants at `scripts/distill.py:49-56`:

| Constant | Value | Default |
|---|---|---|
| `PROVIDER_CLAUDE` | `claude` | yes (`DEFAULT_PROVIDER` at `scripts/distill.py:57`) |
| `PROVIDER_CODEX` | `codex` | no |
| `PROVIDER_OPENCODE` | `opencode` | no |

The CLI flag is `--provider {claude,codex,opencode}`. Absent the flag, distill picks claude.

## Model allowlists

Every provider has a hard-coded allowlist in the source. Requests for an unknown model fail fast with `EXIT_USAGE` in `resolve_model` (`scripts/distill.py:499-536`):

### Claude — `scripts/distill.py:59-66`

| Model | Default? | Notes |
|---|---|---|
| `claude-opus-4-6` | yes | Highest-quality distillation, highest cost |
| `claude-sonnet-4-6` | no | Listed in `SONNET_MODELS` — triggers the effort-default special-case (see below) |

### Codex — `scripts/distill.py:68-69`

| Model | Default? |
|---|---|
| `gpt-5.4` | yes |

### OpenCode — `scripts/distill.py:71-87`

OpenCode does not expose raw model IDs. Instead, it routes through curated *agents*, and distill's allowlist is the agent list. `1-kimi` is the default.

```
1-kimi (default), 2-opus, 3-gpt, 4-sonnet,
worker, worker1, worker2, worker3,
glm, gemini, gpthigh, gptxhigh, gptmini, flash
```

## Canonical effort vocabulary

distill picks one vocabulary and forces every provider to speak it: `low`, `medium`, `high`, `max`. Declared at `scripts/distill.py:89`:

```python
CANONICAL_EFFORTS: tuple[str, ...] = ("low", "medium", "high", "max")
```

The user always types a canonical value. distill translates to whatever the vendor CLI actually accepts through `EFFORT_ETL` at `scripts/distill.py:94-107`:

| Canonical | Claude vendor flag | Codex vendor flag |
|---|---|---|
| `low` | `low` | `low` |
| `medium` | `medium` | `medium` |
| `high` | `high` | `high` |
| `max` | `max` | `xhigh` |

As of 2026-04-11, claude and codex agree on every canonical level except `max` (codex calls it `xhigh`). Earlier versions of the script mapped canonical `medium` to vendor `med` for claude, but upstream claude CLI removed the `med` short form and started rejecting it, so the ETL was corrected to `medium → medium`. See the [LOG](LOG.md) entry for 2026-04-11.

OpenCode is absent from the ETL on purpose. OpenCode agents have their own built-in reasoning configuration — distill does not pass any effort flag, and passing `--effort` alongside `--provider opencode` is rejected at argparse time (`scripts/distill.py:435-436`) with exit code `EXIT_USAGE`.

### Effort defaults

The default is `DEFAULT_EFFORT = "high"` at `scripts/distill.py:90`. This applies to claude-opus and codex alike. There is one exception:

**Sonnet special-case** — any model listed in `SONNET_MODELS` (`scripts/distill.py:66`) overrides the default to `low`. The logic is at `scripts/distill.py:641-653`:

```python
if provider == PROVIDER_OPENCODE:
    effort_canonical = "agent-defined"
    effort_vendor = "agent-defined"
elif args.effort is not None:
    effort_canonical = args.effort
    effort_vendor = translate_effort(provider, effort_canonical)
elif model in SONNET_MODELS:
    effort_canonical = "low"
    effort_vendor = translate_effort(provider, effort_canonical)
else:
    effort_canonical = DEFAULT_EFFORT
    effort_vendor = translate_effort(provider, effort_canonical)
```

Precedence is: explicit `--effort` beats everything, then Sonnet override, then `DEFAULT_EFFORT`. The Sonnet exception exists because sonnet-4-6 is fast and economical and is often reached for when the operator wants a quick summary, not a deep distillation — defaulting it to `high` would waste the model's intended use.

## Per-provider context limits

distill enforces safe input-token ceilings declared at `scripts/distill.py:110-114`:

| Provider | Limit (input + prompt combined) |
|---|---|
| `claude` | 600,000 tokens |
| `codex` | 450,000 tokens |
| `opencode` | 250,000 tokens |

`check_context_size` at `scripts/distill.py:543-558` uses the `tiktoken` `cl100k_base` encoding to count tokens in the input text plus the prompt plus a small fixed overhead for the `"Based on this content:\n\n"` framing declared at `scripts/distill.py:130`. If the total exceeds the limit, the script raises `DistillError` with exit code `EXIT_USAGE` and the error message tells the operator to reduce input size or split the file.

These limits are deliberately conservative — they are not the model's hard context window, they are the point at which the operator should split the input rather than push the provider to its edge.

## Retries and timeouts

Two constants at `scripts/distill.py:116-117` govern every provider call:

- `LLM_CLI_TIMEOUT_SECONDS = 600` — ten minutes per attempt
- `LLM_MAX_RETRIES = 3` — the script retries up to three times with exponential backoff via `retry_request` at `scripts/distill.py:206-253`

A hung provider CLI fails fast at ten minutes rather than hanging forever. A transient provider error (network blip, rate limit) gets three chances before distill surfaces `LLMCallError` to the operator.

## Related

- [[overview]]
- [[output-layout]]
- [[troubleshooting]]
