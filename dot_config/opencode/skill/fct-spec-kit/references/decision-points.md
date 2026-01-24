# Decision Points - Étapes optionnelles

Guide pour décider si une étape optionnelle est nécessaire.

## /speckit.constitution

| Utiliser                              | Sauter                               |
| ------------------------------------- | ------------------------------------ |
| Nouveau projet sans principes établis | Principes déjà documentés            |
| Changement majeur d'architecture      | Feature simple alignée avec existant |
| Nouvelle équipe sur le projet         | Constitution récente et stable       |

## /speckit.clarify

| Utiliser                                        | Sauter                        |
| ----------------------------------------------- | ----------------------------- |
| >3 `[NEEDS CLARIFICATION]` dans spec            | Spec claire, pas de marqueurs |
| Domaine métier inconnu                          | Domaine bien maîtrisé         |
| Stakeholders multiples avec visions différentes | Un seul décideur clair        |
| Feature critique (sécurité, paiement)           | Spike exploratoire, prototype |

## /speckit.checklist

| Utiliser                               | Sauter                              |
| -------------------------------------- | ----------------------------------- |
| Feature critique, haute visibilité     | Feature interne, low-risk           |
| Domaine nouveau (a11y, security, i18n) | Domaine couvert par tests existants |
| Besoin de validation par pairs         | Solo dev, itération rapide          |
| Conformité/compliance requise          | Prototype, PoC                      |

## /speckit.analyze

| Utiliser                            | Sauter                         |
| ----------------------------------- | ------------------------------ |
| Avant implémentation majeure        | Petite feature isolée          |
| Long contexte, risque d'incohérence | Contexte frais, session courte |
| Post-modifications multiples        | Première génération sans edits |
| Doute sur couverture requirements   | Tasks clairement mappées       |

## /speckit.taskstoissues

| Utiliser                                | Sauter                    |
| --------------------------------------- | ------------------------- |
| Repo GitHub avec issue tracking         | Pas de repo GitHub        |
| Équipe distribuée, besoin de visibilité | Solo dev, tasks.md suffit |
| Intégration CI/GitHub Projects          | Workflow manuel préféré   |

## Règle générale

En cas de doute:

- Feature critique → inclure l'étape
- Prototype/spike → sauter pour vélocité
- Demander à l'utilisateur si incertain
