
## 1. Chunking fundamentals

### 1.1 Chunk sizing

- FAQs, definitions: 128–256 tokens — atomic answers, high precision
- Technical documentation: 256–512 tokens — balance precision/context
- Narratives, reports: 512–1024 tokens — preserves narrative coherence
- Source code: per function/class — natural semantic unit

### 1.2 Splitting methods

- Semantic: by paragraph, logical section, Markdown headings
- Sliding window: 20–30% overlap to avoid context breaks
- Recursive hierarchy: ordered separators (\n\n → \n → . → )
- Hybrid: semantic first, then split if chunk > threshold

### 1.3 Required contextual enrichment

Each chunk should carry its context:
```yaml
chunk:
  content: "Chunk text..."
  metadata:
    doc_title: "Security Policy 2024"
    section: "3.2 - Incident Management"
    source_type: "policy"  # policy | procedure | kb | email | chat
    domain: "cybersecurity"
    tags: ["incident-response", "phishing", "SOC"]
    date_created: "2024-01-15"
    author: "Security Team"
    chunk_index: 3
    total_chunks: 12
```
