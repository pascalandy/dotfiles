# UpgradeSchema Workflow

Upgrade an existing v1 wiki to v2 conventions without rewriting page bodies.

## When to Use

- User says "upgrade wiki", "upgrade schema", or "migrate wiki to v2"
- CreateWikiMap detects an existing v1 wiki and halts

## Idempotent Detection

A wiki is considered v1 if any of these markers are present:
- `kind/relationship` appears anywhere
- any page is missing `date_created`
- a content page that should have `sources:` lacks it
- `INDEX.md` lacks the v2 header block and stats line

If none of those markers are found, report that the wiki is already at v2 and stop.

## Steps

### 1. Orientation

- Read the meta-skill `references/SCHEMA.md`
- Read the wiki's `INDEX.md`
- Read the last 30 entries of `references/LOG.md`
- Check for subdirectory drift against the recent log; note it, do not normalize it, and ask whether `INDEX.md` should reflect it if drift is detected

This workflow does not create new topic pages, so the 100+ page topic pre-search rule does not apply.

### 2. Detect and Report

Scan the wiki and report:
- pages with `kind/relationship` that will be rewritten to `topic/relationship`
- pages missing `date_created` that will be backfilled from `date_updated`
- pages missing `sources:` that require manual review
- `INDEX.md` if it needs the v2 header block
- pages missing `status/*` that would receive `status/open`
- content-kind pages below the outbound-link minimum, for review only
- pages over 200 lines, for review only
- large INDEX sections or oversized LOGs, for review only

### 3. Confirm

Present the auto-fix plan and ask for confirmation.

This workflow never runs automatically. In automated mode, halt before writing.

### 4. Apply Auto-Fixes

Apply only these changes:
- rewrite `kind/relationship` to `topic/relationship`
- backfill `date_created` from `date_updated` where missing
- prepend the v2 `INDEX.md` header block while preserving the existing table
- assign `status/open` to pages missing any `status/*` tag

### 5. Never Auto-Do

Do not automatically:
- infer or add `sources:` to old pages
- add new `topic/*` tags beyond the relationship migration
- fix weak cross-linking
- split long pages

### 6. Log

Append to `LOG.md`:

```markdown
- [[{today}]] upgrade | wiki | Schema upgraded to v2: {N} kind->topic rewrites, {N} date_created backfills, INDEX header added
```

### 7. Report

```markdown
## Upgrade Complete

**kind/relationship rewrites:** {N}
**date_created backfills:** {N}
**INDEX header added:** {yes/no}
**Manual review still needed for sources:** {N pages}
```
