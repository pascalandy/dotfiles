# Blog Platform Constitution

## Core Principles

### I. Content-First

All design and technical decisions prioritize content readability and discoverability. No feature shall compromise the reading experience. Typography, whitespace, and load times serve the content.

### II. Performance Budget

- First Contentful Paint: < 1.5s on 3G
- Core Web Vitals: all green
- Total page weight: < 500KB (excluding images)
- Images: lazy-loaded, responsive, WebP/AVIF with fallbacks

### III. Accessibility (NON-NEGOTIABLE)

WCAG 2.1 AA compliance mandatory. All interactive elements keyboard-navigable. Semantic HTML required. Color contrast ≥ 4.5:1 for text. Screen reader testing before each release.

### IV. SEO & Discoverability

- Semantic markup (article, header, nav, main, footer)
- Open Graph + Twitter Cards on all pages
- Structured data (JSON-LD) for articles
- Canonical URLs, proper meta descriptions
- RSS feed for all content types

### V. Simplicity

- Static generation preferred (SSG)
- Minimal JavaScript (< 50KB gzipped for core)
- No build-time frameworks unless justified
- Markdown as content source of truth

## Content Standards

- One canonical source for each article (no duplication)
- Frontmatter schema enforced: title, date, author, tags, description
- Images stored alongside content (co-located)
- Draft/published workflow with preview capability

## Development Workflow

- Feature branches from main
- Preview deployments for each PR
- Lighthouse CI gates (performance ≥ 90, a11y = 100)
- Content changes require no code review (trusted authors)

## Governance

Constitution supersedes style preferences. Amendments require:

1. Written rationale with user impact analysis
2. Performance/accessibility impact assessment
3. Migration plan for existing content

**Version**: 1.0.0 | **Ratified**: 2025-01-01 | **Last Amended**: 2025-01-01
