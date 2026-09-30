---
name: redteam-open-redirect-detail-pack
description: "Domain routing and boundary guidance for authorized open redirect testing, including parameter redirects, meta or JavaScript redirects, and OAuth redirect_uri abuse. Use when a task belongs to the open redirect domain and needs scope, evidence, pivot, or exit criteria."
---

# Open-Redirect Testing

## Domain

Currently operating in the open-redirect testing domain.
You are performing open-redirect vulnerability testing. The scope is limited to URL-redirect bypass (including parameter redirects, Meta/JS redirects, OAuth redirect_uri exploitation, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| Parameter redirect | ?url=//evil.com |
| OAuth redirect | redirect_uri tampering |
| Meta refresh | HTML meta tag |
| JS redirect | Controllable location.href |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not use the redirect to phish real users.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If a URL allowlist is validated, try the @ symbol, backslashes, URL encoding, and double encoding.
- If relative paths are restricted, try protocol-relative URLs (//evil.com) and path traversal.
- If only same-origin is allowed, look for subdomain takeover or an open-redirect chain.
- If every redirect point is secure, fall back to the parent knowledge base and reselect a testing direction.
- Strict allowlist → URL encoding → path confusion → chained redirects → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete request URL (including the redirect payload).
- Proof of a successful redirect to an external domain.
- An exploitation-scenario assessment (OAuth-token leakage / phishing aid).

When the vulnerability cannot be proven, submit a negative report: the list of redirect points tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
