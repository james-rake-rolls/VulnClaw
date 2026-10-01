---
name: redteam-api-detail-pack
description: "Domain routing and boundary guidance for authorized API security testing, including BOLA/IDOR, authentication bypass, mass assignment, missing rate limits, and GraphQL issues. Use when a task belongs to the API testing domain and needs scope, evidence, pivot, or exit criteria."
---

# API Security Testing

## Domain

Currently operating in the API-security-testing domain.
You are performing API security testing. The scope is limited to API vulnerabilities (including BOLA/IDOR, authentication bypass, mass assignment, missing rate limiting, GraphQL flaws, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| BOLA/IDOR | Horizontal privilege escalation |
| Mass assignment | Privilege escalation via unfiltered fields |
| Authentication bypass | JWT/token weaknesses |
| GraphQL | Nested queries / information disclosure |
| Missing rate limiting | Enumeration / brute force |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not delete or modify production data.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If endpoint authorization is strict, enumerate hidden endpoints, try low-privilege authorization bypass, and check older API versions.
- If parameters are unknown, fuzz common parameter names, analyze front-end JS, and check OpenAPI/Swagger docs.
- If rate limiting is present, rotate tokens, lower the request rate, and try batch endpoints.
- If GraphQL introspection is disabled, use field suggestions and error messages to leak the schema.
- If no entry point is exploitable, fall back to the parent knowledge base and reselect a testing direction.
- Strict authorization → hidden endpoints → older API versions → front-end analysis → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete HTTP request (including the payload).
- Proof of a successful authorization bypass / disclosure.
- The vulnerability type and a brief impact summary.

When the vulnerability cannot be proven, submit a negative report: the list of endpoints tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
