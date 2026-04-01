# Entity Lookup

Use this workflow when the seed is an IP, URL, hash, ASN, IOC, or other technical entity.

## Steps

1. Classify the entity.
Identify whether the seed is an IP, URL, hash, ASN, threat actor name, or another technical indicator.

2. Gather passive context.
Collect attribution clues, geolocation, hosting, certificates, network relationships, malware references, and reputation records appropriate to the entity type.

3. Pivot by relationship.
Expand through related domains, IP neighbors, certificates, shared hosting, related hashes, campaigns, or reports when those pivots remain relevant.

4. Check for corroboration.
A single reputation hit is not enough. Prefer multiple independent references before calling something suspicious or malicious.

5. Produce a risk-aware summary.
State whether the entity looks benign, suspicious, malicious, compromised, or inconclusive, and explain why.

## Deliverable

Return the entity classification, factual infrastructure details, threat or reputation evidence, related entities, and a confidence-rated assessment.
