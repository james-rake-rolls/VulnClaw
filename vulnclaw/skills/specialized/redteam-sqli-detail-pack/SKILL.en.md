---
name: redteam-sqli-detail-pack
description: "Domain routing and boundary guidance for authorized SQL injection testing, including union-based, blind, error-based, stacked query, and second-order SQL injection variants. Use when a task belongs to the SQL injection domain and needs scope, evidence, pivot, or exit criteria."
---

# SQL Injection Testing

## Domain

Currently operating in the SQL-injection testing domain.
You are performing SQL-injection vulnerability testing. The scope is limited to SQL injection (including union-based, blind, error-based, stacked-query, and second-order variants). Choose injection points and payloads autonomously.
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

| Variant | Typical scenario |
|------|---------|
| Union-based (UNION) | Controllable column count in the SELECT |
| Boolean-based blind | Judged by page differences |
| Time-based blind | SLEEP/BENCHMARK delay |
| Error-based | extractvalue / updatexml |
| Stacked queries | Multi-statement execution |
| Second-order | Triggered after storage |
| OOB exfiltration | DNS/HTTP callback |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not run irreversible destructive SQL such as DROP/TRUNCATE.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If a WAF / keyword filter is present, try encoding bypass (double URL encoding, Unicode), comment splitting, mixed case, and inline comments.
- If parameterized queries leave no injection point, switch to other parameters (headers, cookies, JSON fields, path segments).
- If no entry point is injectable, fall back to the parent knowledge base and reselect a testing direction.
- Do not repeatedly retry the same failed payload variant.
- WAF block → encoding bypass → switch injection point → switch parameter position → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete HTTP request (including the injection payload).
- The corresponding response (indicators that the SQL executed: data leakage / error message / timing difference).
- The injection type (union / blind / error-based / stacked) and a brief impact summary.

When the vulnerability cannot be proven, submit a negative report: the list of injection points tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
