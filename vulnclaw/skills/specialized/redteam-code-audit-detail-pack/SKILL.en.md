---
name: redteam-code-audit-detail-pack
description: "Domain routing and boundary guidance for authorized source code security review, including dangerous function tracing, data-flow analysis, logic flaw detection, and dependency review. Use when a task belongs to the code audit domain and needs scope, evidence, pivot, or exit criteria."
---

# Code Audit

## Domain

Currently operating in the code-audit domain.
You are performing a source-code security audit. The scope is limited to white-box code auditing (including dangerous-function tracing, data-flow analysis, logic-flaw identification, third-party dependency review, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| Injection class | SQL/CMD/LDAP sinks |
| Authentication flaws | Hardcoded secrets / weak validation |
| Logic flaws | Race conditions / step skipping |
| Dependency risk | Known CVEs / supply chain |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not disclose the audited target's source code.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the codebase is huge, prioritize auditing entry points (routes / APIs / user-input handling).
- If the framework is deeply abstracted, trace its security mechanisms and look for bypass points.
- If dependencies are complex, check for known CVEs, insecure versions, and supply-chain risk.
- If no high-severity vulnerability is found, downgrade to reviewing medium/low-severity issues and report back to the parent.
- Entry points first → dangerous functions → data-flow tracing → dependency checks → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The vulnerable code location (file:line).
- The data-flow path (source → sink).
- A PoC or a description of the exploitation scenario.
- Remediation recommendations.

When no vulnerability is found, submit an audit report: the scope audited + a security assessment → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
