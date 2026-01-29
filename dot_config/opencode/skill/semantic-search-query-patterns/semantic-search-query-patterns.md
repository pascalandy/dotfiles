# Semantic Search Query Patterns

Query engineering determines retrieval quality. A raw user question rarely matches how information is stored. These patterns transform user intent into effective vector searches.

**Key principle:** Combine patterns. A single search often benefits from expansion + filtering + temporal awareness. The patterns below are composable building blocks.

## Chunking Fundamentals

Before querying, documents must be chunked well.

### Chunk Size

| Size | Use Case |
|------|----------|
| 256-512 tokens | Precise, fact-based retrieval |
| 512-1024 tokens | Broader context, explanations |

Domain matters. Test with your data.

### Chunking Methods

- **Semantic**: Split by paragraph or logical section
- **Sliding window**: 20-30% overlap between chunks
- **Recursive**: Hierarchical separators (headers → paragraphs → sentences)

### Preserve Context

Each chunk should carry:
- Parent document title
- Section/chapter name
- Date, author, source
- Business tags (department, project, status)

Repeat key context in chunk headers when the chunk would otherwise lose meaning.

## Query Patterns

### Pattern 1: Query Expansion

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

**When to use:**
- User vocabulary differs from document vocabulary
- Documents use technical jargon the user doesn't know
- You want recall over precision

### Pattern 2: Query Decomposition

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

**When to use:**
- Multi-faceted questions (procedure + legal + technical)
- Cross-domain queries (cybersecurity + compliance)
- Region-specific context (Quebec vs. Canada vs. international)

### Pattern 3: Contextual Query Rewriting

Rewrite follow-up questions using conversation history.

```python
# Turn 1
user: "What is SSPM?"
→ query: "SSPM SaaS security posture management definition"

# Turn 2
user: "How do we implement it here?"
→ BAD:  "How do we implement it here?"
→ GOOD: "SSPM implementation financial institution Canadian bank"

# Turn 3
user: "What's the typical ROI?"
→ BAD:  "What's the typical ROI?"
→ GOOD: "ROI return investment SSPM cloud security financial services"
```

**When to use:**
- Multi-turn conversations
- Pronouns or references to previous context ("it", "that", "this approach")
- Follow-up questions that lack standalone meaning

### Pattern 4: Diagnostic Expansion

For troubleshooting queries, expand across symptom → cause → solution dimensions.

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

**When to use:**
- User describes a problem, error, or malfunction
- Troubleshooting scenarios
- You need to surface both cause documentation and solution guides

### Pattern 5: Self-Ask

The agent generates clarifying questions before retrieval.

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

**When to use:**
- Ambiguous queries missing critical context
- Diagnostic/troubleshooting scenarios
- High-stakes queries where precision matters

### Pattern 6: HyDE (Hypothetical Document Embedding)

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

**When to use:**
- Vague or abstract questions
- User doesn't know domain vocabulary
- Large semantic distance between question length and document length

### Pattern 7: Metadata Pre-filtering

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

**When to use:**
- Large corpus spanning departments/projects
- Known user context (role, team, location)
- Documents with lifecycle status (draft, approved, archived)

### Pattern 8: Multi-hop Retrieval

Use first retrieval results to inform the next query.

```python
user_query = "What are the exceptions to our MFA policy?"

# Hop 1: Find the main policy
hop1_query = "MFA policy multi-factor authentication"
hop1_results = vector_search(hop1_query, top_k=3)
# → Finds "POL-SEC-042: Corporate MFA Policy"

# Hop 2: Extract context, search for exceptions
policy_id = extract_policy_id(hop1_results)  # "POL-SEC-042"
hop2_query = f"exceptions exemptions {policy_id} MFA"
hop2_results = vector_search(hop2_query, top_k=5)
# → Finds exception documents linked to this policy

# Hop 3 (optional): Find approved exception cases
hop3_query = f"approved MFA exception request {policy_id}"
hop3_results = vector_search(hop3_query, top_k=5)
```

**When to use:**
- Questions about document relationships (policy → exceptions → cases)
- Hierarchical navigation (parent → children)
- Progressive context building

### Pattern 9: Temporal Query Rewriting

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

**When to use:**
- Versioned corpus (policies, procedures)
- Time-sensitive documents (incidents, changes)
- Document lifecycle tracking (draft → approved → deprecated → archived)

## Combining Patterns

Real queries benefit from multiple patterns. Examples:

**Complex compliance question:**
1. **Decomposition** → Break into legal + procedural sub-queries
2. **Metadata filtering** → Filter by region (Quebec) and doc_type (policy)
3. **Temporal** → Ensure current/approved versions only

**Vague troubleshooting query:**
1. **Self-Ask** → Generate clarifying questions
2. **Diagnostic Expansion** → Cover symptoms + causes + solutions
3. **Query Expansion** → Add vocabulary variations

**Follow-up in conversation:**
1. **Contextual Rewriting** → Inject prior context
2. **HyDE** → Bridge short question to detailed docs
3. **Multi-hop** → First find referenced doc, then search within it

## Result Aggregation

When running multiple queries, merge results using:

- **Reciprocal Rank Fusion (RRF)**: Weight by position across result sets
- **Score normalization**: Normalize similarity scores, then combine
- **De-duplication**: Remove duplicate chunks by ID before final ranking

The aggregation strategy matters as much as the query strategy.
