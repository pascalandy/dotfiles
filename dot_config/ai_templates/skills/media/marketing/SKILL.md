---
name: marketing
description: Full-stack SaaS marketing -- strategy and research, SEO, conversion optimization, content creation, demand generation, and revenue operations across 34 specialized domains routed automatically based on intent.
keywords: [marketing, seo, cro, copywriting, content-strategy, email-sequence, cold-email, lead-magnets, paid-ads, ad-creative, launch-strategy, pricing, analytics, churn, referral, revops, sales-enablement, competitor, psychology, positioning]
---

# Marketing

> Six marketing specialists in one unified skill -- from strategic foundations to SEO to conversion optimization to demand generation, routed automatically based on what you need.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Marketing a SaaS product requires dozens of distinct specialties. SEO audits demand different expertise than writing cold emails. Optimizing a signup flow requires different frameworks than planning a launch strategy. Pricing research uses different methods than building a sales deck. When you bring a marketing problem to an AI, you get a generalist response that lacks the depth, frameworks, and reference material that serious marketing demands. You end up:

- **Getting surface-level advice** -- helpful but generic, without structured methodologies for the specific marketing domain
- **Missing the connections** -- SEO recommendations that ignore CRO impact, copy that doesn't account for buyer psychology, campaigns without proper tracking
- **Repeating context** -- explaining your product, audience, and positioning from scratch every time
- **Lacking reference material** -- no access to proven frameworks, templates, benchmarks, or examples
- **Mixing concerns** -- wanting a pricing analysis but getting copy suggestions, or wanting ad creative but getting strategy lectures

The fundamental issue: marketing is not one skill. It is at least six distinct disciplines with 34 specialized domains, each with its own methodology, and an AI needs explicit structure to deploy the right one.

---

## The Solution

The Marketing skill provides six specialized sub-skills covering the full SaaS marketing lifecycle:

1. **Strategy** -- Product positioning, customer research (transcript analysis, digital watering hole research, persona generation), 50+ marketing psychology mental models, and a library of 139 proven marketing ideas. The strategic foundation all other marketing builds on.

2. **SEO** -- Technical SEO audits (crawlability, indexation, Core Web Vitals, on-page), AI search optimization (getting cited by ChatGPT, Perplexity, AI Overviews), schema markup implementation, programmatic SEO at scale, and site architecture planning.

3. **CRO** -- Conversion rate optimization across every surface: marketing pages, signup flows, post-signup onboarding, forms, popups/modals, in-app paywalls, and A/B test design with statistical rigor.

4. **Content** -- Conversion copywriting with page structure frameworks, systematic copy editing (Seven Sweeps), content strategy with pillar/cluster planning, and social media content creation across LinkedIn, Twitter/X, Instagram, and TikTok.

5. **Acquisition** -- Demand generation through email sequences (welcome, nurture, re-engagement), cold email outreach, lead magnet strategy, paid advertising across all platforms, ad creative generation at scale, product launch planning, and free tool strategy.

6. **Revenue** -- Revenue operations (lead lifecycle, scoring, routing, pipeline, CRM automation), sales enablement (decks, one-pagers, objection handling, demo scripts), competitor comparison pages, pricing strategy, analytics tracking, churn prevention, and referral programs.

The collection `SKILL.md` loads `references/ROUTER.md`, which routes requests to the right sub-skill based on keyword matching. Each sub-skill has its own `SKILL.md` and supporting reference documents.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | Dispatches requests to the right marketing domain |
| Strategy skill | `references/Strategy/MetaSkill.md` | Positioning, research, psychology, ideation |
| Strategy references | `references/Strategy/references/` | Source guides, 139 ideas by category |
| SEO skill | `references/SEO/MetaSkill.md` | Audits, AI SEO, schema, programmatic SEO, site architecture |
| SEO references | `references/SEO/references/` | 8 reference files (ranking factors, patterns, playbooks, templates) |
| CRO skill | `references/CRO/MetaSkill.md` | Pages, signup, onboarding, forms, popups, paywalls, testing |
| CRO references | `references/CRO/references/` | Experiment ideas, sample size guide, test templates |
| Content skill | `references/Content/MetaSkill.md` | Copywriting, editing, strategy, social content |
| Content references | `references/Content/references/` | Copy frameworks, transitions, plain English, CMS, social templates |
| Acquisition skill | `references/Acquisition/MetaSkill.md` | Email, cold outreach, lead magnets, ads, launches, tools |
| Acquisition references | `references/Acquisition/references/` | 16 reference files (templates, benchmarks, specs, frameworks) |
| Revenue skill | `references/Revenue/MetaSkill.md` | RevOps, sales, competitors, pricing, analytics, churn, referrals |
| Revenue references | `references/Revenue/references/` | 19 reference files (playbooks, templates, models, implementations) |

**Summary:**
- **Sub-skills:** 6 (Strategy, SEO, CRO, Content, Acquisition, Revenue)
- **Source domains covered:** 34 specialized marketing areas
- **Reference documents:** 57 supporting files (frameworks, templates, benchmarks, examples)
- **Dependencies:** None (works standalone)

---

## Shared Foundation: Product Marketing Context

All sub-skills check for `.agents/product-marketing-context.md` before asking questions. This document captures foundational positioning and messaging -- product overview, target audience, personas, pain points, competitive landscape, differentiation, objections, customer language, brand voice, proof points, and goals.

If it doesn't exist, the Strategy sub-skill creates it. Once created, every other sub-skill uses it automatically so you never repeat foundational context.

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "help me position my product" | Routes to Strategy -- Product Marketing Context workflow |
| "analyze these customer interview transcripts" | Routes to Strategy -- Customer Research, Mode 1 |
| "what marketing ideas should I try" | Routes to Strategy -- Marketing Ideas with 139 proven tactics |
| "audit my site's SEO" | Routes to SEO -- full technical and on-page audit |
| "optimize for AI search" | Routes to SEO -- AI SEO three-pillar optimization |
| "add schema markup to my blog" | Routes to SEO -- Schema Markup implementation |
| "this landing page isn't converting" | Routes to CRO -- Page CRO seven-dimension analysis |
| "our signup completion rate is low" | Routes to CRO -- Signup Flow optimization |
| "write copy for my homepage" | Routes to Content -- Copywriting with page structure frameworks |
| "review and improve this copy" | Routes to Content -- Copy Editing Seven Sweeps |
| "what should I write about" | Routes to Content -- Content Strategy with pillar planning |
| "create a LinkedIn content calendar" | Routes to Content -- Social Content |
| "build a welcome email sequence" | Routes to Acquisition -- Email Sequences |
| "write cold outreach emails" | Routes to Acquisition -- Cold Email |
| "plan our Product Hunt launch" | Routes to Acquisition -- Launch Strategy |
| "set up Google Ads campaigns" | Routes to Acquisition -- Paid Ads |
| "design our lead scoring model" | Routes to Revenue -- RevOps |
| "create a sales pitch deck" | Routes to Revenue -- Sales Enablement |
| "build a competitor comparison page" | Routes to Revenue -- Competitor Pages |
| "how should we price our product" | Routes to Revenue -- Pricing Strategy |
| "set up GA4 tracking" | Routes to Revenue -- Analytics Tracking |
| "reduce our churn rate" | Routes to Revenue -- Churn Prevention |

---

## Example Usage

### Strategic Foundation

```
User: help me set up product marketing context for my SaaS

AI responds:
Routing to Strategy -- Product Marketing Context...

Checking for existing .agents/product-marketing-context.md...
Not found. I'll study your codebase and draft a V1.

[Reads README, landing pages, marketing copy]
[Drafts all 12 sections based on findings]

Here's the draft context document. What needs correcting? What's missing?
```

### SEO Audit

```
User: my organic traffic dropped 40% last month

AI responds:
Routing to SEO -- SEO Audit...

Starting with the highest-impact checks:
1. Crawlability & Indexation -- checking robots.txt, sitemap, noindex tags
2. Technical Foundations -- Core Web Vitals, HTTPS, mobile
3. On-Page -- title tags, meta descriptions, heading structure
4. Content Quality -- E-E-A-T signals, thin content

[Produces prioritized audit report with specific fixes]
```

### Conversion Optimization

```
User: our pricing page has a 2% conversion rate

AI responds:
Routing to CRO -- Page CRO (Pricing Page)...

Analyzing across seven dimensions:
1. Value Proposition Clarity -- can visitors understand plan differences?
2. Headline -- does it address "which plan is right for me?"
3. CTA hierarchy -- is the recommended plan obvious?

Quick Wins: [immediate changes]
High-Impact Changes: [bigger improvements]
Test Ideas: [hypotheses to A/B test]
```

---

## Configuration

No configuration required. All six sub-skills work immediately.

Optional: Create `.agents/product-marketing-context.md` via the Strategy sub-skill to provide shared context across all marketing domains.

---

## Credits

- **Original skills:** Corey Haines -- [Marketing Skills](https://github.com/coreyhaines31/marketing-skills) collection of 34 specialized marketing skills
- **Meta-skill structure:** Hierarchical routing pattern with progressive disclosure
