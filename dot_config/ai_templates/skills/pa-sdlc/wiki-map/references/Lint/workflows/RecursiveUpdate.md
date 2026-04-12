# RecursiveUpdate Workflow

Refresh an existing wiki tree bottom-up. Preserve existing nested child wiki boundaries, rebuild local `INDEX.md` files level by level, and refresh parent routes from child wiki metadata.

## When to Use

- user says `wiki-map update`
- user says `recursive wiki update`
- user says `refresh wiki tree`
- user says `update nested wiki`
- a requested wiki already contains nested child wikis and the goal is maintenance rather than one-off diagnosis

## Steps

### 1. Orientation and Boundary Discovery

- read the shared `references/SCHEMA.md`
- read the requested wiki's `INDEX.md`
- read the last 30 entries of the requested wiki's active `references/LOG.md`
- discover nested wiki descendants under the requested wiki
- treat only directories that already contain their own `INDEX.md` as nested child wiki boundaries
- ignore plain directories that do not define their own child wiki boundary
- sort discovered child wikis deepest first so traversal is bottom-up

Emit progress in traversal order as the run proceeds.

### 2. Refresh Each Wiki Bottom-Up

For each discovered wiki, from deepest descendant up to the requested root wiki:

- read that wiki's local `INDEX.md`
- refresh local indexing for the wiki's own pages
- keep plain directories without `INDEX.md` in the local indexing model as ordinary content
- preserve existing child wiki routes
- refresh each direct child route description from the child `INDEX.md`
- use child `INDEX.md` frontmatter `description` first
- fall back to the first non-empty paragraph after frontmatter and title when description is missing
- do not flatten a child wiki's internal pages into the parent `INDEX.md`
- do not create new child wiki boundaries

### 3. Failure Handling

- use best-effort execution for nested trees
- if one branch fails, skip that branch and continue updating sibling branches
- continue updating higher levels when it is still safe to do so
- do not stop mid-run to ask the user how to handle a failed branch
- collect warnings and report them at the end

### 4. Report Results

Report the actual bottom-up traversal order.

```markdown
## Recursive Wiki Update: {wiki name}

### Traversal
1. updated {grandchild wiki path}
2. updated {child wiki path}
3. updated {root wiki path}

### Warnings
1. skipped {failed branch path}: {reason}
```

If there are no failures, state that explicitly.

### 5. Update LOG.md

For each successfully updated wiki, append a maintenance entry to that wiki's active `references/LOG.md`.

```markdown
- [[{today}]] lint | recursive update | refreshed local index and direct child wiki routes
```
