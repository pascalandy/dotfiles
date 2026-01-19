# Patterns / Query Engineering Playbook

Goal: Help an AI assistant run effective semantic searches by picking the best pattern for the situation.

## Playbook: choosing a pattern

Key principle: The raw user query is rarely optimal. The assistant should rewrite it using the appropriate pattern.

**Actors**

- `USER` = the person asking a question
- `AI` = the assistant
- `EMB` = embedding search (via a CLI)

**Quick selection guide**

- If the query is vague or ambiguous
  - `Self-Ask`: generate clarification sub-questions, then search per sub-question
  - `Step-back`: ask a more general question first, then narrow down to the specific one
- If the request is multi-turn (references like “that”, “here”, “in our setup”)
  - `Decomposition`: break it into atomic sub-questions, then search per sub-question
- If it’s troubleshooting (symptom → cause)
  - `Symptoms + causes`: cover symptoms, root causes, and known fixes
- If you have reliable metadata (date, type, domain, product)
  - `Hybrid`: filter first, then run semantic search on the subset
- If you get too few relevant results
  - `Query Expansion`: generate 3–5 variants (synonyms, internal jargon, different phrasings), then merge results
- If you want to steer search with a “proto-answer”
  - `HyDE`: write a short hypothetical answer, then search for documents similar to that answer

## Patterns (details)

### Pattern 1: Query Expansion (multiple rewrites)

#### Example

**Intent**: Generate 3–5 semantically-close variants, run them in parallel, merge results.

```text
├── USER:
│   ├── "What do we do when an employee clicks a phishing link?"
├── AI generates variants:
│   ├── "employee clicked phishing link incident procedure"
│   ├── "phishing click incident response steps"
│   ├── "post-click compromise detection playbook"
│   ├── "user clicked malicious link containment steps"
│   └── "SOAR playbook phishing user clicked malicious link"
├── EMB:
│   ├── "employee clicked phishing link incident procedure"
│   ├── "phishing click incident response steps"
│   ├── "post-click compromise detection playbook"
│   ├── "user clicked malicious link containment steps"
│   └── "SOAR playbook phishing user clicked malicious link"
└── AI reviews relevant results and answers
```

### Pattern 2: Step-back (first principles)

**Mechanism**: ask a more general question, then refine toward the target question.

#### Example

**Intent**: Start from a general obligation, then drill down to the specific detail.

```text
├── USER:
│   └── "What is the notification deadline to MSSS for a health data breach?"
├── AI generates a step-back question:
│   ├── "What are the notification obligations for data breaches in Quebec?"
│   └── "What is the notification deadline to MSSS for a health data breach?"
├── EMB:
│   ├── "What are the notification obligations for data breaches in Quebec?"
│   └── "What is the notification deadline to MSSS for a health data breach?"
└── AI reviews relevant results and answers
```

### Pattern 3: Hypothetical Document Embedding (HyDE)

**Mechanism**: generate a short hypothetical answer, then search for documents similar to that answer.

#### Example

**Intent**: Write a plausible “proto-answer”, then use it as the search query.

```text
├── USER:
│   └── "How does our company handle phishing incidents?"
├── AI writes a short hypothetical answer:
│   ├── "Triage: confirm the incident, identify the user and channel"
│   ├── "Containment: revoke sessions, reset access, enforce MFA"
│   ├── "Eradication: remove emails, block URLs/domains, scan endpoints"
│   ├── "Recovery: restore access, monitor, fix controls"
│   └── "Postmortem: document and update playbooks + rules"
├── EMB:
│   └── (semantic search using the hypothetical answer)
└── AI reviews relevant results and answers
```

### Pattern 4: Decomposition into sub-questions (multi-turn)

**Mechanism**: decompose the request into atomic (standalone) sub-questions, search separately, then synthesize.

#### Example

**Intent**: Turn a conversation into a list of atomic questions, then run one search per question.

```text
├── Conversation (3 turns)
│   ├── USER: "What is SSPM?"
│   ├── USER: "How do we implement it in our environment?"
│   └── USER: "What is the typical ROI?"
├── AI extracts atomic (standalone) sub-questions:
│   ├── "SSPM definition (SaaS Security Posture Management)"
│   ├── "SSPM implementation steps (context: financial institution)"
│   └── "Typical SSPM KPIs and ROI"
├── EMB:
│   ├── "SSPM SaaS security posture management definition"
│   ├── "SSPM implementation best practices financial institution"
│   └── "SSPM KPIs ROI typical"
└── AI synthesizes and answers
```

### Pattern 5: Metadata filtering + semantics (hybrid)

**Mechanism**: apply structured filters before vector search.

#### Example

**Intent**: Reduce the search space with structured filters, then run a semantic query on the subset.

```text
├── USER:
│   └── "Show me SOC procedures updated in 2024"
├── AI extracts:
│   ├── structured filter: source_type = "procedure" AND domain = "SOC" AND date >= 2024-01-01
│   └── semantic query: "SOC operational procedures"
├── EMB (hybrid):
│   ├── applies the structured filter
│   └── vector search with the semantic query
└── AI reviews relevant results and answers
```

Result: filter first, then run vector search on the subset

### Pattern 6: Query Expansion with symptoms + causes

**Mechanism**: generate queries that cover symptoms AND root causes.

#### Example

**Intent**: Increase recall by covering both the observed issue and plausible technical root-cause hypotheses.

```text
├── USER:
│   └── "My VPN disconnects every 5 minutes on Mac"
├── AI generates queries:
│   ├── Exact symptom: "VPN disconnection every 5 minutes macOS"
│   ├── Similar symptoms: "VPN connection drops frequently Mac unstable"
│   ├── Possible technical causes:
│   │   ├── "VPN timeout network MTU fragmentation macOS"
│   │   ├── "VPN authentication session expiry certificate"
│   │   └── "Cisco AnyConnect GlobalProtect Mac bug disconnection"
│   └── Known fixes: "fix VPN disconnection macOS troubleshooting steps"
├── EMB:
│   ├── "VPN disconnection every 5 minutes macOS"
│   ├── "VPN connection drops frequently Mac unstable"
│   ├── "VPN timeout network MTU fragmentation macOS"
│   ├── "VPN authentication session expiry certificate"
│   ├── "Cisco AnyConnect GlobalProtect Mac bug disconnection"
│   └── "fix VPN disconnection macOS troubleshooting steps"
└── AI reviews relevant results and answers
```

### Pattern 7: Self-Ask (reflective agent)

**Mechanism**: the agent generates clarification sub-questions before retrieval.

#### Example

**Intent**: Clarify before retrieval to avoid an overly vague search, then formulate a more precise query set.

```text
├── USER:
│   └── "My VPN disconnects every 5 minutes on Mac"
├── AI (Self-Ask) asks diagnostic questions:
│   ├── "Which VPN client is the user on? (Cisco, GlobalProtect, other)"
│   ├── "Which macOS version?"
│   ├── "Does it happen on all networks or only Wi‑Fi?"
│   ├── "Are there errors in system logs?"
│   └── "Did it start after an update?"
├── AI generates queries (without user clarification):
│   ├── "VPN macOS disconnects every 5 minutes Wi‑Fi"
│   ├── "GlobalProtect macOS VPN disconnects every 5 minutes"
│   ├── "Cisco AnyConnect macOS VPN disconnects every 5 minutes"
│   ├── "VPN macOS MTU fragmentation frequent disconnects"
│   └── "VPN macOS session expiry auth errors disconnect"
├── EMB:
│   ├── "VPN macOS disconnects every 5 minutes Wi‑Fi"
│   ├── "GlobalProtect macOS VPN disconnects every 5 minutes"
│   ├── "Cisco AnyConnect macOS VPN disconnects every 5 minutes"
│   ├── "VPN macOS MTU fragmentation frequent disconnects"
│   └── "VPN macOS session expiry auth errors disconnect"
└── AI reviews relevant results and answers
```

## Anti-patterns to avoid

- Raw user query: never pass the question as-is without rewriting it
- Orphan chunks: chunks without metadata = lost context = hallucinations
- Top-k too small: k < 10 often misses relevant results
- Ignoring reranking: bi-encoders alone have limited precision
- Single embedding model: consider domain-specific models (code, legal, etc.)
