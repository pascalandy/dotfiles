# semantic search using qmd cli

It’s important that you use all these flags to leverage user’s GPU.

## start by indexing

```shell
/Users/andy16/Documents/github_local/SKILLS_MONO/apps/qmd/qmd --backend lmstudio --index andy_alpha update &&\
/Users/andy16/Documents/github_local/SKILLS_MONO/apps/qmd/qmd --backend lmstudio  --index andy_alpha embed
```

## query

```shell
/Users/andy16/Documents/github_local/SKILLS_MONO/apps/qmd/qmd --backend lmstudio --index andy_alpha --compact -n 15 vsearch "Qui est mon ancien comptable ?"
```
