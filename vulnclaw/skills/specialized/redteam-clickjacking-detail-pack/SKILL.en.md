---
name: redteam-clickjacking-detail-pack
description: "Domain routing and boundary guidance for authorized clickjacking testing, including missing X-Frame-Options, CSP frame-ancestors bypasses, and drag-and-drop hijacking. Use when a task belongs to the clickjacking domain and needs scope, evidence, pivot, or exit criteria."
---

# Clickjacking Testing

## Domain

Currently operating in the clickjacking testing domain.
You are performing clickjacking vulnerability testing. The scope is limited to clickjacking (including missing X-Frame-Options, CSP frame-ancestors bypass, drag-and-drop hijacking, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| No frame protection | Direct iframe embedding |
| Partial protection | Some paths left uncovered |
| Drag-and-drop hijack | Drag-and-drop exploitation |
| Multi-step actions | Combined multi-click sequences |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not carry out clickjacking attacks against real users.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If X-Frame-Options is set, check whether it is consistent across all pages and whether any pages are exceptions.
- If CSP frame-ancestors is used, look for subdomains or paths with inconsistent policy.
- If JavaScript defenses exist, check whether the framebusting script can be disabled via the sandbox attribute.
- If every page is fully protected, fall back to the parent knowledge base and reselect a testing direction.
- XFO present → find uncovered paths → sandbox bypass → subdomain embedding → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The clickjacking PoC HTML (an iframe embedding the target page).
- A screenshot proving the page loads inside an iframe.
- An assessment of the affected sensitive operations.

When the vulnerability cannot be proven, submit a negative report: the list of pages tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
