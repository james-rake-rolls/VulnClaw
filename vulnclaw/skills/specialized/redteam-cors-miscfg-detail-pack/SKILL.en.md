---
name: redteam-cors-miscfg-detail-pack
description: "Domain routing and boundary guidance for authorized CORS misconfiguration testing, including reflected origins, null origins, subdomain trust, and credential exposure. Use when a task belongs to the CORS testing domain and needs scope, evidence, pivot, or exit criteria."
---

# CORS Misconfiguration Testing

## Domain

Currently operating in the CORS-misconfiguration testing domain.
You are performing CORS configuration-security testing. The scope is limited to cross-origin resource-sharing misconfigurations (including Origin reflection, null allowance, subdomain trust, credential leakage, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| Origin reflection | Arbitrary Origin echoed back |
| null allowed | sandbox-iframe exploitation |
| Subdomain trust | XSS+CORS combination |
| Wildcard + credentials | Contradictory-config exploitation |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not use the CORS flaw to steal real user data.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the Origin allowlist is strict, try subdomains, special prefixes/suffixes, and a null Origin.
- If the credentials flag is absent, assess whether non-sensitive data can still be leaked.
- If preflight requests are blocked, check whether a simple request bypasses it.
- If every endpoint's CORS configuration is secure, fall back to the parent knowledge base and reselect a testing direction.
- Strict allowlist → null Origin → subdomain XSS → prefix matching → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The malicious-Origin request and the response headers (Access-Control-Allow-*).
- A cross-origin data-read PoC.
- An assessment of the data that can be leaked.

When the vulnerability cannot be proven, submit a negative report: the list of endpoints tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
