---
name: redteam-injection-detail-pack
description: "Domain routing and boundary guidance for authorized general injection testing outside SQL injection, including NoSQL, LDAP, XPath, and expression language injection. Use when a task belongs to the general injection domain and needs scope, evidence, pivot, or exit criteria."
---

# General Injection Testing

## Domain

Currently operating in the general-injection testing domain.
You are performing general injection vulnerability testing. The scope covers non-SQL injection classes (including NoSQL injection, LDAP injection, XPath injection, expression-language injection, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| NoSQL injection | MongoDB $ne/$regex |
| LDAP injection | )(|(uid=*) |
| XPath injection | ' or '1'='1 |
| EL injection | ${applicationScope} |
| Header injection | CRLF / Host injection |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not perform destructive injection operations.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the backend type is unknown, test multiple injection probes in parallel ($ne/$gt, *)(|, ' or '1'='1).
- If input is strictly filtered, use encoding bypass, Unicode-normalization differences, and HPP parameter pollution.
- If there is no echo, confirm via error-based or time-based blind injection.
- If every injection point is secure, fall back to the parent knowledge base and reselect a testing direction.
- Backend unknown → multi-probe → encoding bypass → blind-injection confirmation → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete request (including the injection payload).
- Proof of successful injection execution.
- The injection type and an impact assessment.

When the vulnerability cannot be proven, submit a negative report: the list of injection points tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
