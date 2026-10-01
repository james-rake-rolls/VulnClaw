---
name: redteam-auth-detail-pack
description: "Domain routing and boundary guidance for authorized authentication, authorization, and session security testing, including password policy, JWT/token, OAuth, and MFA bypass issues. Use when a task belongs to the auth testing domain and needs scope, evidence, pivot, or exit criteria."
---

# Authentication & Authorization Vulnerability Testing

## Domain

Currently operating in the authentication-and-authorization vulnerability-testing domain.
You are performing authentication and session-security testing. The scope is limited to authentication-mechanism vulnerabilities (including password policy, session management, JWT/tokens, OAuth, MFA bypass, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|---------|--------|
| Weak password policy | Brute force / credential stuffing |
| JWT weaknesses | alg:none / key confusion |
| OAuth weaknesses | redirect_uri tampering / CSRF |
| Session fixation | Session unchanged across login |
| MFA bypass | State skipping / race condition |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not perform lockout attacks against real user accounts.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If login is rate-limited, rotate IPs, attempt distributed low-rate tries, and try other authentication endpoints.
- If JWT signature validation is strict, check alg:none, key confusion (RS→HS), kid injection, and jwk injection.
- If MFA is enabled, check for MFA bypass (state skipping, backup-code leakage, race conditions).
- If session management is secure, check for session fixation, token leakage, and concurrent-session controls.
- If every authentication flow is secure, fall back to the parent knowledge base and reselect a testing direction.
- Do not repeatedly retry the same failed attack vector.
- Rate limiting → switch endpoints → JWT attacks → OAuth flow → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete authentication-bypass request chain.
- Proof of a successful bypass (obtained session / access to a protected resource).
- The vulnerability type and its impact scope.

When the vulnerability cannot be proven, submit a negative report: the list of authentication points tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
