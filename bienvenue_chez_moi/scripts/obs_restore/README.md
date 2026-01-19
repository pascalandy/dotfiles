# Note personnelle : Projet Obs Restore

## Pourquoi ce projet ?
J'ai remarqué un phénomène inquiétant : certaines notes semblent disparaître "mystérieusement" de ma voûte Obsidian. Heureusement, j'ai des backups (Time Machine, snapshots, etc.).

L'objectif de ce dossier est de rassembler les outils pour identifier et restaurer ces fichiers perdus.

## Conclusion apres 1h30 de travail

donc même en ayant restauré environ une quinzaine de snapshots sur deux ans, je ne comprends pas mais il y a des notes qui étaient inexistantes tout partout, comme si ça n'avait jamais existé. j'ai de la misère à comprendre donc c'est pour ça que je vais mettre en place d'autres mécanismes pour garder un historique, un snapshot de l'arborescence de mon dossier Obsidian. 

## La Stratégie
L'idée originale (voir `archives/idea_obs_restore.md`) est de :
1. Scanner l'état actuel de la voûte.
2. Comparer chronologiquement avec des backups (il y a 1 semaine, 1 mois, 2 mois...).
3. Générer une liste des notes qui existaient avant mais qui sont absentes aujourd'hui.
4. Procéder à une vérification et restauration manuelle.

## Outils inclus

### `clean_missing_files.py`
Ce script est une utilitaire pour nettoyer les listes de fichiers "manquants" (souvent générées sous forme de liens brisés dans Obsidian, ex: `[[Note Perdue]] in [[Autre Note]]`).

**Usage :**
Il prend un fichier texte en entrée (liste brute) et extrait proprement les noms de fichiers pour en faire une liste exploitable.

```bash
uv run clean_missing_files.py input_list.md --output clean_list.md
```

---
*Ce README sert de mémoire pour ne pas oublier le contexte de création de ce script lors de futures sessions de maintenance.*
