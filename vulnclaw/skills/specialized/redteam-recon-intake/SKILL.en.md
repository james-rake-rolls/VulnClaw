---
name: redteam-recon-intake
description: "Recon intake skill for first contact with a bare domain, URL, or IP address. Use to build an initial recon_profile and provide factual inputs for CVE lookup and attack-path routing."
---

# Recon Intake

## Domain

The reconnaissance entry point for the first time a bare domain / URL / IP enters a security assessment.
Responsible for building the target asset profile (recon_profile) from scratch, providing a factual basis for subsequent CVE lookup and attack-path assignment.

Phase order:
1. DNS resolution + liveness probing
2. Port scanning + service fingerprinting
3. Subdomain enumeration
4. Web directory / sensitive-file probing
5. WAF/CDN identification
6. Tech-stack fingerprinting (CMS / framework / middleware versions)

## Boundaries

- Do not perform any active exploitation.
- Do not send destructive requests (DELETE/DROP/shutdown).
- Probe only the current target; do not automatically expand to related domains/IPs not present in the task.
- Do not perform brute forcing or password spraying.
- Do not bypass rate limiting (if throttled, slow down or pause).
- Reconnaissance depth stops at information gathering; do not enter the vulnerability-verification phase.

## Pivot Hints

- WAF/CDN blocks direct connection → try historical DNS, email headers, and certificate search to obtain the real IP.
- Subdomain enumeration is limited → certificate-transparency logs, DNS zone transfer, related-domain reverse lookup.
- Directory scanning is blocked → slow down, rotate User-Agent, use a custom wordlist.
- All ports filtered → check IPv6, try common high ports, confirm the target is alive.
- Information gathering is saturated → organize what you have, output the recon_profile, and advance to the next phase.

## Exit Evidence

- Required: recon_profile, port_scan_result, service_fingerprint
- min_attempts: 4
