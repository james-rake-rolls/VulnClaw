---
name: redteam-web-detail-pack
description: "Routing and boundary guidance for authorized general web application security testing. Use as a web testing router when the attack surface should be dispatched to more specific web vulnerability skills."
---

# Comprehensive Web Penetration Testing

## Domain

Currently operating in the comprehensive-web-penetration-testing domain.
You are performing comprehensive web-application security testing. This skill acts as the web-testing routing layer, dispatching to specific sub-domain skills based on the attack surface discovered.
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|----------|
| SQL injection | redteam-sqli-detail-pack |
| XSS | redteam-xss-detail-pack |
| SSRF | redteam-ssrf-detail-pack |
| SSTI | redteam-ssti-detail-pack |
| Command injection | redteam-cmdi-detail-pack |
| XXE | redteam-xxe-detail-pack |
| File operations | redteam-file-detail-pack |
| Authentication | redteam-auth-detail-pack |
| CSRF | redteam-csrf-detail-pack |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not skip the sub-domain skills and jump straight into a deep attack.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the attack surface is unclear, first complete thorough reconnaissance (endpoint enumeration, tech-stack identification).
- If there are multiple potential vulnerability types, dispatch to sub-domain skills one by one in risk-priority order.
- If a sub-domain skill reports negative, switch to the next-priority direction.
- If every direction is negative, produce a summary report and fall back to the parent.
- Attack surface unclear → reconnaissance first → dispatch sub-domains by risk → switch direction on a negative sub-domain → summarize and fall back.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The attack-surface enumeration results.
- A summary of each sub-domain skill's test results.
- The final vulnerability finding or negative report.

As the routing layer, aggregate the sub-domain skills' output into a comprehensive report.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
