# Standard Postmortem Template

```markdown
# Postmortem: [Incident Title]

**Date**: YYYY-MM-DD
**Authors**: @person1, @person2
**Status**: Draft | In Review | Final
**Incident Severity**: SEV[1-4]
**Incident Duration**: [X] minutes

## Executive Summary

[2-3 sentences: what happened, root cause, resolution, impact]

**Impact**:
- [X] users/customers affected
- Estimated [revenue/data/time] loss
- [X] support tickets created
- [Data loss / security implications: yes/no]

## Timeline (All times UTC)

| Time | Event |
|------|-------|
| HH:MM | [Event description] |
| HH:MM | [Event description] |

## Root Cause Analysis

### What Happened
[Technical description of the failure]

### Why It Happened

1. **Proximate Cause**: [The specific technical failure]

2. **Contributing Factors**:
   - [Factor 1]
   - [Factor 2]
   - [Factor 3]

3. **5 Whys Analysis**:
   - Why [symptom]? -> [cause 1]
   - Why [cause 1]? -> [cause 2]
   - Why [cause 2]? -> [cause 3]
   - Why [cause 3]? -> [cause 4]
   - Why [cause 4]? -> [root cause]

## Detection

### What Worked
- [Detection success 1]
- [Detection success 2]

### What Didn't Work
- [Detection gap 1]
- [Detection gap 2]

## Response

### What Worked
- [Response success 1]

### What Could Be Improved
- [Response improvement 1]

## Impact

### Customer Impact
- [Quantified customer impact]

### Business Impact
- [Quantified business impact]

### Technical Impact
- [Technical consequences]

## Lessons Learned

### What Went Well
1. [Success 1]
2. [Success 2]

### What Went Wrong
1. [Failure 1]
2. [Failure 2]

### Where We Got Lucky
1. [Lucky break 1]

## Action Items

| Priority | Action | Owner | Due Date | Ticket |
|----------|--------|-------|----------|--------|
| P0 | [Action] | @who | YYYY-MM-DD | LINK |
| P1 | [Action] | @who | YYYY-MM-DD | LINK |
| P2 | [Action] | @who | YYYY-MM-DD | LINK |

## Appendix

### Supporting Data
- [Links to dashboards, graphs, logs]

### Related Incidents
- [Links to similar past incidents]
```
