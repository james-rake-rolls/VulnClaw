---
name: redteam-ssrf-detail-pack
description: "Domain routing and boundary guidance for authorized SSRF testing, including basic SSRF, blind SSRF, protocol smuggling, and cloud metadata access paths. Use when a task belongs to the SSRF domain and needs scope, evidence, pivot, or exit criteria."
---

# SSRF (Server-Side Request Forgery) Testing

## Domain

Currently operating in the SSRF (server-side request forgery) testing domain.
You are performing SSRF vulnerability testing. The scope is limited to server-side request forgery (including basic SSRF, blind SSRF, protocol smuggling, cloud-metadata access, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

| Variant | Typical scenario |
|------|---------|
| Basic SSRF | Direct internal-network access |
| Blind SSRF | OOB-callback confirmation |
| Protocol smuggling | gopher/dict exploitation |
| DNS rebinding | Allowlist bypass |
| Cloud metadata | AWS/GCP/Azure IMDSv1 |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not use SSRF to reach external systems outside the current target.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If a URL allowlist restricts you, try DNS rebinding, URL-parsing discrepancies, redirect chaining, and IPv6 mapping.
- If protocols are restricted, switch protocol (file://, gopher://, dict://) and use redirects to change protocol.
- If the internal network is unreachable, try cloud metadata (169.254.169.254) and local-service enumeration.
- If no request point is exploitable, fall back to the parent knowledge base and reselect a testing direction.
- Do not repeatedly retry the same failed bypass technique.
- Allowlist not bypassable → DNS rebinding → redirect chaining → switch protocol → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete HTTP request (including the SSRF payload URL).
- Evidence that the server made the request (internal response content / DNS callback / timing difference).
- A reachability assessment (internal segments, cloud metadata, local files).

When the vulnerability cannot be proven, submit a negative report: the list of URL parameters tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
