---
name: rapid-checklist
description: Pentest quick-reference and payloads — quick payload families, bypass reminders, verification order, and common testing cards, for fast lookup once the testing direction is known
---

# Pentest Quick-Reference & Payload Skill

**Use only after routing is decided**. This skill is for fast lookup; it does not replace methodology or workflow selection.

## When to use

- Quickly recall what to look at first for a given vulnerability class or blocker
- Quickly shortlist payload families, bypass directions, and verification order
- Quickly confirm common testing cards for AI, MCP, containers, WebSocket, JWT, files, auth, SSRF, etc.
- Move from "I know what to test" to "which class do I verify first"

## When not to use

- To replace scenario routing → use `pentest-flow`
- To replace methodology decisions → use the corresponding specialized skill
- Blind testing when requests aren't captured or replay isn't stable → use `client-reverse` first

## CTF quick-reference

> For CTF challenges, prefer the `ctf-web` / `ctf-crypto` / `ctf-misc` skills; the following are quick cards:

| Scenario | Quick locator |
|------|---------|
| PHP loose comparison → MD5 value starting with 0e | `ctf-web` → `php-bypass-cheatsheet.md` |
| Command-injection space bypass → ${IFS}/$IFS$9/< | `ctf-web` → `command-injection-bypass.md` |
| eval with no echo → write file / DNS exfiltration | `ctf-web` → `eval-and-rce-techniques.md` |
| RSA small exponent → cube root / Coppersmith | `ctf-crypto` → `rsa-attacks-cheatsheet.md` |
| Python Jail → `__import__` / func_globals | `ctf-misc` → `python-jail-escape.md` |
| Encoding chain → base64→hex→ROT13 multi-layer | `ctf-misc` → `encoding-chain-reference.md` |

## Quick routing cards

### Web injection / output execution
- SQLi → `'`, `"`, `)`, boolean difference, timing difference, error difference
- XSS → `<script>`, `<img onerror>`, `javascript:`, DOM sink
- Command injection → `;id`, `|id`, `` `id` ``, `$(id)`
- SSTI → `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`, template-engine fingerprint
- XXE → `<!ENTITY>`, parameter entities, OOB exfiltration

### Auth / logic / token
- JWT → none algorithm, algorithm tampering, key brute force, jku/x5u injection
- CSRF → missing token, predictable token, Referer-validation flaw
- IDOR → modify the ID parameter, bulk traversal
- Payment logic → amount tampering, negatives, race conditions

### Browser signing / anti-scraping
- Use `client-reverse` first to stabilize replay
- Phases: locate → recover → runtime → validation

### Android runtime / signature recovery
- Use the `client-reverse` runtime-first path first
- Reverse-engineer only when you cannot capture packets / they are encrypted / cannot be replayed

### AI / MCP
- Prompt injection → direct / indirect / CoT interference
- Tool abuse → MCP poisoning / instruction override
- Identity escape → role overreach / privilege drift

### Internal network / AD
- Use `intranet-pentest-advanced` first
- When unsure about tooling, also consult `pentest-tools`

## References

- `references/08-rapid-checklists-and-payloads.md` — integrated quick-reference and payloads
- `references/testing-methodology.md` — testing methodology
