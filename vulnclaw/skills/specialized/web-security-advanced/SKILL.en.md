---
name: web-security-advanced
description: Advanced web security testing — the injection-attack family, protocol security, authentication and logic flaws, file and deployment security, and modern web attack surfaces, with complete playbooks
routing:
  target_types: [web, api]
  phases: [vuln_discovery, exploitation]
  task_types: [pentest, audit]
  vulnerability_classes:
    - sqli
    - xss
    - ssrf
    - ssti
    - xxe
    - rce
    - deserialization
    - idor
    - csrf
    - cors
    - file_upload
    - path_traversal
    - auth_bypass
    - jwt
    - oauth
    - graphql
    - websocket
    - request_smuggling
    - prototype_pollution
    - business_logic
  exclude_signals: ["无法重放", "签名阻塞", "重放被阻", "cannot replay", "signing blocker", "replay blocked"]
---

# Advanced Web Security Testing Skill

Use this skill when the target is a web application, API, gateway, or browser-facing service and systematic vulnerability testing is needed.

**Precondition**: if requests are still client-controlled and replay is not yet stable, use the `client-reverse` skill first.

## CTF scenario routing

> When the target is a CTF challenge (a flag is known to exist and a specific filter must be bypassed), prefer the `ctf-web` skill for concrete bypass values and payloads:

| CTF scenario | Route to ctf-web | Reference |
|---------|---------------|---------|
| PHP loose comparison / type juggling | `ctf-web` | `references/php-bypass-cheatsheet.md` |
| Command-injection space bypass | `ctf-web` | `references/command-injection-bypass.md` |
| eval with/without echo | `ctf-web` | `references/eval-and-rce-techniques.md` |
| PHP code audit | `ctf-web` | `references/php-code-audit-checklist.md` |
| SSTI injection chains | `ctf-web` | `references/ssti-injection-chains.md` |
| Deserialization exploit chains | `ctf-web` | `references/deserialization-playbook.md` |
| File upload → RCE | this skill | `references/web-playbook-08-file-vulnerabilities.md` |

**This skill focuses on pentest methodology**; for CTF-specific bypass values and payload templates, see `ctf-web`.

## Scenario routing

| Attack-surface type | Preferred reference |
|-----------|---------|
| Parameter injection (SQLi/XSS/command execution/SSTI/XXE) | `references/web-injection.md` |
| Protocol security (CORS/GraphQL/WebSocket/OAuth/request smuggling) | `references/web-modern-protocols.md` |
| Authentication and logic (IDOR/authorization/payment/password reset/auth bypass) | `references/web-logic-auth.md` |
| Files and infrastructure (upload/traversal/inclusion/deployment/cache/CDN/cloud) | `references/web-file-infra.md` |
| Deployment security | `references/web-deployment-security.md` |

## Testing workflow

### 1. Input-validation testing
- SQL injection: boolean / time / error / Union / stacked
- XSS: reflected / stored / DOM / CSP bypass
- Command injection: separator bypass, encoding bypass
- SSTI: template-engine identification + RCE chains
- XXE: entity injection, OOB data exfiltration
- Deserialization: Java/PHP/Python chains

### 2. Authentication and session testing
- Default credentials, brute force
- Session-management flaws (fixation / hijacking / insecure cookies)
- JWT security (algorithm tampering / key brute force / none algorithm)
- OAuth/OIDC misconfiguration
- MFA bypass

### 3. Logic-flaw testing
- Authorization bypass (horizontal / vertical)
- Business-logic bypass (payment / coupons / voting)
- Race conditions
- IDOR (insecure direct object references)

### 4. Protocol-security testing
- CORS misconfiguration
- GraphQL introspection / injection
- WebSocket authentication and injection
- HTTP request smuggling
- SSRF (internal-network probing / cloud metadata)

### 5. File and deployment security
- File-upload bypass
- Path traversal
- LFI/RFI
- CDN / cache poisoning
- Supply-chain attacks
- Cloud security configuration

## References

- `references/web-injection.md` — detailed injection-attack reference
- `references/web-modern-protocols.md` — modern-protocol security
- `references/web-logic-auth.md` — authentication and logic flaws
- `references/web-file-infra.md` — file and infrastructure security
- `references/web-deployment-security.md` — deployment security
- `references/web-ai-attack-map.md` — web and AI attack mapping
- `references/web-playbook-*.md` — individual playbooks (23 files)
