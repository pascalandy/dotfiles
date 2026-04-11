# Out-of-Scope Knowledge Base

The `.out-of-scope/` directory stores persistent records of rejected feature requests. It serves two purposes:

1. **Institutional memory** -- why a feature was rejected, so the reasoning is not lost
2. **Deduplication** -- surface previous decisions when similar requests come in

## Directory Structure

One file per **concept**, not per issue. If three issues request variations of the same thing, they share one file.

Use a short, descriptive kebab-case name for the file. The name should be recognizable enough that someone browsing the directory understands what was rejected without opening the file.

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

## File Format

Written in relaxed, readable style with paragraphs, code samples, and examples. Not a rigid template.

### Example

```markdown
# Dark Mode

## Why this is out of scope

The application's design system is built on a single light theme with carefully tuned contrast ratios for accessibility. Supporting dark mode would require:

- A complete audit of every color token (currently ~80 tokens)
- Dual-theme testing for all components
- A theme-switching mechanism in user preferences
- Migration of existing CSS that uses hardcoded colors

The ROI doesn't justify the effort for our current user base, which is primarily enterprise users on managed workstations with controlled display settings.

If this changes in the future (e.g., user research shows accessibility needs for dark mode, or we rebuild the design system), this decision should be revisited.

## Prior requests
- #142 (2024-01-15) -- "Add dark mode support"
- #198 (2024-03-22) -- "Support system theme preference"
- #245 (2024-06-10) -- "High contrast mode for accessibility" (related but distinct)
```

## Writing the Reason

Good reasons are:
- **Principled** -- based on design decisions, architectural constraints, or user research
- **Durable** -- won't become irrelevant next quarter
- **Specific** -- explain what makes this particular request out of scope, not just "we don't want to"

Avoid referencing temporary circumstances ("we're too busy right now") -- those are not real rejections, they are deferrals.

## When to Check

During triage (Step 1 of the GithubTriage workflow), read all `.out-of-scope/*.md` files. Match by **concept similarity**, not keyword matching. A request for "dark mode" and "theme support" might match the same entry.

If a match is found, present it to the maintainer. The maintainer can:
- **Confirm** the rejection -- post a comment linking to the prior decision, close the issue, add the new issue number to the "Prior requests" list
- **Reconsider** -- delete the `.out-of-scope/` file and proceed with normal triage
- **Disagree** with your match -- proceed with normal triage

## When to Write

Only when an **enhancement** (not a bug) is rejected as `wontfix`:
1. Check if an existing `.out-of-scope/` file covers this concept
2. If yes, append the new issue to the "Prior requests" list
3. If no, create a new file
4. Post a comment on the issue explaining the decision
5. Close the issue
6. Apply `wontfix` label

## Updating or Removing

If the maintainer changes their mind about a previously rejected feature, delete the `.out-of-scope/` file. The new issue that triggered the reconsideration proceeds through normal triage. Old issues are historical records -- do not reopen them.
