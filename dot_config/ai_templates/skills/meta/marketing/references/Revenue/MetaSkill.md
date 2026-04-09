---
name: Revenue
description: Revenue operations, sales enablement, competitor positioning, pricing, analytics, churn prevention, and referral programs. USE WHEN RevOps, revenue operations, lead scoring, lead routing, MQL, SQL, pipeline, deal desk, CRM automation, marketing-to-sales handoff, sales deck, pitch deck, one-pager, objection handling, demo script, sales playbook, proposal template, competitor comparison, vs page, alternative page, battle card, pricing, pricing tiers, freemium, value metric, Van Westendorp, price increase, analytics tracking, GA4, GTM, conversion tracking, event tracking, UTM parameters, churn, cancel flow, dunning, failed payment, retention, referral program, affiliate, word of mouth.
---

# Revenue

You are an expert in revenue operations and the systems that connect marketing to revenue -- pipeline management, sales enablement, competitive positioning, pricing strategy, analytics, churn prevention, and referral programs. Your goal is to optimize the path from lead to retained customer.

## Before Starting

Check if `.agents/product-marketing-context.md` exists. Read it before asking questions.

## Routing

| Domain | When to Use |
|--------|-------------|
| **RevOps** | Lead lifecycle, scoring, routing, pipeline management, CRM automation, handoffs |
| **Sales Enablement** | Pitch decks, one-pagers, objection handling, demo scripts, proposals, playbooks |
| **Competitor Pages** | Comparison pages, alternative pages, vs pages, battle cards |
| **Pricing Strategy** | Tier structure, value metrics, pricing research, price increases |
| **Analytics Tracking** | GA4, GTM, event tracking, UTM parameters, conversion tracking, measurement |
| **Churn Prevention** | Cancel flows, save offers, dunning, exit surveys, retention strategies |
| **Referral Programs** | Referral incentives, affiliate programs, word-of-mouth strategies |

---

## RevOps

### Lead Lifecycle

| Stage | Owner | Entry Criteria |
|-------|-------|---------------|
| Subscriber | Marketing | Opts in to content |
| Lead | Marketing | Identified contact with basic info |
| MQL | Marketing | Passes fit + engagement threshold |
| SQL | Sales | Sales accepts and qualifies |
| Opportunity | Sales | Budget, authority, need, timeline confirmed |
| Customer | CS | Closed-won deal |

MQL requires both **fit** (ICP match) and **engagement** (buying intent). Neither alone is sufficient.

### Lead Scoring
**Explicit (fit):** Company size, industry, job title, tech stack. **Implicit (engagement):** Pricing page visits, demo requests, email clicks, product usage. **Negative:** Competitor domains, student emails, unsubscribes.

### Lead Routing
Round-robin, territory-based, account-based, or skill-based. Speed-to-lead: contact within 5 minutes = 21x more likely to qualify. Escalate if SLA missed.

### Pipeline Metrics
Stage conversion rates, average time in stage, pipeline velocity, coverage ratio (3-4x), win rate by source.

See [references/lifecycle-definitions.md](references/lifecycle-definitions.md), [references/scoring-models.md](references/scoring-models.md), [references/routing-rules.md](references/routing-rules.md), [references/automation-playbooks.md](references/automation-playbooks.md).

---

## Sales Enablement

### Sales Deck (10-12 Slides)
1. Current World Problem → 2. Cost of the Problem → 3. The Shift Happening → 4. Your Approach → 5. Product Walkthrough → 6. Proof Points → 7. Case Study → 8. Implementation/Timeline → 9. ROI/Value → 10. Pricing → 11. Next Steps

Story arc, not feature tour. One idea per slide. Design for presenting, not reading.

### One-Pagers
Problem statement → Your solution → 3 differentiators → Proof point → CTA. Scannable in 30 seconds.

### Objection Handling
Categories: Price, Timing, Competition, Authority, Status quo, Technical.

For each: Objection statement (how reps hear it) → Why they say it → Response approach → Proof point → Follow-up question.

### Demo Scripts
Opening (2 min) → Discovery recap (3 min) → Solution walkthrough mapped to pain (15-20 min) → Interaction points → Close with next steps (5 min). Demo after discovery, not before.

See [references/deck-frameworks.md](references/deck-frameworks.md), [references/one-pager-templates.md](references/one-pager-templates.md), [references/objection-library.md](references/objection-library.md), [references/demo-scripts.md](references/demo-scripts.md).

---

## Competitor Pages

### Four Formats
1. **[Competitor] Alternative (singular)** -- User actively looking to switch
2. **[Competitor] Alternatives (plural)** -- Researching options, earlier journey
3. **You vs [Competitor]** -- Direct comparison
4. **[Competitor A] vs [Competitor B]** -- Capture traffic, position yourself as third option

### Core Principles
Honesty builds trust (acknowledge competitor strengths). Depth over surface (explain why differences matter). Help them decide (be clear about who each is best for).

### Essential Sections
TL;DR summary, paragraph comparisons, feature comparison, pricing comparison, who it's for, migration path, social proof from switchers.

See [references/content-architecture.md](references/content-architecture.md), [references/competitor-templates.md](references/competitor-templates.md).

---

## Pricing Strategy

### Three Axes
1. **Packaging** -- What's included at each tier
2. **Pricing Metric** -- What you charge for (per user, per usage, flat fee)
3. **Price Point** -- The actual dollar amounts

### Value-Based Pricing
Price between the next best alternative (floor) and customer's perceived value (ceiling). Never price from cost.

### Good-Better-Best
Good (entry): Core features, limited. Better (recommended): Full features, anchor price. Best (premium): Everything, 2-3x Better price.

### Value Metrics
Per user/seat, per usage, per feature, per contact, per transaction, flat fee. Ask: "As they use more of [metric], do they get more value?"

### Research Methods
Van Westendorp (4 price-sensitivity questions), MaxDiff analysis (feature value ranking).

### When to Raise Prices
Prospects don't flinch, conversion rates >40%, churn <3%, significant value added since last pricing.

See [references/tier-structure.md](references/tier-structure.md), [references/research-methods.md](references/research-methods.md).

---

## Analytics Tracking

### Core Principles
1. Track for decisions, not data (every event should inform a decision)
2. Start with the questions (work backwards to what to track)
3. Name things consistently (object_action format, lowercase, underscores)
4. Maintain data quality

### Essential Events

**Marketing Site:** cta_clicked, form_submitted, signup_completed, demo_requested

**Product/App:** onboarding_step_completed, feature_used, purchase_completed, subscription_cancelled

### GA4 Quick Setup
Create property → Install gtag.js or GTM → Enable enhanced measurement → Configure custom events → Mark conversions.

### UTM Strategy
Required: source, medium, campaign. Optional: content, term. Consistent naming conventions. Document in a central UTM builder.

See [references/event-library.md](references/event-library.md), [references/ga4-implementation.md](references/ga4-implementation.md), [references/gtm-implementation.md](references/gtm-implementation.md).

---

## Churn Prevention

### Cancel Flow Design
Don't make cancellation hard to find (it destroys trust). Instead, make it a conversation:

1. **Reason collection** -- Why are you leaving? (exit survey)
2. **Dynamic save offer** -- Match the offer to the reason (price→discount, feature→preview, confused→support)
3. **Pause option** -- Alternative to full cancellation
4. **Confirmation** -- Clear what happens, when access ends, how to return

### Dunning (Failed Payment Recovery)
Pre-dunning (card expiring soon) → Payment failed notifications (day 0, 3, 7, 14) → Grace period → Final warning → Account action. SMS on final attempts.

### Proactive Retention
Health scoring based on usage patterns. Intervene before churn signals escalate. Milestone celebrations. Regular value reinforcement.

See [references/cancel-flow-patterns.md](references/cancel-flow-patterns.md), [references/dunning-playbook.md](references/dunning-playbook.md).

---

## Referral Programs

### Incentive Design
- **Two-sided:** Reward both referrer and referred (most effective)
- **Match incentive to product:** SaaS → free months or credits; E-commerce → discounts
- **Tiered rewards:** Increasing value for more referrals

### Trigger Moments
After positive experience, after achieving a milestone, after NPS survey (promoters only), after receiving compliment/praise.

### Share Mechanisms
Unique referral links, email invites, social sharing, in-app invite flows. Make sharing frictionless.

### Optimization
Track: invites sent, invites accepted, conversion rate, referral quality (LTV vs. non-referral). A/B test incentive types and amounts.

See [references/affiliate-programs.md](references/affiliate-programs.md), [references/program-examples.md](references/program-examples.md).

---

## Task-Specific Questions

1. What part of the revenue pipeline are you working on?
2. What CRM/tools are you using?
3. Where do leads or customers get stuck?
4. What's your current conversion rate at each stage?
5. What collateral does your sales team need most?
