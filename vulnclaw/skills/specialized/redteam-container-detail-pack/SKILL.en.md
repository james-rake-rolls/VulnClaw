---
name: redteam-container-detail-pack
description: "Domain routing and boundary guidance for authorized container and orchestration security testing, including Docker escape, Kubernetes privilege escalation, image vulnerabilities, and service mesh bypasses. Use when a task belongs to the container testing domain and needs scope, evidence, pivot, or exit criteria."
---

# Container Security Testing

## Domain

Currently operating in the container-security-testing domain.
You are performing container-security testing. The scope is limited to container escape and orchestration-platform vulnerabilities (including Docker escape, K8s privilege escalation, image vulnerabilities, service-mesh bypass, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| Docker escape | Privileged mode / mounted volumes |
| K8s privilege escalation | RBAC / SA token |
| Image vulnerabilities | Known-CVE exploitation |
| Network policy | Unisolated pod-to-pod traffic |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not disrupt the production container-orchestration state.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the container is hardened (no privileged mode), check capabilities, mounted volumes, and proc/sys writability.
- If K8s RBAC is strict, enumerate ServiceAccount permissions and check secret readability.
- If Seccomp/AppArmor restricts syscalls, look for an exploitation path among the allowed syscalls.
- If every container configuration is secure, fall back to the parent knowledge base and reselect a testing direction.
- Non-privileged → capability checks → mount exploitation → SA enumeration → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete escape / privilege-escalation command chain.
- Proof of host access or cluster privilege escalation.
- The impact scope (reachable nodes / namespaces).

When the vulnerability cannot be proven, submit a negative report: the list of paths tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
