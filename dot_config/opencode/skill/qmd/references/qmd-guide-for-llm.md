# semantic search using qmd cli

## general usage 

```shell
qmd --help
```

## start by indexing

```shell
qmd --backend lmstudio --index andy_alpha update
qmd --backend lmstudio --index andy_alpha embed

## force it from scratch
qmd --backend lmstudio --index andy_alpha embed -f
```

## query

```shell
qmd --index andy_alpha --compact -n 15 query "Qui est mon ancien comptable ?"
```
