# Reverse Lookup

Use this workflow when the seed input is an identifier rather than a full person profile.

Supported seed types:

- phone number
- email address
- username
- profile photo or image link

## Steps

1. Classify the identifier.
Determine the seed type and normalize it before searching.

2. Search sources appropriate to that identifier.
Use phone directories for phone numbers, account-discovery and breach-aware sources for emails, username-enumeration for handles, and reverse-image tools for photos.

3. Pivot to person-level evidence.
Only move from the raw identifier to names, addresses, profiles, or relatives when the pivot stays within public data.

4. Cross-check every claimed match.
A reverse lookup result is only a lead until another independent source supports it.

5. Return evidence with caveats.
Call out recycled data-broker results, stale records, and any uncertainty caused by VoIP numbers, shared inboxes, reused usernames, or copied images.

## Deliverable

Return these sections:

```text
Seed identifier
Potential owner or account matches
Supporting sources
Secondary pivots worth checking
Confidence and caveats
```
