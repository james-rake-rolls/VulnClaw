---
name: redteam-deserialize-detail-pack
description: "Domain routing and boundary guidance for authorized insecure deserialization testing, including Java, PHP, Python, .NET, and gadget-chain analysis. Use when a task belongs to the deserialization testing domain and needs scope, evidence, pivot, or exit criteria."
---

# Deserialization Vulnerability Testing

## Domain

Currently operating in the deserialization vulnerability-testing domain.
You are performing deserialization vulnerability testing. The scope is limited to insecure deserialization (including Java/PHP/Python/.NET deserialization, gadget-chain construction, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|----------|--------|
| Java | Commons-Collections/JNDI |
| PHP | __wakeup/__destruct chain |
| Python | pickle/yaml.load |
| .NET | TypeNameHandling/BinaryFormatter |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not perform destructive operations via RCE.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the serialization format is unknown, check magic bytes (AC ED 00 05 = Java, O:/a: = PHP) and base64 in cookies/parameters.
- If a known gadget is unavailable, try chains for different library versions, JNDI injection, and secondary deserialization.
- If a WAF blocks the payload, use encoding variants, chunked transfer, and Content-Type confusion.
- If every deserialization point is secure, fall back to the parent knowledge base and reselect a testing direction.
- Gadget unavailable → switch chain → JNDI injection → blind probing (time-delay) → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete request (including the serialized payload).
- Proof of RCE / file read / SSRF execution.
- The gadget chain used and an impact assessment.

When the vulnerability cannot be proven, submit a negative report: the list of deserialization points tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
