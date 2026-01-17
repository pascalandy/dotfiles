---
description: apply chezmoi changes, commit and push
---

IF the current directory is : `$HOME/.local/share/chezmoi`

THEN: run these commands :

```sh
chezmoi diff
chezmoi apply
commit (see how by using the commit skill)
git push
```

ELSE: Tell the user : "Can't run this. We must run these commands into `chezmoi cd`"
