# Cache and CDN Security
English: Cache & CDN Security
- Entry Count: 3
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Cache Poisoning
- ID: cache-poisoning
- Difficulty: advanced
- Subcategory: Cache poisoning
- Tags: cache, poisoning, web-cache
- Original Extracted Source: original extracted web-security-wiki source/cache-poisoning.md
Description:
Web cache-poisoning attack
Prerequisites:
- The target uses caching
- The cache key is misconfigured
Execution Outline:
1. Probe the cache
2. Untyped header
3. Cache poisoning
4. Fat GET
## Cache Deception
- ID: cache-deception
- Difficulty: intermediate
- Subcategory: Deception
- Tags: cache, deception, auth
- Original Extracted Source: original extracted web-security-wiki source/cache-deception.md
Description:
Exploit differences between web caching and server path parsing to induce the CDN/cache layer to cache a dynamic page containing sensitive information
Prerequisites:
- The target uses a CDN or reverse-proxy cache
- Path parsing differs (the back end ignores the path suffix)
- The caching policy is based on the URL extension
Execution Outline:
1. Probe the caching behavior
2. Path-confusion cache deception
3. Advanced cache-deception variants
4. Full-attack-flow verification
## CDN Bypass
- ID: cdn-bypass
- Difficulty: intermediate
- Subcategory: CDN
- Tags: cdn, bypass, recon
- Original Extracted Source: original extracted web-security-wiki source/cdn-bypass.md
Description:
Bypass the CDN to find the real IP
Prerequisites:
- The target uses a CDN
Execution Outline:
1. Historical DNS
2. Mail headers
3. DNS-history and certificate-transparency queries
4. Probe the real IP via subdomains and related services

