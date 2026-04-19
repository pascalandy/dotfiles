# Delete Workflow

Safely remove one page from the wiki with full inbound-link cleanup.

## When to Use

- User says "delete", "remove", or "get rid of" a specific page
- A page is wrong, off-topic, duplicative, or superseded

Use `status/close` for completed work that should remain in the wiki. Delete is for pages that should not exist at all.

## Steps

### 1. Orientation

- Read the meta-skill `references/SCHEMA.md`
- Read the wiki's `INDEX.md`
- Read the last 30 entries of `references/LOG.md`
- Check for subdirectory drift against the recent log; note it, do not normalize it, and ask whether `INDEX.md` should reflect it if drift is detected

This workflow does not create new pages, so the 100+ page topic pre-search rule does not apply.

### 2. Identify the Target

Confirm the page to delete by page name or file path.

Refuse to delete:
- `INDEX.md`
- active or rotated log files
- any page tagged `kind/wiki`
- any page tagged `kind/log`

These require manual intervention.

### 3. Find References

Scan all wiki pages for both:
- inbound `[[target-page-name]]` wikilinks in body text and `## Related`
- frontmatter `sources:` references pointing to the target page name

Build a list with:
- source page
- whether the reference is a wikilink or a `sources:` provenance link
- line number or section when available
- surrounding sentence, bullet, or frontmatter context

### 4. Present Findings and Actions

For each inbound wikilink, present options:
- replace with plain text: `target-page-name (deleted)`
- redirect to another page
- remove the sentence or bullet if it becomes empty
- leave broken, with warning that lint will flag it

For each `sources:` provenance reference, present options:
- remove the deleted source from the `sources:` list
- replace it with another source page if there is a valid provenance successor
- halt if provenance would become misleading and the user has not decided how to handle it

Also ask for:
- the reason for deletion
- final confirmation

In automated mode:
- default wikilink handling to plain-text replacement
- default `sources:` handling to removing the deleted page from the list
- halt instead of guessing if a provenance replacement would require human judgment

### 5. Extra Confirmation for Webclips

If the target is a `kind/webclip` page, require explicit confirmation because deleting it removes provenance for any page that cites it in `sources:`.

### 6. Apply

1. Apply the chosen action to each inbound wikilink
2. Apply the chosen cleanup to each `sources:` provenance reference
3. Remove the page from `INDEX.md`
4. Delete the file with `trash` when available; fall back only if no safer delete exists
5. Append a log entry:

```markdown
- [[{today}]] delete | {page-name} | reason: {reason} | fixed inbound links in {N} pages: [list]
```

### 7. Report

```markdown
## Page Deleted: {page-name}

**Inbound links fixed:** {N}
**Provenance references fixed:** {N}
**INDEX.md updated:** yes
**LOG.md updated:** yes
```

## Guardrails

- Never delete without inbound-link analysis
- Never batch-delete from this workflow
- Never delete protected wiki root or log pages
