---
name: redteam-xss-detail-pack
description: "Domain routing and boundary guidance for authorized cross-site scripting testing, including reflected, stored, DOM-based, mXSS, and CSP bypass variants. Use when a task belongs to the XSS domain and needs scope, evidence, pivot, or exit criteria."
---

# XSS (Cross-Site Scripting) Testing

## Domain

Currently operating in the XSS (cross-site scripting) testing domain.
You are performing XSS vulnerability testing. The scope is limited to cross-site scripting (including reflected, stored, DOM-based, mXSS, and CSP-bypass variants).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

| Variant | Typical scenario |
|------|---------|
| Reflected XSS | URL-parameter echo |
| Stored XSS | Persisted in comments / profile |
| DOM-based XSS | JS sink/source chain |
| mXSS | Parser-differential exploitation |
| CSP bypass | JSONP / trusted-types |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not launch real phishing attacks against other users.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If input is filtered/encoded, try HTML-entity bypass, event handlers, SVG/MathML tags, and template literals.
- If CSP is strict, look for JSONP endpoints, unsafe-eval gadgets, an unrestricted base-uri, and trusted-domain resources.
- If the framework auto-escapes, look for sinks such as dangerouslySetInnerHTML / v-html / [innerHTML].
- If every reflection point is safely handled, fall back to the parent knowledge base and reselect a testing direction.
- Do not repeatedly retry the same failed payload variant.
- Filter not bypassable → switch tag/event → find a DOM sink → CSP gadget → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete HTTP request or DOM-operation steps (including the XSS payload).
- Proof of script execution (alert / console / cookie-access screenshot).
- The XSS type (reflected / stored / DOM) and a brief impact summary (session-hijacking / data-theft feasibility).

When the vulnerability cannot be proven, submit a negative report: the list of reflection points tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
