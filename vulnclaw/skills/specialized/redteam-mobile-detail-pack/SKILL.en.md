---
name: redteam-mobile-detail-pack
description: "Domain routing and boundary guidance for authorized mobile application security testing, including insecure storage, certificate pinning bypass, exposed components, and binary reverse engineering. Use when a task belongs to the mobile testing domain and needs scope, evidence, pivot, or exit criteria."
---

# Mobile Application Security Testing

## Domain

Currently operating in the mobile-application-security testing domain.
You are performing mobile-application security testing. The scope is limited to mobile-side vulnerabilities (including insecure storage, certificate-pinning bypass, component exposure, binary reverse-engineering, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| Insecure storage | Cleartext in SharedPrefs / Keychain |
| Certificate bypass | SSL-pinning hook |
| Component exposure | exported Activity / Provider |
| Binary reverse-engineering | Hardcoded keys / algorithms |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not distribute a maliciously modified version of the app.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If root/jailbreak detection is present, use Frida bypass, Magisk Hide, and Objection hooks.
- If certificate pinning is used, dynamically hook SSL validation and use a custom trust store.
- If the code is obfuscated, use jadx/Ghidra static analysis and runtime-hook key methods.
- If every mobile-side security measure is sound, fall back to the parent knowledge base and reselect a testing direction.
- Root detection → Frida bypass → certificate hook → static analysis → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The reproduction steps (including the Frida script or operation sequence).
- Screenshots proving the data leak / bypass.
- An impact assessment (extent of user-data exposure).

When the vulnerability cannot be proven, submit a negative report: the list of surfaces tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
