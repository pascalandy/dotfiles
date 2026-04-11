# Writing Agent Briefs

An agent brief is a structured comment posted on a GitHub issue when it transitions to `ready-for-agent`. It is the authoritative specification that an AFK agent will work from. The original issue body and discussion are context -- the agent brief is the contract.

The issue may sit in `ready-for-agent` for days or weeks. The codebase will change in the meantime. Write the brief so it stays useful even as files are renamed, moved, or refactored.

## Principles

### Durability Over Precision

- DO describe interfaces, types, and behavioral contracts
- DO name specific types, function signatures, or config shapes that the agent should look for or modify
- DO NOT reference file paths -- they go stale
- DO NOT reference line numbers
- DO NOT assume the current implementation structure will remain

### Behavioral, Not Procedural

Describe **what** the system should do, not **how** to implement it. An agent should be able to choose its own implementation approach.

Good: "The `processPayment` function should return a `PaymentResult` with status `failed` and error code `insufficient_funds` when the charge amount exceeds the account balance."

Bad: "Add an if-statement in the payment handler to check the balance before charging."

Good: "When a user uploads a CSV, the system should validate all rows before importing any. Invalid rows should be collected and reported in a single error response."

Bad: "Loop through the CSV rows and throw an error if any row is invalid."

### Complete Acceptance Criteria

Every brief must have concrete, testable acceptance criteria. Each criterion should be independently verifiable. If you cannot write a test for a criterion, it is too vague.

### Explicit Scope Boundaries

State what is out of scope. This prevents the agent from gold-plating or making assumptions about adjacent features.

## Template

```markdown
## Agent Brief

**Category:** bug / enhancement
**Summary:** [one-line description]

**Current behavior:**
[Describe what happens now. For bugs, this is the broken behavior.
For enhancements, this is the status quo the feature builds on.]

**Desired behavior:**
[Describe what should happen after the fix/feature.
Be specific about inputs, outputs, and edge cases.]

**Key interfaces:**
- `TypeName` -- what needs to change and why
- `functionName()` return type -- what it currently returns vs what it should return
- Config shape -- any new configuration options needed

**Acceptance criteria:**
- [ ] [Concrete, independently verifiable criterion]
- [ ] [Concrete, independently verifiable criterion]
- [ ] ...

**Out of scope:**
- [What this brief does NOT cover]
```

## Complete Example (Bug)

```markdown
## Agent Brief

**Category:** bug
**Summary:** Payment webhook silently drops events when signature verification fails

**Current behavior:**
When a payment webhook arrives with an invalid signature, the handler returns HTTP 200 with no logging. The payment provider considers the event delivered and never retries. The payment state becomes permanently inconsistent between provider and database.

**Desired behavior:**
When signature verification fails, the handler should return HTTP 401 and log the failure at WARN level with the event type and a truncated signature. The payment provider will then retry per its backoff schedule.

**Key interfaces:**
- `WebhookHandler` -- should distinguish between "processed successfully" (200), "signature invalid" (401), and "processing failed" (500)
- `PaymentEvent` type -- no changes needed, but the handler should log `event.type` on failure
- Logging -- use the existing structured logger, WARN level

**Acceptance criteria:**
- [ ] Invalid signature returns HTTP 401 (not 200)
- [ ] Valid signature with processing error returns HTTP 500
- [ ] WARN log entry includes event type and truncated signature (first 8 chars)
- [ ] Payment provider retries after 401 (verify via integration test or documentation reference)
- [ ] Existing valid-signature flow is unchanged

**Out of scope:**
- Changing the signature verification algorithm
- Adding a dead-letter queue for failed events
- Dashboard visibility of failed webhooks
```

## Complete Example (Enhancement)

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** Add CSV export for transaction history

**Current behavior:**
Transaction history is only viewable in the web UI with pagination. Users who need to process transactions in spreadsheets must manually copy data page by page.

**Desired behavior:**
A new "Export CSV" action on the transaction history page triggers a download of all transactions matching the current filters. The CSV includes: date, description, amount, category, and status.

**Key interfaces:**
- `TransactionQuery` type -- already supports the filters needed; the export endpoint reuses this
- New endpoint: `GET /api/transactions/export` accepting the same query params as the list endpoint
- Response: `Content-Type: text/csv` with `Content-Disposition: attachment`

**Acceptance criteria:**
- [ ] Export includes all transactions matching current filters (not just current page)
- [ ] CSV columns: date (ISO 8601), description, amount (decimal with 2 places), category, status
- [ ] Empty result produces a CSV with only the header row
- [ ] Export of 10,000+ transactions completes within 10 seconds
- [ ] Existing list endpoint behavior is unchanged

**Out of scope:**
- Other export formats (PDF, Excel)
- Scheduled/automated exports
- Export progress indicator
```

## Bad Example (And Why)

```markdown
Fix the payment bug in the handler where it doesn't handle the error correctly.
Check line 47 of processor.ts and add proper error handling.
```

This is bad because:
1. References a file path (`processor.ts`) that may move
2. References a line number (47) that will shift with any edit
3. Describes implementation ("add proper error handling") not behavior
4. No acceptance criteria
5. No scope boundaries
6. An agent cannot verify when this is "done"
