# Plan : Restauration de fichiers manquants - Un par un (v2 - Optimisé)

## Contexte
- **412 fichiers manquants** à retrouver dans les snapshots
- **9 snapshots** disponibles (2023-12-01 → 2025-11-26)
- **Vault actuel** : `$HOME/Documents/_my_docs/10_obsidian/vault_obsidian`
- **Snapshots** : `/Volumes/2TBM2/11_obsidian_bkp/`

## Stratégie de recherche optimisée

Pour chaque fichier manquant, dans l'ordre de la liste :

```
1. Recherche globale dans TOUS les snapshots avec find
   └─ find /Volumes/2TBM2/11_obsidian_bkp/ -iname "*pattern*" | sort -r | head -1
   └─ Si trouvé → open -R → NEXT
   
2. Si non trouvé → Essayer des variations du nom
   └─ Wildcards, variations orthographiques, avec/sans tirets, o/0, etc
   └─ Si trouvé → open -R → NEXT

3. Si toujours non trouvé → Recherche par contenu avec rg
   └─ rg -l "pattern" /Volumes/2TBM2/11_obsidian_bkp/
   └─ Si trouvé → open -R → NEXT

4. Si toujours non trouvé → mgrep sémantique (dernier recours)
   └─ cd snapshot_recent && mgrep -m 10 "description sémantique"
   └─ Si trouvé → open -R → NEXT

5. Si introuvable → marquer comme "non trouvé" dans le log
```

## Outils de recherche (par ordre de préférence)

| Outil | Usage | Performance | Commande |
|-------|-------|-------------|----------|
| `find` | Recherche par nom de fichier | ⭐⭐⭐ | `find /path -iname "*pattern*" 2>/dev/null \| sort -r \| head -1` |
| `rg` (ripgrep) | Recherche par contenu | ⭐⭐⭐⭐⭐ | `rg -l "pattern" /path 2>/dev/null` |
| `mgrep` | Recherche sémantique | ⭐⭐ | `cd /path && mgrep -m 10 "semantic query"` |
| `grep` | ❌ À éviter | ⭐ | Trop lent, utiliser `rg` à la place |

## Cas particuliers identifiés

| Type de fichier | Stratégie |
|-----------------|-----------|
| **Noms génériques** (template, note, link, database, expression, YYYY-MM-DD) | Probablement des placeholders → Vérifier avec `rg` si référencés comme exemples |
| **Fichiers dans .trash** | ✅ Valides! Ne pas ignorer `.trash/` |
| **Daily notes** (2023-03-09) | Recherche exacte : `find -name "2023-03-09.md"` |
| **Images** (.webp) | `find -iname "*.webp"` |
| **Variations de noms** (o3-mini vs o3 mini vs o3mini) | Essayer toutes les variations avec wildcards |

## Workflow optimisé par fichier

```bash
# 1. Recherche globale (prend le plus récent automatiquement)
RESULT=$(find /Volumes/2TBM2/11_obsidian_bkp/ -iname "*pattern*" 2>/dev/null | sort -r | head -1)

# 2. Si trouvé
if [ -n "$RESULT" ]; then
  open -R "$RESULT"
  echo "| N | Nom | ✅ | snapshot | $RESULT |" >> log.md
else
  # 3. Essayer variations, rg, mgrep...
  # 4. Si toujours rien
  echo "| N | Nom | ❌ | - | Non trouvé |" >> log.md
fi
```

## Logging

- **Fichier** : `./EXPORT/obs_restore/restoration_log.md`
- **Méthode** : Append uniquement (`echo >> log.md`)
- **Ne jamais** : Relire et réécrire les lignes existantes (l'utilisateur édite le log)

Format :
```markdown
| # | Fichier | Statut | Snapshot | Chemin |
|---|---------|--------|----------|--------|
| 1 | Blinkist - 12 Rules For Life | ✅ | 2025-08-19 | /Volumes/.../file.md |
| 2 | Gemini 2.5 Pro | ❌ | - | Non trouvé (similaires: ...) |
```

## Retrait de liens brisés (bonus)

Quand un fichier est trouvé et que des liens brisés doivent être retirés :

```bash
# 1. Trouver les fichiers contenant le lien
grep -rl "\[\[Nom du fichier\]\]" /path/to/vault/

# 2. Retirer le lien avec sed (sans lire le fichier d'abord)
sed -i '' 's/- \[\[Nom du fichier\]\]//g' fichier.md
```

## Ordre d'exécution

1. Commencer par **fichier #1** et procéder séquentiellement
2. Attendre confirmation de l'utilisateur avant de passer au suivant
3. Logger chaque résultat immédiatement

---

**Version** : v2 (Optimisé après retour d'expérience)
**Date** : 2025-12-14
