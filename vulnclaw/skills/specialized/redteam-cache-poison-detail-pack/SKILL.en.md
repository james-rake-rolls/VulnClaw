---
name: redteam-cache-poison-detail-pack
description: "Domain routing and boundary guidance for authorized web cache poisoning testing, including unkeyed headers, unkeyed parameters, cache deception, and CDN-specific behavior. Use when a task belongs to the cache poisoning domain and needs scope, evidence, pivot, or exit criteria."
---

# Cache Poisoning Testing

## Domain

Currently operating in the cache-poisoning testing domain.
You are performing web cache-poisoning testing. The scope is limited to cache-poisoning attacks (including unkeyed header/parameter poisoning, cache deception, CDN-specific flaws, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| Header poisoning | X-Forwarded-Host injection |
| Parameter poisoning | Unkeyed query parameters |
| Cache deception | Path confusion to steal responses |
| CDN discrepancy | Origin and CDN use different cache keys |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not perform persistent poisoning against a production cache.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the cache key cannot be determined, use Param Miner or manually fuzz unkeyed inputs.
- If the cache is not hit, adjust the cache-buster parameter and check the Vary header.
- If the CDN layer's caching rules differ, test the origin and CDN behavior separately for discrepancies.
- If all caching behavior is safe, fall back to the parent knowledge base and reselect a testing direction.
- No unkeyed input → Param Miner fuzzing → cache-deception paths → CDN-layer testing → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The poisoning request (including the unkeyed input).
- Proof that a victim request receives the poisoned response.
- The cache persistence time and the impact scope.

When the vulnerability cannot be proven, submit a negative report: the list of cache points tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
