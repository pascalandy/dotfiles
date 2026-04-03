# UbiquitousLanguage

Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms.

## Process

### 1. Scan the Conversation

Read through the conversation for domain-relevant nouns, verbs, and concepts. Look for:
- Terms that appear repeatedly
- Concepts that get explained differently each time
- Technical jargon mixed with domain terminology

### 2. Identify Problems

Flag:
- **Ambiguity** -- same word used for different concepts
- **Synonyms** -- different words used for the same concept
- **Vague terms** -- words that could mean many things
- **Overloaded terms** -- programming concepts masquerading as domain terms

### 3. Propose a Canonical Glossary

Be opinionated -- pick the best term, list others as "aliases to avoid." Do not present options; make a choice and defend it.

Rules:
- Only domain-relevant terms -- skip module names, class names, and generic programming concepts unless they carry domain meaning
- One sentence definitions maximum. Define what it IS, not what it does.
- Group terms into multiple tables when natural clusters emerge
- Show relationships with bold term names and express cardinality where obvious
- Flag conflicts explicitly with a clear recommendation in the "Flagged Ambiguities" section

### 4. Write to UBIQUITOUS_LANGUAGE.md

Create or update the file. Example of expected output:

```markdown
# Ubiquitous Language

## Billing Lifecycle

| Term | Definition | Aliases to Avoid |
|------|-----------|-----------------|
| **Order** | A customer's request to purchase one or more products. | Purchase, Transaction |
| **Invoice** | A payment request generated from a fulfilled order. | Bill, Receipt |
| **Line Item** | A single product entry within an order, with quantity and price. | Order Item, SKU Entry |

## Actors

| Term | Definition | Aliases to Avoid |
|------|-----------|-----------------|
| **Customer** | A person or organization that places orders. | User, Client, Buyer |
| **Fulfillment Agent** | The system or person responsible for preparing an order for delivery. | Shipper, Warehouse |

## Relationships

**Customer** places **Orders** (1:N).
**Order** contains **Line Items** (1:N).
**Order** generates one **Invoice** (1:1).

## Example Dialogue

> **Dev:** When a user creates a new transaction...
> **Domain Expert:** Let's call that "placing an order." The customer places an order. Each line item in the order has a quantity and unit price.
> **Dev:** And then we generate a bill?
> **Domain Expert:** An invoice. We generate an invoice from the fulfilled order. The invoice references the order but has its own lifecycle -- it can be paid, voided, or reissued.
> **Dev:** What about partial shipments?
> **Domain Expert:** An order can have multiple fulfillments. Each fulfillment covers some line items. An invoice is generated per fulfillment, not per order.

## Flagged Ambiguities

- **"Account"** is used to mean both "a customer's login credentials" and "a billing entity with payment history." Recommend: use **User Account** for authentication and **Billing Account** for financial records.
- **"Item"** is ambiguous between a product in the catalog and a line item in an order. Recommend: use **Product** for catalog entries, **Line Item** for order entries.
```

### 5. Output Summary Inline

After writing the file, present a brief summary of:
- Terms defined (count)
- Ambiguities flagged (count)
- Key decisions made

## Re-running

When invoked again:
1. Read the existing `UBIQUITOUS_LANGUAGE.md`
2. Incorporate new terms from the current conversation
3. Update definitions that have evolved
4. Re-flag any new ambiguities
5. Rewrite the example dialogue to demonstrate all key terms
