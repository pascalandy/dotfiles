---
name: cli-btca
description: "Use when the user asks to use btca or wants docs answers for a supported library/framework."
---

# btca

Use `btca` to query local docs for supported libraries and frameworks.

## Ask a question

```bash
btca ask -t <tech> -q "<question>"
```

Example:

```bash
btca ask -t opencode -q "Does opencode have an sdk available?"
```

## List supported tech

```bash
btca config repos list
```

## If something fails

- Missing tech: tell the user you cannot find it.
- Missing CLI: check with `which btca`.

## More details

See `references/`.
