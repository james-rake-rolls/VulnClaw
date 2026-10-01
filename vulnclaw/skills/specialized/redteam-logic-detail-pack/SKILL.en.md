---
name: redteam-logic-detail-pack
description: "Domain routing and boundary guidance for authorized business logic vulnerability testing, including race conditions, flow bypass, price tampering, permission logic errors, and bulk operation abuse. Use when a task belongs to the logic testing domain and needs scope, evidence, pivot, or exit criteria."
---

# Business-Logic Vulnerability Testing

## Domain

Currently operating in the business-logic vulnerability-testing domain.
You are performing business-logic vulnerability testing. The scope is limited to logic flaws (including race conditions, step skipping, price tampering, authorization-logic errors, bulk-operation abuse, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| Race condition | Double submission / concurrent consumption |
| Step skipping | Payment-step bypass |
| Price tampering | Client-side amount modification |
| Authorization logic | Incomplete role checks |
| IDOR | Object-reference authorization bypass |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not cause real financial loss.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the flow is strictly validated, analyze the state machine and look for skippable intermediate steps.
- If the race window is tiny, increase concurrency and use HTTP/2 single-packet multi-request.
- If amounts/quantities are validated server-side, try negatives, very large numbers, float precision, and currency-unit confusion.
- If all business logic is secure, fall back to the parent knowledge base and reselect a testing direction.
- Strict validation → race attack → parameter tampering → flow analysis → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete sequence of operation steps.
- Proof of successful logic-flaw exploitation (balance change / privilege escalation / flow bypass).
- A business-impact assessment.

When the vulnerability cannot be proven, submit a negative report: the list of logic points tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
