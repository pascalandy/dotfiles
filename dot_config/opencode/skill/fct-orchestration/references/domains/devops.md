# DevOps Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Infrastructure as carefully orchestrated as code.         │
│   Safe deployments. Fast pipelines. Reliable operations.    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **AGENT REMINDER**: Only use `@ben`, `@abby`, or `@oracle`.
> See [SKILL.md](../../SKILL.md) for costs and task mapping.
> In examples below, "Agent A/B/C" = parallel `@abby` tasks for implementation or `@ben` for ops.

> **Load when**: CI/CD pipeline, deployment, infrastructure as code, monitoring, incident response
> **Common patterns**: Pipeline Setup, Zero-Downtime Deployment, Incident Triage

## Table of Contents

1. [CI/CD Pipeline](#cicd-pipeline)
2. [Deployment](#deployment)
3. [Infrastructure](#infrastructure)
4. [Monitoring and Alerting](#monitoring-and-alerting)
5. [Incident Response](#incident-response)

---

## CI/CD Pipeline

### Pattern: Pipeline Setup

```
User Request: "Set up CI/CD for this project"

Phase 1: EXPLORE
└─ @ben: Analyze project structure, build system, test setup

Phase 2: PLAN
└─ @abby: Design pipeline stages and requirements

Phase 3: FAN-OUT (Parallel stage implementation - @ben tasks)
├─ @ben: Build stage (compile, dependencies)
├─ @ben: Test stage (unit, integration)
├─ @ben: Security scan stage (SAST, dependencies)
└─ @ben: Deploy stage (environments, rollback)

Phase 4: PIPELINE
└─ @abby: Wire stages, add notifications
```

### Pattern: Pipeline Optimization

```
User Request: "Speed up our CI pipeline"

Phase 1: FAN-OUT (Parallel analysis)
├─ @ben: Analyze current pipeline duration by stage
├─ @ben: Find parallelization opportunities
├─ @ben: Check caching effectiveness
└─ @ben: Review resource allocation

Phase 2: REDUCE
└─ @abby: Prioritized optimization plan

Phase 3: FAN-OUT (Implement optimizations - @ben tasks)
├─ @ben: Implement caching improvements
├─ @ben: Parallelize independent jobs
└─ @ben: Optimize resource-heavy stages
```

### Pattern: Multi-Environment Pipeline

```
Phase 1: EXPLORE
└─ @ben: Map environments (dev, staging, prod)

Phase 2: FAN-OUT (parallel @ben tasks)
├─ @ben: Configure dev deployment
├─ @ben: Configure staging deployment
├─ @ben: Configure prod deployment (with gates)
└─ @ben: Configure environment promotions

Phase 3: PIPELINE
└─ @abby: Add approval workflows, rollback triggers
```

---

## Deployment

### Pattern: Zero-Downtime Deployment

```
User Request: "Deploy the new version without downtime"

Phase 1: EXPLORE
└─ @ben: Current deployment strategy, infrastructure

Phase 2: PIPELINE
├─ @abby: Build and tag new image
├─ @abby: Deploy to canary/blue environment
├─ @ben: Run smoke tests
└─ @abby: Shift traffic, drain old instances

Phase 3: BACKGROUND
└─ @ben: Monitor error rates post-deploy
```

### Pattern: Rollback Preparation

```
Phase 1: FAN-OUT (Pre-deployment - @ben tasks)
├─ @ben: Tag current stable version
├─ @ben: Document database state
├─ @ben: Prepare rollback scripts
└─ @ben: Verify rollback path

Phase 2: PIPELINE (Deployment with safety)
├─ @abby: Deploy new version
├─ @ben: Health check monitoring
└─ @abby: (If needed) Execute rollback
```

### Pattern: Database Migration Deployment

```
Phase 1: PIPELINE (Safe migration)
├─ @abby: Backup current database
├─ @abby: Run forward migration
├─ @abby: Deploy compatible app version
└─ @ben: Verify data integrity

Phase 2: BACKGROUND
└─ @ben: Monitor for migration issues
```

---

## Infrastructure

### Pattern: Infrastructure as Code

```
User Request: "Create Terraform for our AWS setup"

Phase 1: EXPLORE
└─ @ben: Map current infrastructure, requirements

Phase 2: FAN-OUT (Parallel module creation - @ben tasks)
├─ @ben: Network module (VPC, subnets, security groups)
├─ @ben: Compute module (ECS/EKS, EC2)
├─ @ben: Database module (RDS, ElastiCache)
├─ @ben: Storage module (S3, EFS)
└─ @ben: CDN and DNS module

Phase 3: PIPELINE
├─ @abby: Wire modules, configure state backend
└─ @ben: Validate and plan
```

### Pattern: Kubernetes Manifest Generation

```
Phase 1: EXPLORE
└─ @ben: Analyze application requirements

Phase 2: FAN-OUT (parallel @ben tasks)
├─ @ben: Deployment manifests
├─ @ben: Service and ingress manifests
├─ @ben: ConfigMaps and Secrets
├─ @ben: HPA and PDB configurations
└─ @ben: NetworkPolicies

Phase 3: PIPELINE
├─ @abby: Kustomize or Helm setup
└─ @ben: Validate against cluster
```

### Pattern: Security Hardening

```
Phase 1: FAN-OUT (Parallel security checks - @ben tasks)
├─ @ben: Network security (firewall, security groups)
├─ @ben: IAM and access control
├─ @ben: Encryption (at rest, in transit)
├─ @ben: Secrets management
└─ @ben: Compliance checks

Phase 2: REDUCE
└─ @abby: Security report with remediations

Phase 3: FAN-OUT (Implement fixes)
├─ @ben: Implement security improvements
```

---

## Monitoring and Alerting

### Pattern: Observability Setup

```
User Request: "Set up monitoring for the application"

Phase 1: FAN-OUT (Parallel pillar implementation - @ben tasks)
├─ @ben: Metrics (Prometheus, CloudWatch)
├─ @ben: Logging (ELK, CloudWatch Logs)
├─ @ben: Tracing (Jaeger, X-Ray)
└─ @ben: Dashboards (Grafana, custom)

Phase 2: PIPELINE
└─ @abby: Configure alerting rules, runbooks
```

### Pattern: Alert Tuning

```
Phase 1: EXPLORE
└─ @ben: Analyze current alerts, noise ratio

Phase 2: FAN-OUT (parallel @ben tasks)
├─ @ben: Tune threshold-based alerts
├─ @ben: Implement anomaly detection
└─ @ben: Configure alert routing

Phase 3: PIPELINE
└─ @abby: Document runbooks for each alert
```

### Pattern: SLO Definition

```
Phase 1: EXPLORE
└─ @ben: Identify critical user journeys

Phase 2: FAN-OUT (parallel @ben tasks)
├─ @ben: Define availability SLIs/SLOs
├─ @ben: Define latency SLIs/SLOs
├─ @ben: Define error rate SLIs/SLOs
└─ @ben: Configure error budget alerts

Phase 3: PIPELINE
└─ @abby: Create SLO dashboard
```

---

## Incident Response

### Pattern: Incident Triage

```
User Request: "Production is down!"

Phase 1: FAN-OUT (Rapid parallel diagnosis - @ben tasks)
├─ @ben: Check application logs for errors
├─ @ben: Check infrastructure metrics
├─ @ben: Check recent deployments
├─ @ben: Check external dependencies
└─ @ben: Check database health

Phase 2: REDUCE (Fast)
└─ @abby: Identify most likely cause

Phase 3: PIPELINE
├─ @abby: Implement fix or rollback
└─ @ben: Verify recovery
```

### Pattern: Post-Incident Review

```
Phase 1: FAN-OUT (Evidence gathering)
├─ @ben: Timeline of events
├─ @ben: Relevant logs and metrics
├─ @ben: Changes before incident
└─ @ben: Response actions taken

Phase 2: PIPELINE
├─ @abby: Root cause analysis
├─ @abby: Impact assessment
└─ @abby: Action items and preventions

Phase 3: REDUCE
└─ @abby: Post-mortem document
```

### Pattern: Runbook Execution

```
Phase 1: EXPLORE
└─ @ben: Find relevant runbook

Phase 2: PIPELINE (Step-by-step)
├─ @abby: Execute step 1
├─ @abby: Verify step 1
├─ @abby: Execute step 2
└─ ... continue until resolved

Phase 3: BACKGROUND
└─ @ben: Continued monitoring
```

---

## Task Management for DevOps

Structure infrastructure work with safety checkpoints:

```python
# Create DevOps tasks
TaskCreate(subject="Assess infrastructure", description="Current state, requirements...")
TaskCreate(subject="Plan changes", description="Design with minimal disruption...")
TaskCreate(subject="Implement network changes", description="VPC, security groups...")
TaskCreate(subject="Implement compute changes", description="ECS, scaling...")
TaskCreate(subject="Validate deployment", description="Health checks, smoke tests...")
TaskCreate(subject="Configure monitoring", description="Alerts, dashboards...")

# Sequential safety gates
TaskUpdate(taskId="2", addBlockedBy=["1"])
TaskUpdate(taskId="3", addBlockedBy=["2"])
TaskUpdate(taskId="4", addBlockedBy=["2"])  # Can parallel with network
TaskUpdate(taskId="5", addBlockedBy=["3", "4"])
TaskUpdate(taskId="6", addBlockedBy=["5"])

# Parallel infrastructure implementation
Task(subagent_type="@abby", prompt="TaskId 3: Implement network changes...")
Task(subagent_type="@abby", prompt="TaskId 4: Implement compute changes...")
```

## Safety Principles

1. **Always have rollback plan** before deploying
2. **Background monitor** during and after deployment
3. **Parallel diagnosis** during incidents for speed
4. **Document everything** for future incidents
5. **Test in staging** before production

---

```
─── ◈ DevOps ────────────────────────────
```
