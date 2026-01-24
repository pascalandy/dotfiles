---
name: cli-chezmoi
description: "Gère les dotfiles via le CLI chezmoi. Utilisez ce skill lorsque vous devez lire, modifier ou ajouter des fichiers de configuration (dotfiles) dans le répertoire personnel de l'utilisateur. Il garantit que les modifications sont effectuées dans le répertoire source de chezmoi (~/.local/share/chezmoi) et appliquées correctement."
---

# Cli Chezmoi

Ce skill permet de gérer les fichiers de configuration (dotfiles) de l'utilisateur en utilisant l'outil `chezmoi`. Il assure que les modifications ne sont pas faites directement sur les fichiers dans le home directory, mais via le système de gestion de `chezmoi`.

## Workflow de base

### 1. Identifier un dotfile

Avant de modifier un fichier de configuration (ex: `.zshrc`, `.gitconfig`), vérifiez s'il est géré par chezmoi.

```bash
chezmoi list | grep <nom_du_fichier>
```

### 2. Modifier un fichier

N'éditez JAMAIS un fichier directement dans le home directory s'il est géré par chezmoi. Utilisez la commande `edit` :

```bash
chezmoi edit ~/.zshrc
```

Cela ouvrira le fichier source (ex: `~/.local/share/chezmoi/dot_zshrc`) dans votre éditeur.

### 3. Appliquer les changements

Après avoir modifié un fichier via `chezmoi edit`, ou si vous avez modifié manuellement un fichier dans `~/.local/share/chezmoi`, appliquez les changements :

```bash
chezmoi apply -v
```

### 4. Ajouter un nouveau fichier

Pour commencer à gérer un nouveau fichier avec chezmoi :

```bash
chezmoi add ~/.new_config
```

## Commandes Utiles

- `chezmoi status` : Voir l'état des fichiers (modifiés, à appliquer).
- `chezmoi diff` : Voir les différences entre les fichiers gérés et les fichiers réels.
- `chezmoi cd` : Se déplacer dans le répertoire source de chezmoi.
- `chezmoi managed` : Lister tous les fichiers gérés.

## Références

Pour plus de détails sur les commandes et les templates, consultez [references/api_reference.md](references/cli_reference.md).

## cli-btca

Donne accès aux docs du repo offciel via le skill cli `cli-btca`
