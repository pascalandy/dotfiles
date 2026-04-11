---
name: spec-kit
description: "Orchestrer le workflow Spec-Driven Development. Commandes /speckit.* pour specs, plans, tasks, implementation."
---

# Spec Kit

## But

Guider le workflow SDD étape par étape.

## Structure

```
spec-kit/
├── SKILL.md                    # Ce fichier
├── references/
│   ├── command/                # Instructions par commande (source de vérité)
│   ├── templates/              # Modèles: spec, plan, tasks, checklist, constitution
│   ├── decision-points.md      # Critères pour étapes optionnelles
│   ├── checkpoints.md          # Guide pour revues externes
│   └── spec-driven.md          # Contexte SDD (théorie)
└── scripts/                    # Scripts bash (numérotation, setup)
```

## Flux recommandé

1. `/speckit.specify` → `specs/###-feature/spec.md`
2. `/speckit.plan` → `plan.md` + artefacts
3. `/speckit.tasks` → `tasks.md`
4. `/speckit.implement` → code

Étapes optionnelles: voir `references/decision-points.md`

## Carte des commandes

| Commande               | Quand                  | Sortie                    |
| ---------------------- | ---------------------- | ------------------------- |
| /speckit.constitution  | Créer/màj constitution | `specs/constitution.md`   |
| /speckit.specify       | Nouvelle feature       | `spec.md` + checklist     |
| /speckit.clarify       | Spec ambiguë           | `spec.md` mis à jour      |
| /speckit.plan          | Plan technique         | `plan.md` + artefacts     |
| /speckit.checklist     | Qualité exigences      | `checklists/<domaine>.md` |
| /speckit.tasks         | Générer tasks          | `tasks.md`                |
| /speckit.analyze       | Audit cohérence        | rapport (read-only)       |
| /speckit.taskstoissues | Issues GitHub          | issues créées             |
| /speckit.implement     | Exécuter tasks         | code modifié              |

## Comment utiliser

1. Choisir étape selon le flux
2. Lire `references/command/speckit.<nom>.md`
3. Exécuter et suivre les règles

## Règles

- Source de vérité: `references/command/`
- Suggérer UNE étape à la fois
- Proposer checkpoint de revue après specify, plan, tasks
- Si validation critique: suggérer revue externe (autre AI/contexte)
- Charger `spec-driven.md` seulement si utilisateur veut théorie

## Structure d'export (repo cible)

```
specs/
├── constitution.md              # Global
├── 001-feature-name/
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   ├── research.md
│   ├── data-model.md
│   ├── quickstart.md
│   ├── contracts/
│   └── checklists/
└── 002-autre-feature/
    └── ...
```
