# Query Pattern Examples

Detailed implementation examples for each pattern.

## Contents

1. [Query Expansion](#pattern-1-query-expansion)
2. [Query Decomposition](#pattern-2-query-decomposition)
3. [Contextual Rewriting](#pattern-3-contextual-query-rewriting)
4. [Diagnostic Expansion](#pattern-4-diagnostic-expansion)
5. [Self-Ask](#pattern-5-self-ask)
6. [HyDE](#pattern-6-hyde-hypothetical-document-embedding)
7. [Metadata Pre-filtering](#pattern-7-metadata-pre-filtering)
8. [Multi-hop Retrieval](#pattern-8-multi-hop-retrieval)
9. [Temporal Rewriting](#pattern-9-temporal-query-rewriting)

---

## Pattern 1: Query Expansion

Generate 3-5 semantic variations of the same question.

**Raw query:**
```
"What do we do when an employee clicks a phishing link?"
```

**Expanded queries:**
```python
queries = [
    # Simplified original
    "phishing incident procedure employee",
    
    # Technical register
    "incident response phishing email compromise employee",
    
    # Process-focused
    "steps handle malicious link click user",
    
    # Detection angle
    "phishing compromise detection post-incident",
    
    # SOC tooling
    "playbook XSOAR phishing user clicked malicious link"
]
```

---

## Pattern 2: Query Decomposition

Break complex questions into atomic sub-queries.

```python
user_query = """
What's our procedure for phishing incidents targeting executives, 
and what are the notification deadlines required by Quebec's Law 25?
"""

sub_queries = [
    "incident response procedure phishing executives C-level",
    "playbook phishing targeting senior leadership high priority",
    "notification deadlines personal data breach Quebec Law 25",
    "legal obligations cybersecurity incident disclosure Canada",
    "timeline notification CAI privacy commissioner incident"
]
```

---

## Pattern 3: Contextual Query Rewriting

Rewrite follow-up questions using conversation history.

```python
# Turn 1
user: "What is SSPM?"
query: "SSPM SaaS security posture management definition"

# Turn 2
user: "How do we implement it here?"
BAD:  "How do we implement it here?"
GOOD: "SSPM implementation financial institution Canadian bank"

# Turn 3
user: "What's the typical ROI?"
BAD:  "What's the typical ROI?"
GOOD: "ROI return investment SSPM cloud security financial services"
```

---

## Pattern 4: Diagnostic Expansion

For troubleshooting, expand across symptom-cause-solution dimensions.

```python
queries = {
    # Exact symptom
    "symptom_exact": "VPN disconnection every 5 minutes macOS",
    
    # Similar symptoms
    "symptom_similar": "VPN connection drops frequently Mac unstable",
    
    # Possible technical causes
    "cause_network": "VPN timeout network MTU fragmentation macOS",
    "cause_auth": "VPN authentication session expiry certificate",
    "cause_client": "Cisco AnyConnect GlobalProtect Mac bug disconnection",
    
    # Known solutions
    "solution": "fix VPN disconnection macOS troubleshooting steps"
}
```

---

## Pattern 5: Self-Ask

Agent generates clarifying questions before retrieval.

```python
user_query = "My VPN disconnects every 5 minutes on Mac"

# Agent generates diagnostic questions
sub_questions = agent.self_ask(user_query)

[
    "Which VPN client? (Cisco, GlobalProtect, other)",
    "Which macOS version?",
    "Does this happen on all networks or only WiFi?",
    "Are there errors in system logs?",
    "Did this start after an update?"
]
```

**Two paths forward:**
1. **Interactive**: Ask user these questions, then search with refined context
2. **Parallel retrieval**: Use each question as a separate search query, merge results

---

## Pattern 6: HyDE (Hypothetical Document Embedding)

Generate a hypothetical answer, embed that instead of the question.

```python
user_query = "How do we secure our cloud?"

# Step 1: LLM generates hypothetical answer (no retrieval)
hypothetical_answer = llm.generate(f"""
Answer this question as if you had access to internal documentation:
{user_query}
""")

# Result:
# "To secure cloud infrastructure, implement CSPM, configure security 
#  groups with least privilege, enable CloudTrail logging, use IAM 
#  roles with minimal permissions, encrypt data at-rest and in-transit..."

# Step 2: Embed the hypothetical answer (not the question)
embedding = embed(hypothetical_answer)

# Step 3: Search for documents similar to this answer
results = vector_search(embedding, top_k=10)
```

**Why it works:** Short questions embed far from long, detailed documents. A hypothetical answer bridges that semantic gap.

---

## Pattern 7: Metadata Pre-filtering

Filter by metadata before vector search runs.

```python
user_query = "What's the backup policy for databases?"
user_context = {"department": "finance", "region": "quebec"}

# Step 1: Extract/infer relevant filters
filters = {
    "department": ["finance", "corporate"],  # Finance + global policies
    "doc_type": ["policy", "procedure", "standard"],
    "status": "approved",  # Exclude drafts
    "region": ["quebec", "canada", "global"]  # Geographic hierarchy
}

# Step 2: Vector search with pre-filtering
results = vector_search(
    query=user_query,
    filters=filters,
    top_k=10
)
```

---

## Pattern 8: Multi-hop Retrieval

Use first retrieval results to inform the next query.

```python
user_query = "What are the exceptions to our MFA policy?"

# Hop 1: Find the main policy
hop1_query = "MFA policy multi-factor authentication"
hop1_results = vector_search(hop1_query, top_k=3)
# Finds "POL-SEC-042: Corporate MFA Policy"

# Hop 2: Extract context, search for exceptions
policy_id = extract_policy_id(hop1_results)  # "POL-SEC-042"
hop2_query = f"exceptions exemptions {policy_id} MFA"
hop2_results = vector_search(hop2_query, top_k=5)
# Finds exception documents linked to this policy

# Hop 3 (optional): Find approved exception cases
hop3_query = f"approved MFA exception request {policy_id}"
hop3_results = vector_search(hop3_query, top_k=5)
```

---

## Pattern 9: Temporal Query Rewriting

Transform time references into filters or query modifications.

```python
temporal_queries = {
    "Recent security incidents?": {
        "rewrite": "security incidents breach compromise",
        "filters": {"date": "last_30_days"},
        "sort": "date_desc"
    },
    
    "Old backup procedure before cloud migration": {
        "rewrite": "backup procedure on-premise legacy",
        "filters": {"date_before": "2023-01-01", "status": ["archived", "deprecated"]}
    },
    
    "Policy changes this quarter": {
        "rewrite": "policy procedure update modification",
        "filters": {"date": "current_quarter", "doc_type": "policy"},
        "sort": "date_desc"
    }
}

# Temporal marker detection
temporal_markers = {
    r"recent|new|latest": "last_30_days",
    r"this month": "current_month",
    r"this quarter|Q[1-4]": "current_quarter",
    r"old|legacy|before": "archived_or_old",
    r"history|historical": "all_time_sort_desc"
}
```
