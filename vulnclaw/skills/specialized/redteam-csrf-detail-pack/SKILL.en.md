---
name: redteam-csrf-detail-pack
description: "Domain routing and boundary guidance for authorized CSRF testing, including token bypasses, SameSite bypasses, and JSON CSRF. Use when a task belongs to the CSRF testing domain and needs scope, evidence, pivot, or exit criteria."
---

# CSRF (Cross-Site Request Forgery) Testing

## Domain

Currently operating in the CSRF (cross-site request forgery) testing domain.
You are performing CSRF vulnerability testing. The scope is limited to cross-site request forgery (including token bypass, SameSite bypass, JSON CSRF, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

| Variant | Typical scenario |
|------|--------|
| No token protection | Form submits directly |
| Token bypassable | Deleting/blanking it still passes |
| JSON CSRF | Content-Type restriction bypass |
| SameSite bypass | Subdomain / top-level navigation |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not launch CSRF attacks against real users.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If a CSRF token exists, check whether it is predictable, whether it is bound to the session, and whether deleting the token still passes.
- If SameSite=Strict, look for a controllable subdomain, use top-level navigation, and check for GET-request side effects.
- If Content-Type is restricted, try text/plain, multipart/form-data, and fetch redirects.
- If Referer is checked, use an empty Referer (data: URI) or substring-matching bypass.
- If every sensitive operation is fully protected, fall back to the parent knowledge base and reselect a testing direction.
- Strict token validation → SameSite bypass → Referer bypass → subdomain exploitation → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The CSRF PoC HTML (able to trigger a sensitive operation).
- Proof that the cross-origin request executed successfully.
- The affected operations and an impact assessment.

When the vulnerability cannot be proven, submit a negative report: the list of endpoints tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
