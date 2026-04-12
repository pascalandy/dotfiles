---
name: IncidentReview
description: Write formal blameless postmortems after production incidents with root cause analysis, timelines, and action items. USE WHEN postmortem, incident review, blameless, root cause analysis, 5 whys, SEV, outage, incident, RCA, timeline, production incident, service disruption.
---

# IncidentReview

Write effective blameless postmortems that drive organizational learning and prevent incident recurrence.

## When to Use

- Post-incident reviews (SEV1, SEV2, or any significant incident)
- Customer-facing outages
- Data loss or security incidents
- Near-misses that could have been severe
- Novel failure modes
- Incidents requiring unusual intervention

## Blameless Culture

| Blame-Focused | Blameless |
|---------------|-----------|
| "Who caused this?" | "What conditions allowed this?" |
| "Someone made a mistake" | "The system allowed this mistake" |
| Punish individuals | Improve systems |
| Hide information | Share learnings |
| Fear of speaking up | Psychological safety |

Every postmortem starts by establishing: "We are here to learn, not to blame."

## Template Selection

Ask the user which template fits the incident:

1. **Standard** -- Full postmortem with executive summary, detailed timeline, root cause analysis (including 5 Whys), detection/response assessment, impact quantification, and prioritized action items. For SEV1/SEV2 incidents.

2. **5 Whys** -- Deep causal chain analysis drilling from symptom to systemic root causes. For complex incidents where the root cause is unclear or multi-layered.

3. **Quick** -- Condensed postmortem for minor incidents (SEV3/SEV4). Timeline, root cause, fix, and one lesson. Fast to write, still captures the key insight.

## Execution

### Step 1: Gather Incident Data

Collect from conversation, logs, alerts, and the user:

- Incident start/end times (UTC)
- Severity level (SEV1-SEV4)
- Affected services and components
- Error messages, alerts, metrics screenshots
- Who responded and when
- Resolution actions taken
- Customer impact (users affected, revenue loss, support tickets)

If critical details are missing, ask and wait before proceeding.

### Step 2: Construct Timeline

Build a chronological timeline:

| Time (UTC) | Event |
|------------|-------|
| HH:MM | [What happened, who did what] |

Identify gaps in the timeline and flag them.

### Step 3: Root Cause Analysis

Apply 5 Whys methodology:

1. Why did the service fail? -> [answer + evidence]
2. Why [answer 1]? -> [answer + evidence]
3. Why [answer 2]? -> [answer + evidence]
4. Why [answer 3]? -> [answer + evidence]
5. Why [answer 4]? -> [answer + evidence]

Distinguish:
- **Proximate cause** -- the specific technical failure
- **Contributing factors** -- conditions that allowed the proximate cause
- **Systemic root causes** -- organizational or process gaps

### Step 4: Assess Detection and Response

| Category | What Worked | What Didn't Work |
|----------|-------------|------------------|
| Detection | [How the incident was detected] | [Detection gaps, alert timing] |
| Response | [Effective response actions] | [Response delays, process gaps] |
| Communication | [Clear comms] | [Information gaps] |

### Step 5: Draft Action Items

Create prioritized, owned, time-bound action items:

| Priority | Action | Owner | Due Date | Ticket |
|----------|--------|-------|----------|--------|
| P0 | [Critical prevention] | @who | YYYY-MM-DD | LINK |
| P1 | [Important improvement] | @who | YYYY-MM-DD | LINK |
| P2 | [Nice-to-have hardening] | @who | YYYY-MM-DD | LINK |

### Step 6: Write Postmortem

Assemble the full document using the selected template from `references/`. Include:
- All sections from the template
- Specific data points, not vague descriptions
- Graphs/metrics links where available
- Related incidents for pattern detection

### Step 7: Review and Present

Show the completed postmortem to the user for review. Flag:
- Timeline gaps that need filling
- Action items without owners
- Root causes that seem incomplete

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Better Approach |
|-------------|---------|-----------------|
| Blame game | Shuts down learning | Focus on systems |
| Shallow analysis | Doesn't prevent recurrence | Ask "why" 5 times |
| No action items | Waste of time | Always have concrete next steps |
| Unrealistic actions | Never completed | Scope to achievable tasks |
| No follow-up | Actions forgotten | Track in ticketing system |

## Facilitation Guide

For running a postmortem meeting (60 minutes):

1. **Opening (5 min)** -- Remind everyone of blameless culture
2. **Timeline Review (15 min)** -- Walk through events chronologically
3. **Analysis Discussion (20 min)** -- What failed, why, what conditions allowed it
4. **Action Items (15 min)** -- Brainstorm, prioritize, assign owners
5. **Closing (5 min)** -- Summarize key learnings, confirm owners
