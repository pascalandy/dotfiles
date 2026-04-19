# Properties (Frontmatter) Reference

Properties use YAML frontmatter at the very start of a note (no blank lines before `---`):

```yaml
---
title: My Note Title
date: 2024-01-15
tags:
  - project
  - important
aliases:
  - My Note
  - Alternative Name
cssclasses:
  - custom-class
status: in-progress
rating: 4.5
completed: false
due: 2024-02-01T14:30:00
---
```

## Property types

| Type | Example |
|------|---------|
| Text | `title: My Title` |
| Number | `rating: 4.5` |
| Checkbox | `completed: true` |
| Date | `date: 2024-01-15` |
| Date & Time | `due: 2024-01-15T14:30:00` |
| List | `tags: [one, two]` or YAML list |
| Links | `related: "[[Other Note]]"` |

## Default properties

- `tags` -- searchable labels, shown in graph view. See tag syntax rules in the main skill.
- `aliases` -- alternative names for the note (used in link suggestions). **Must be a list**, not a string.
- `cssclasses` -- CSS classes applied to the note in reading/editing view.
