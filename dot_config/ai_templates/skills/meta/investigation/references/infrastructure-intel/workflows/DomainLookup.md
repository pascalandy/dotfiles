# Domain Lookup

Use this workflow when the target is a domain or subdomain and the user needs technical context.

## Steps

1. Normalize the target.
Capture the root domain, any known subdomains, and whether the request includes passive-only or deeper analysis.

2. Collect registration and DNS facts.
Gather WHOIS or registrar data when available, name servers, A and MX records, TXT records, and historical DNS if relevant.

3. Discover related surface area.
Map subdomains, certificate entries, related domains, hosting providers, IPs, and CDN or third-party dependencies.

4. Review reputation and exposure.
Check passive threat and reputation sources, screenshots, abuse references, breach mentions, and hosting context.

5. Report the infrastructure picture.
Separate hard facts from reputation signals and note what requires active confirmation outside this workflow.

## Deliverable

Return the domain profile, key subdomains, hosting and certificate facts, notable risk indicators, and the best next pivot.
