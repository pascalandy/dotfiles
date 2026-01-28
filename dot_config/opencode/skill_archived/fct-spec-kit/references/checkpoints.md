# Checkpoints - Guide pour revues externes

Certaines étapes bénéficient d'une revue dans un autre contexte (nouvelle session, autre AI, humain).

## Quand suggérer un checkpoint

### Après /speckit.specify

**Suggérer si:**

- Feature critique (sécurité, paiement, données sensibles)
- Spec complexe (>2 user stories, >5 requirements)
- Domaine métier nouveau pour l'équipe

**Message type:**

```
✋ Checkpoint: La spec est prête.
Avant de continuer, considérez une revue externe pour valider:
- Complétude des requirements
- Clarté des critères d'acceptation
- Scope approprié
```

### Après /speckit.plan

**Suggérer si:**

- Choix d'architecture significatif
- Nouvelles dépendances/technologies
- Intégrations externes critiques

**Message type:**

```
✋ Checkpoint: Le plan technique est complet.
Une revue externe peut valider:
- Choix technologiques appropriés
- Architecture scalable
- Risques identifiés et mitigés
```

### Après /speckit.tasks

**Suggérer si:**

- > 10 tasks générées
- Dépendances complexes entre tasks
- Doute sur la décomposition

**Message type:**

```
✋ Checkpoint: Tasks générées.
Une revue peut confirmer:
- Granularité appropriée
- Ordre de dépendances correct
- Rien n'est manquant
```

## Format d'export pour revue

Pour faciliter la revue dans un autre contexte, proposer:

```markdown
## Export pour revue

Voici le contexte à copier dans une nouvelle session:

---
**Feature:** [nom]
**Étape complétée:** /speckit.[commande]
**Fichiers à revoir:**
- specs/###-feature/spec.md
- specs/###-feature/plan.md (si applicable)

**Questions de validation:**
1. [question spécifique 1]
2. [question spécifique 2]
3. [question spécifique 3]
---
```

## Quand NE PAS suggérer

- Prototype/spike exploratoire
- Feature triviale (<3 requirements)
- Domaine bien maîtrisé, patterns établis
- Utilisateur a explicitement demandé d'accélérer
