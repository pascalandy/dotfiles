# Cas d'utilisation et leur processus / Plateforme SOAR

---

## CU_01 | Triage Intelligent et Priorisation des Alertes de Sécurité

### Valeur d'affaires

- Élimination des alertes non-critiques (réduction du bruit)
- Optimisation des ressources de l'équipe Équipe SOC
- Accélération de la détection des vraies menaces
- Réduction des coûts opérationnels de surveillance

### Processus

```mermaid
---
title: CU_01 | Triage Intelligent Multi-Sources
---

sequenceDiagram
    autonumber

    participant S as SIEM
    participant X as Plateforme SOAR
    participant TI1 as Source 1
    participant TI2 as Source 2
    participant TI3 as Source N
    participant Équipe SOC as Équipe Équipe SOC

    S->>X: Flux d'alertes avec métadonnées enrichies
    X->>TI1: Requête reputation avec timestamp unique
    X->>TI2: Requête reputation avec identifiant différent
    X->>TI3: Requête reputation via proxy

    TI1-->>X: Réponse avec score de réputation / confiance
    TI2-->>X: Réponse avec score de réputation / confiance
    TI3-->>X: Réponse avec score de réputation / confiance

    alt Consensus fort (>80%)
        X->>X: Traitement automatique + logging
        Note over X: Déclenchement CU_04<br/>pour enrichissement si IOC détecté
    else Consensus faible (<50%)
        X->>Équipe SOC: Escalade avec sources contradictoires
        Note over Équipe SOC: Possible transition vers CU_01<br/>si criticité métier détectée
    else Consensus moyen (50-80%)
        X->>Équipe SOC: Review requise avec contexte enrichi
        Note over X: Enrichissement via CU_04<br/>avant escalade Équipe SOC
    end

    Note over S,S: m-à-j par Auteur (2025-12-09)
```

---

## CU_02 | Enrichissement Automatique des Incidents de Sécurité

### Valeur d'affaires

- Amélioration de la qualité des investigations
- Réduction du temps d'analyse manuelle
- Meilleure compréhension du contexte des incidents
- Optimisation des décisions de réponse

### Processus

```mermaid
---
title: CU_02 | Enrichissement Automatique des Incidents de Sécurité
---

sequenceDiagram
    autonumber

    participant S as SIEM
    participant X as Plateforme SOAR
    participant TI as Threat Intelligence
    participant GEO as Géolocalisation
    participant Équipe SOC as Équipe Équipe SOC

    S->>X: Incident avec IOC
    Note over S: IP, Domaine,<br/>Hash de fichier

    X->>TI: Requête threat intelligence
    Note over TI: Source TI 1, Source TI 2,<br/>Source TI 3, Source TI 4

    X->>GEO: Géolocalisation IP
    GEO-->>X: Localisation et ASN

    X->>X: Corrélation historique
    Note over X: Liens avec<br/>autres incidents

    X->>X: Génération de contexte enrichi
    Note over X: - Timeline détaillée<br/>- Graphiques relationnels<br/>- Recommandations

    X->>Équipe SOC: Rapport enrichi
    Note over Équipe SOC: Contexte complet<br/>pour investigation

    loop Mise à jour continue
        X->>TI: Actualisation réputation
        TI-->>X: Nouvelles informations
        X->>Équipe SOC: Notifications de mise à jour
    end

    Note over S,S: m-à-j par Auteur (2025-12-09)
```

---

## CU_03 | Réponse Automatique aux Incidents de Sécurité Critiques

### Valeur d'affaires

- Réduction drastique du temps de réponse aux menaces
- Prévention des pertes financières majeures et des dommages à la réputation
- Conformité automatique aux exigences réglementaires BSIF/OSFI
- Minimisation de l'intervention humaine lors d'incidents critiques

### Processus

```mermaid
---
title: CU_03 | Réponse Automatique aux Incidents de Sécurité Critiques
---

sequenceDiagram
    autonumber

    participant S as SIEM
    participant X as Plateforme SOAR
    participant Sys as Systèmes affectés
    participant Équipe SOC as Équipe Équipe SOC

    S->>X: Alerte sécurisée avec validation
    Note over S,X: Webhook sécurisé + signature

    X->>X: Classification intelligente avec contexte
    Note over X: - Analyse multi-critères<br/>- Impact business assessment<br/>- Historique incidents

    alt Validation incertaine
        X->>Équipe SOC: Escalade immédiate + contexte
        Note over Équipe SOC: Pas d'isolation automatique<br/>Validation humaine requise
        Note over X: Transition possible vers CU_02<br/>pour triage approfondi
    else Validation positive haute confiance
        X->>Sys: Isolation progressive par phases
        Note over Sys: - Phase 1: Monitoring renforcé<br/>- Phase 2: Restriction accès<br/>- Phase 3: Isolation complète
        Sys-->>X: Confirmation par étapes
        X->>Équipe SOC: Notification + plan d'action
        Note over X: Déclenchement CU_03<br/>pour documentation conformité
    end

    loop Surveillance continue
        X->>X: Re-validation toutes les X minutes
        Note over X: Confiance score mise à jour
    end

    Note over S,S: m-à-j par Auteur (2025-12-09)
```

---

## CU_04 | Orchestration des Réponses Multi-Systèmes

### Valeur d'affaires

- Coordination cohérente des actions sur tous les systèmes
- Élimination des erreurs manuelles lors des interventions
- Réduction du temps de remédiation
- Amélioration de l'efficacité opérationnelle

### Processus

```mermaid
---
title: CU_04 | Orchestration des incidents sur nos actifs
---

sequenceDiagram
    autonumber

    participant S as SIEM
    participant X as Plateforme SOAR
    participant MAP as Mappage Systèmes
    participant FW as Firewall
    participant EDR as EDR Solution
    participant IAM as Identity Management
    participant DB as Base de Données
    participant APP as Applications Métier
    participant MON as Monitoring
    participant Équipe SOC as Équipe Équipe SOC

    S->>X: Alerte multi-systèmes avec métadonnées
    Note over S: - Systèmes affectés<br/>- Criticité métier<br/>- Dépendances identifiées

    X->>MAP: Analyse topology et dépendances
    Note over MAP: - Cartographie complète<br/>- Impacts en cascade<br/>- Priorités systèmes

    par Analyse parallèle des systèmes
        X->>FW: Requête statut et capacités
        FW-->>X: État actuel + règles actives
    and
        X->>EDR: Inventaire endpoints affectés
        EDR-->>X: Liste endpoints + versions agents
    and
        X->>IAM: Analyse comptes compromis
        IAM-->>X: Profils utilisateurs + permissions
    and
        X->>DB: Vérification intégrité données
        DB-->>X: Statut + sauvegardes récentes
    and
        X->>APP: Test accès applications
        APP-->>X: Disponibilité + dépendances
    end

    X->>X: Calcul plan d'orchestration optimal
    Note over X: - Actions parallèles<br/>- Validation croisée<br/>- Rollback intelligent

    Note over X,X: Phase 1: Actions non-critiques
    par Actions parallèles priorisées
        X->>FW: Blocage trafic suspect (IP/Ports)
        FW-->>X: Confirmation + règles appliquées
    and
        X->>EDR: Isolation endpoints (quarantaine)
        EDR-->>X: Endpoints isolés + scans
    and
        X->>MON: Surveillance renforcée temps réel
        MON-->>X: Métriques de surveillance
    end

    Note over X,X: Phase 2: Actions critiques coordonnées
    X->>IAM: Désactivation compte avec propagation
    IAM->>APP: Révocation sessions actives
    IAM->>DB: Blocage accès données sensibles
    IAM-->>X: Confirmation disable + propagation

    X->>X: Validation croisée des actions
    Note over X: - Vérification efficacité<br/>- Test accès résiduels<br/>- Contrôle intégrité

    alt Échec d'une action critique
        X->>X: Mécanisme de rollback intelligent
        Note over X: - Annulation actions précédentes<br/>- Restauration états<br/>- Notification impact
        X->>Équipe SOC: Escalade avec plan de recovery
        Note over Équipe SOC: Analyse échec + actions manuelles
        Note over X: Possible déclenchement CU_04<br/>pour analyse approfondie
    else Validation positive
        X->>X: Monitoring post-orchestration
        Note over X: - Surveillance continue<br/>- Métriques efficacité<br/>- Alertes anomalies
        X->>Équipe SOC: Rapport orchestration complet
        Note over Équipe SOC: - Actions réalisées<br/>- Validation efficacité<br/>- Recommandations
        Note over X: Déclenchement CU_03<br/>pour documentation conformité
    end

    loop Surveillance continue (24h)
        X->>MON: Vérification état systèmes
        MON-->>X: Métriques + alertes
        X->>X: Ajustement si nécessaire
    end

    Note over S,S: m-à-j par Auteur (2025-12-09)
```

---

## CU_05 | Conformité Réglementaire Automatique et Reporting

### Valeur d'affaires

- Conformité automatique aux exigences BSIF/OSFI
- Réduction des risques de pénalités réglementaires
- Transparence complète des activités de sécurité pour les auditors
- Rationalisation des processus d'audit et de certification

### Processus

```mermaid
---
title: CU_05 | Conformité Réglementaire Automatique et Reporting
---

sequenceDiagram
    autonumber

    participant X as Plateforme SOAR
    participant DB as Base de données conformité
    participant AUD as Auditeurs/Régulateur

    X->>X: Collecte automatique des logs
    Note over X: Toutes actions<br/>de sécurité

    X->>DB: Sauvegarde
    Note over DB: Classification<br/>par type d'incident

    loop Génération de rapports
        X->>X: Compilation des données
        X->>X: Génération de rapports
        Note over X: - Rapports exécutifs<br/>- Tableaux de bord<br/>- Preuves de conformité
    end

    X->>AUD: Diffusion automatique
    Note over AUD: Selon calendrier<br/>réglementaire

    alt Demande d'audit spécifique
        AUD->>X: Demande d'extraction
        X->>X: Préparation des preuves
        X->>AUD: Transmission
    end

    X->>X: Validation automatique
    Note over X: Vérification<br/>complétude des données

    Note over X,X: m-à-j par Auteur (2025-12-09)
```
