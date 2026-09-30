# 08 Rapid Checklists And Payloads

This file is the rapid operator-reference layer of the final skill system.
Use it only after routing is clear. It is meant for fast lookup, not for replacing methodology or workflow selection.

## Use This File For

- Quickly recall what to look at first for a given vulnerability class or blocker
- Quickly shortlist payload families, bypass directions, and verification order
- Quickly confirm common testing cards for AI, MCP, containers, WebSocket, JWT, files, auth, SSRF, etc.
- Quickly move from "I know what to test" to "which class do I verify first"

## Do Not Use This File For

- Replaces `00-usage-and-routing.md` for scenario routing
- Replaces `01-unified-methodology.md` for methodology decisions
- Jumping into blind payload testing before requests are captured and replay is stable

## Fast Routing Cards

### Web injection or output execution

- Start with `web-playbook-index.md` (the `web-security-advanced` skill)
- For input-point validation, first split into `SQLi`, `XSS`, `command execution`, `SSTI`, `XXE`
- If the request is built by the client, return to `02-client-api-reverse-and-burp.md` first

### Auth, logic, token, or state bugs

- Start with `web-playbook-index.md` (the `web-security-advanced` skill)
- First confirm object identifiers, role boundaries, reset flows, payment amounts, and ordering dependencies
- If the token or signature comes from the client, stabilize replay before testing

### Browser-side sign, anti-bot, or WebSocket handshake

- Start with `browser-js-signing-workflow.md`
- Then, by phase, move into `browser-locate-and-request-chain.md`, `browser-recover-and-shell-reduction.md`, `browser-runtime-fit-and-risk.md`, `browser-validation-and-handoff.md`
- Once replay is stable, switch back to `web-playbook-index.md` (the `web-security-advanced` skill)

### Android runtime, packet visibility, or sign recovery

- Start with `android-external-url-runtime-first-workflow.md`
- If you need to progress via UI state, continue with `android-ui-driven-observation-and-packet-loop.md`
- Only when you cannot capture packets, they are opaque, or replay is blocked, move into `android-signing-and-crypto-workflow.md`

### AI, agent, or MCP exposure

- Start with `04-ai-and-mcp-security-integrated.md`
- First categorize into `prompt injection`, `tool abuse`, `MCP trust boundary`, `memory/state poisoning`, `output approval gaps`
- When you need a quick lookup of common test semantics, see the AI/MCP cards below

### Intranet, host, or AD work

- Start with `06-intranet-and-host-operations-integrated.md`
- When unsure about tooling, also consult `tools-reference-index.md` (the `pentest-tools` skill)

## Web Rapid Cards

### SQL injection

- Quick verification: `'`, `"`, `)`, boolean difference, timing difference, error difference
- First confirm the injection location: query, body, JSON, header, cookie, WebSocket message
- First check whether input is affected by client-side signing or encryption; if so, recover the request lifecycle first
- Common bypass directions: inline comments, whitespace variation, keyword case folding, alternate encodings, parameter pollution

### XSS

- Quick typing: reflected, stored, DOM
- First confirm the context: HTML body, attribute, JS string, URL, template
- Common opening families: event handlers, SVG, tag breaking, JS context breaking
- If the result passes through a client-side rendering framework, also check DOM sinks and CSP behavior

### Command execution

- Quick verification: timing, DNS or HTTP OOB, harmless command echo
- First identify whether the execution point is a system shell, template helper, language runtime, or worker sidecar
- Common bypass directions: separators, whitespace bypass, variable concatenation, Base64 or hex decode chains

### File and SSRF

- Categorize file issues first: upload, traversal/download, inclusion, parser confusion
- SSRF: first categorize into raw fetch, image proxy, webhook, PDF render, URL preview, cloud-metadata reachability
- Common bypass directions: encoding layers, mixed path separators, alternate IP formats, redirect chaining, protocol pivot

### Modern protocols

- WebSocket: first confirm handshake auth, Origin validation, message-level auth, and room boundaries
- JWT: first confirm algorithm handling, signature validation, and dynamic key-fetch paths like `kid` or `jku`
- OAuth/OIDC: first confirm the redirect URI, state, PKCE, and account binding
- Request smuggling: first confirm the proxy chain and front-end/back-end parsing differences

## AI And MCP Rapid Cards

### Prompt injection

- Quick typing: direct, indirect, retrieval-borne, tool-description-borne, memory-borne
- First confirm which boundary the injection enters: model prompt, retrieval context, tool metadata, tool output, persisted memory
- Common bypass directions: role play, instruction override, encoding, multilingual phrasing, hidden text, long-context dilution

### Tool abuse and MCP trust boundary

- First confirm whether the tool description is read with high trust by the model
- First confirm whether tool parameters, resource paths, and tool outputs are re-interpreted
- Quick checks: unauthorized resource reads, prompt override in the description, hidden instructions, cross-tool request rewriting

### Agent memory and state poisoning

- First confirm whether memory is explicit storage or an implicit history summary
- First check whether a malicious goal, role preference, or external instruction can be written into persistent state
- Watch for cross-turn behavior drift, approval bypass, and silent exfiltration

### Model or data leakage

- Quick checks: system-prompt extraction, tool-inventory exposure, API or secret leakage, training-data-style continuation, RAG source disclosure
- First distinguish direct disclosure from inference-style leakage

## Container And Sandbox Rapid Cards

### Environment triage

- First confirm whether you are inside a container, sandbox, restricted shell, or agent execution sandbox
- First check capabilities, namespaces, mounts, sockets, and metadata reachability
- If you are only verifying the isolation boundary, do not attempt destructive actions first

### Escape paths

- Common directions: exposed Docker socket, writable host mounts, privileged container, cgroup abuse, `/proc` traversal, kernel CVE, cloud-metadata pivots
- Do minimal information gathering first, then decide whether to continue

### Persistence or staged foothold

- First confirm the authorization boundary and the test target
- Prioritize verifying "can it persist" over spreading directly
- Common locations: shell rc files, scheduled tasks, service startup, workspace poisoning, SSH keys

## Payload Family Hints

Use families, not copied full lists, unless the current task specifically needs detail from a deeper source.

- SQLi: boolean, time, error, union, second-order
- XSS: reflected, stored, DOM, mutation-based, CSP-aware
- Command execution: separator-based, subshell, whitespace-bypass, encoded launcher, OOB validation
- File bugs: upload extension variants, MIME mismatch, parser confusion, traversal encodings
- SSRF: alternate IP encodings, redirect pivot, protocol pivot, metadata paths
- AI injection: direct override, indirect document-borne, description poisoning, memory poisoning, encoded or multilingual prompts
- Escape and shell: environment triage, breakout path validation, persistence validation, callback channel selection

## Escalation Rule

- If the route is still unclear, go back to `00-usage-and-routing.md`.
- If packet visibility or replay is blocked, go back to `02-client-api-reverse-and-burp.md` or the matching browser or Android workflow.
- If you need exact original payload wording or exhaustive raw examples, use the Web Rapid Cards section above or open the relevant `web-playbook-*.md` files in `web-security-advanced`.


