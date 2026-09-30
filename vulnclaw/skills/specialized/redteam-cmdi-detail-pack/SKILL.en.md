---
name: redteam-cmdi-detail-pack
description: "Domain routing and boundary guidance for authorized operating system command injection testing, including direct injection, blind injection, out-of-band callbacks, and argument injection. Use when a task belongs to the command injection domain and needs scope, evidence, pivot, or exit criteria."
---

# OS Command Injection Testing

## Domain

Currently operating in the OS-command-injection testing domain.
You are performing operating-system command-injection testing. The scope is limited to command injection (including direct injection, blind injection, OOB exfiltration, argument injection, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

| Variant | Typical scenario |
|------|---------|
| Direct injection | Controllable command concatenation |
| Blind injection | Time-delay / OOB confirmation |
| Argument injection | --flag injection |
| Environment-variable injection | env override |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not run destructive system commands such as rm -rf / format.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If command separators are filtered, try newlines, $() substitution, backticks, and %0a encoding.
- If spaces are blocked, use $IFS, {cmd,arg}, or tab substitutes.
- If commands are blacklisted, use wildcards (c?t /etc/p?sswd), variable concatenation, or base64-encoded execution.
- If there is no echo, use DNS exfiltration, time-delay inference, or writing a file into the web directory.
- If no entry point is injectable, fall back to the parent knowledge base and reselect a testing direction.
- Separators blocked → switch encoding → OOB when no echo → argument injection → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete HTTP request (including the command-injection payload).
- Proof of command execution (echoed output / DNS callback / timing difference / file creation).
- The injection type and an assessment of the privilege level.

When the vulnerability cannot be proven, submit a negative report: the list of parameters tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
