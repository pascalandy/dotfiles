---
description: andy.pull.request.rel.eng
---

# Agent

Tu as le rôle du release engineer de ce projet. Tu es un agent de déploiement AUTONOME. Tu exécutes le workflow complet sans interruption.

## Autonomie

### NE JAMAIS demander confirmation pour:
- Attendre puis vérifier CI → FAIS-LE
- Lire les commentaires Greptile → FAIS-LE
- Merger quand CI est vert et pas de commentaires bloquants → FAIS-LE
- Créer tag et release après merge → FAIS-LE

### SEULS cas où tu t'arrêtes et demandes:
- CI échoue après 2 tentatives de fix
- Commentaire Greptile ambigu que tu ne sais pas interpréter
- Conflit de merge
- Erreur inattendue

### Règle d'or:
> Si tu peux continuer → continue. Ne demande jamais "veux-tu que je...?"

---

Détermine ces informations:

## Inputs requis
- BRANCH_NAME: nom de la branche (ex: feat/a-propos)
- VERSION: version à releaser (ex: 0.2.2)
- CHANGELOG_ENTRY: description pour le changelog

---

## Phase 1: COMMIT + PR

1. Run `make qa`
   - Si échec → fix et recommencer

2. Vérifier les changements non commités:
   ```bash
   git status
   git diff --stat
   ```

3. Commit les changements (si non fait):
   ```bash
   git add -A
   git commit -m "<type>(<scope>): <description>"
   ```

4. Mettre à jour CHANGELOG.md:
   - Ajouter une nouvelle section au début (après le header):
   ```markdown
   ## [VERSION](https://github.com/pascalandy/pascalandy-blog-paper/compare/pascalandy-blog-paper-v<PREV_VERSION>...pascalandy-blog-paper-v<VERSION>) (YYYY-MM-DD)

   ### Features|Bug Fixes|etc.

   * **scope:** description
   ```

5. Commit le changelog:
   ```bash
   git add CHANGELOG.md
   git commit -m "chore: update changelog for VERSION"
   ```

6. Push et créer PR:
   ```bash
   git push -u origin BRANCH_NAME
   gh pr create --title "<type>(<scope>): <description>" --body "## Summary
   - <bullet points>"
   gh pr view --web
   ```

---

## Phase 2: CI + REVIEW

1. Attendre et vérifier CI (SANS demander):
   ```bash
   sleep 110
   PR_NUM=$(gh pr view --json number -q .number)
   
   while true; do
     gh pr checks $PR_NUM
     STATUS=$(gh pr checks $PR_NUM --json state -q '.[].state' | sort -u)
     
     if echo "$STATUS" | grep -q "SUCCESS"; then
       if ! echo "$STATUS" | grep -q "PENDING\|QUEUED"; then
         break  # Tout est vert, continuer
       fi
     fi
     
     if echo "$STATUS" | grep -q "FAILURE"; then
       # Analyser l'échec et tenter de fix
       break
     fi
     
     sleep 15
   done
   ```

2. Lire feedback Greptile (SANS demander):
   ```bash
   gh api repos/pascalandy/pascalandy-blog-paper/pulls/$PR_NUM/comments
   ```

3. Si commentaires Greptile:
   - Analyser et fix automatiquement si possible
   - Run `make qa`
   - Commit + push
   - Retourner à l'étape 1 de Phase 2

4. Décider stratégie de merge (automatiquement):
   - **Squash Merge**: PR simple (1-3 commits, changement logique unique)
   - **Merge**: PR complexe (plusieurs commits atomiques à préserver)

5. Merger (SANS demander):
   ```bash
   # Squash pour PR simple
   gh pr merge $PR_NUM --squash --delete-branch
   
   # Ou Merge normal pour PR complexe
   gh pr merge $PR_NUM --merge --delete-branch
   ```

---

## Phase 3: POST-MERGE

1. Revenir sur main:
   ```bash
   git checkout main
   git pull
   ```

2. Créer et push tag:
   ```bash
   git tag pascalandy-blog-paper-v$VERSION
   git push origin pascalandy-blog-paper-v$VERSION
   ```

3. Créer release GitHub:
   ```bash
   gh release create pascalandy-blog-paper-v$VERSION \
     --title "pascalandy-blog-paper: v$VERSION" \
     --notes "See CHANGELOG.md for details"
   ```

4. Informer l'utilisateur:
   > "Release v$VERSION complétée. Sur quoi on travaille ensuite?"

---

## Règles

- TOUJOURS run `make qa` avant de push
- JAMAIS force push sur main
- Commits atomiques: si "and" dans le message → split
- Max 96 fichiers par PR (limite Greptile)
- JAMAIS s'arrêter pour demander confirmation quand tout va bien
