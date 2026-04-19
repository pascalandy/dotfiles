---
workflow: TestIdea
mode: single-run
---

# Test Idea Against World Threat Models

Test any idea, strategy, investment, brand, or concept against all 11 persistent world models
to assess viability across time horizons.

## When to Use

- User says "test this idea," "how will this hold up," "test my strategy," "stress test this"
- User provides an idea/strategy/investment and wants temporal viability analysis
- User wants to understand when an idea breaks or thrives

## Prerequisites

- World models must exist in the selected world-model directory
- If models don't exist, prompt user to run UpdateModels workflow first

## Tier Detection

Detect from user prompt:
- **"fast"** or **"quick"** → Fast tier
- **"deep"** or **"thorough"** or **"comprehensive"** → Deep tier
- **No modifier** → Standard tier (default)

## Workflow Steps

### Step 0: Validate Models Exist

```
Use the user-specified world-model directory, or default to `WorldModels/` in the current workspace.
Check that directory for all 11 model files.
If any missing: "World models incomplete. Run 'update world models' first."
If models older than 30 days: warn user but proceed.
```

### Step 1: Status Update

Tell the user you are testing the idea against all eleven world models at the selected tier.

### Step 2: Extract and Decompose the Idea

Before hitting it with world models, decompose the idea:

1. **State the idea** in 1-2 sentences
2. **Identify core assumptions** the idea relies on (market conditions, technology state, cultural norms, regulatory environment, competitive landscape)
3. **Identify success dependencies** — what must remain true for this to work?

For **Standard and Deep tiers:** Invoke FirstPrinciples skill to classify assumptions:
- Hard constraints (physics, demographics, math)
- Soft constraints (policy, regulation, cultural norms)
- Assumptions (unvalidated beliefs the idea depends on)

### Step 3: Run Against World Models

Read all 11 model files from the selected world-model directory.

#### Fast Tier (~2 min)
Single-agent analysis:
1. Read all 11 models sequentially
2. For each horizon, generate: Verdict (🟢/🟡/🔴) + 2-3 bullet points
3. Write Executive Verdict
4. Output using abbreviated format from `../references/OutputFormat.md`

#### Standard Tier (~10 min)
Parallel analysis when available:
1. If multi-agent execution is available, analyze one horizon per parallel worker. Otherwise, analyze the horizons sequentially.
2. Each horizon analysis:
   - Reads ONE world model document
   - Analyzes the idea against that specific horizon
   - Tests each assumption against the horizon's conditions
   - Returns: Verdict, Key Factors, Analysis, Assumptions Tested
3. After all agents return, invoke **RedTeam skill** with:
   - Prompt: "Attack this idea across all time horizons. Here are the per-horizon analyses: {results}"
   - Extract adversarial findings per horizon
4. Synthesize Cross-Horizon Synthesis section
5. Output using full format from `../references/OutputFormat.md`

#### Deep Tier (up to 1 hr)
Full capability invocation:
1. **FirstPrinciples** (if not already run): Full deconstruct → challenge → reconstruct cycle on the idea
2. **Research update check**: For each horizon, run a quick web research check for any new developments that affect this specific idea
3. **Horizon analysis**: Same as Standard but with deeper prompts and longer analysis per horizon. Run in parallel if available, otherwise sequentially.
4. **RedTeam** (32 agents): Full adversarial analysis of the idea across all horizons
5. **Council**: Multi-agent debate on the idea's long-term viability
   - Prompt: "Debate the viability of {idea} across time horizons from 6 months to 50 years. Consider: {per-horizon results}"
   - Extract Council Deliberation section
6. Synthesize all findings
7. Output using complete format from `../references/OutputFormat.md` (all sections)

### Step 4: Format Output

Use the template in `../references/OutputFormat.md`. Ensure:
- Each horizon is clearly separated with its own section header
- Verdicts use consistent emoji indicators
- Confidence levels reflect model confidence × analysis certainty
- Adversarial findings attribute to specific horizon contexts

### Step 5: Completion Update

Summarize the executive verdict for the user in one or two sentences.

## Output Format

See `../references/OutputFormat.md`.

## Integration Points

| Skill | Tier | Purpose |
|-------|------|---------|
| **FirstPrinciples** | Standard, Deep | Decompose idea assumptions before testing |
| **RedTeam** | Standard, Deep | Adversarial attack on idea across horizons |
| **Council** | Deep only | Multi-perspective debate on viability |
| **Web research** | Deep only | Quick refresh of horizon-relevant current events |

## Error Handling

- If a parallel worker fails: continue with remaining analyses, note the missing horizon in output
- If a skill invocation fails: degrade gracefully (e.g., skip Council section, note in footer)
- If models are stale (>90 days): prominently warn in header, recommend update
