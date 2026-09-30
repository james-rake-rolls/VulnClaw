---
name: redteam-xxe-detail-pack
description: "Domain routing and boundary guidance for authorized XXE testing, including file read, SSRF, blind XXE, and parameter entity variants. Use when a task belongs to the XXE domain and needs scope, evidence, pivot, or exit criteria."
---

# XXE (XML External Entity Injection) Testing

## Domain

Currently operating in the XXE (XML external entity injection) testing domain.
You are performing XXE vulnerability testing. The scope is limited to XML external-entity injection (including file read, SSRF, blind XXE, parameter entities, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

| Variant | Typical scenario |
|------|---------|
| Classic XXE | External-entity file read |
| Blind XXE | OOB data exfiltration |
| Parameter entities | Nested exploitation within the DTD |
| XInclude | Injection in a non-DTD context |
| SVG/DOCX XXE | Triggered via file upload |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not use XXE to read system files outside the current target.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the DTD is disabled, try XInclude and embedding entities in SVG/XSLT.
- If external entities are blocked, try parameter entities and local-DTD overriding.
- If there is no echo, use blind XXE with OOB HTTP/FTP/DNS exfiltration.
- If the XML parser is strict, try encoding variants (UTF-16/UTF-7) and a BOM header.
- If every XML entry point is secure, fall back to the parent knowledge base and reselect a testing direction.
- DTD disabled → XInclude → SVG upload → blind XXE OOB → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete HTTP request (including the XXE payload XML).
- Proof of entity resolution (file content / SSRF callback / OOB data).
- A readability assessment (filesystem / internal network / cloud metadata).

When the vulnerability cannot be proven, submit a negative report: the list of XML entry points tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
