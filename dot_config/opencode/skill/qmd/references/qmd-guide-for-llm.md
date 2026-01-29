# semantic search using qmd cli

It’s important that you use all these flags to leverage user’s GPU.

## start by indexing

```shell
qmd --backend lmstudio --index andy_alpha update &&\
qmd --backend lmstudio --index andy_alpha embed
```

## query

```shell
qmd --backend lmstudio --index andy_alpha --compact -n 15 query "Qui est mon ancien comptable ?"
```
