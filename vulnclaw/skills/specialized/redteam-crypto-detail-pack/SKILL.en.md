---
name: redteam-crypto-detail-pack
description: "Domain routing and boundary guidance for authorized cryptography weakness testing, including weak algorithms, padding oracles, key management errors, insecure randomness, and hash collision risks. Use when a task belongs to the cryptography testing domain and needs scope, evidence, pivot, or exit criteria."
---

# Cryptographic Weakness Testing

## Domain

Currently operating in the cryptographic-weakness testing domain.
You are performing cryptographic-implementation vulnerability testing. The scope is limited to cryptographic flaws (including weak algorithms, padding oracles, key management, insecure randomness, hash collisions, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| Weak algorithms | Use of DES/RC4/MD5 |
| Padding oracle | CBC padding leakage |
| ECB mode | Block-reordering attacks |
| Weak randomness | Predictable tokens |
| Hardcoded keys | Source / config leakage |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not attempt to crack keys of systems outside the current target.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the algorithm looks secure, check implementation details (ECB mode, fixed IV, key reuse).
- If decryption cannot be observed directly, try a padding oracle (error-message differences / timing differences).
- If key storage is unreachable, check config files, environment variables, and hardcoded values.
- If every cryptographic implementation is secure, fall back to the parent knowledge base and reselect a testing direction.
- Algorithm secure → check implementation → padding oracle → key management → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- A description of the cryptographic flaw and the exploitation steps.
- Proof of a successful decryption / forgery / collision.
- An impact assessment (what can be forged / what data can be decrypted).

When the vulnerability cannot be proven, submit a negative report: the list of crypto points tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
