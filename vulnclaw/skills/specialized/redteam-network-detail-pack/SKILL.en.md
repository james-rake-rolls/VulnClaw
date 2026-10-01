---
name: redteam-network-detail-pack
description: "Domain routing and boundary guidance for authorized network-layer security testing, including exposed services, protocol downgrade, man-in-the-middle risks, and segmentation bypasses. Use when a task belongs to the network testing domain and needs scope, evidence, pivot, or exit criteria."
---

# Network-Layer Penetration Testing

## Domain

Currently operating in the network-layer penetration-testing domain.
You are performing network-layer security testing. The scope is limited to network vulnerabilities (including port/service exposure, protocol downgrade, man-in-the-middle, network-segmentation bypass, and similar).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|--------|
| Service exposure | Unauthorized access (Redis/MongoDB) |
| Protocol downgrade | TLS → cleartext |
| ARP/DNS spoofing | Man-in-the-middle |
| Segment traversal | Pivot-based lateral movement |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not automatically expand scanning to network segments outside the current target.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the firewall is strict, check non-standard ports, UDP services, and IPv6 dual-stack.
- If IDS/IPS blocks you, lower the scan rate, use fragmentation, and encrypted tunnels.
- If the network is segmented, look for dual-homed hosts, VPN tunnels, and management-network entry points.
- If every network configuration is secure, fall back to the parent knowledge base and reselect a testing direction.
- Firewall → non-standard ports → UDP services → IPv6 → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The network-topology discovery results.
- Proof of an exploitable service / protocol.
- The lateral-reach range and an impact assessment.

When the vulnerability cannot be proven, submit a negative report: the list of services probed + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
