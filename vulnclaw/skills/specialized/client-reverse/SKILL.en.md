---
name: client-reverse
description: Client reversing and Burp replay — complex client signature recovery, crypto recovery, request-chain tracing, and stable replay, for authorized Android app pentesting, browser JS signing, and desktop-client reversing
routing:
  target_types: [client, android, mobile]
  task_types: [reverse]
  tooling: [frida, jadx, burp, scrcpy]
---

# Client Reversing & Burp Replay Skill

Use this skill when requests are built by a client (Android app, browser JS, desktop client) and signing, encryption, token state, device binding, or anti-automation logic prevents Burp from replaying them directly.

## Core principle

**Packet-First**: first capture and analyze the real HTTP/HTTPS requests or WebSocket traffic and confirm usability, then reverse-engineer the blockers as needed. Reversing is a blocker-resolution step, not the default entry point.

## Scenario routing

### Authorized Android app pentesting

**Do not analyze the APK with jadx or ida_pro_mcp first**; follow this order:

1. Confirm the target app is installed on a connected device
2. Have Burp or Charles ready to capture traffic
3. Open the app with scrcpy_vision and drive the real business flows
4. After each key action, check whether HTTP/HTTPS or WebSocket packets appear in Burp/Charles
5. If packets are visible and replayable → go straight to `web-security-advanced` for Web/API security testing
6. Repeat the "UI action → capture → web-security analysis" loop
7. Only when you cannot capture packets / packets are encrypted / cannot be replayed → escalate to jadx → frida_mcp → ida_pro_mcp

**MCP tool chain**: scrcpy_vision → burp/charles → adb_mcp → jadx → frida_mcp → ida_pro_mcp

### Browser JS signing, anti-scraping, WebSocket handshakes

1. chrome_devtools to view page state and the request chain
2. js_reverse to locate the token/sign generation logic
3. burp to verify replay and determine the mutable fields

**Phase model**: locate → recover → runtime → validation → replay

**MCP tool chain**: chrome_devtools → js_reverse → burp

### Desktop client / local signer

1. everything_search to locate the relevant files
2. ida_pro_mcp for static analysis of the signing function
3. frida_mcp to obtain runtime parameters
4. burp to verify stable replay

**MCP tool chain**: everything_search → ida_pro_mcp → frida_mcp → burp

## Replay-readiness checklist

Before entering payload testing, you must be able to answer:

- How is the request body constructed?
- Where do the signing/encryption inputs come from?
- Which cookies, headers, tokens, device values, timestamps, and nonces are required?
- Does the request depend on ordering or session state?
- Which fields can be changed without breaking replay?

## Evidence to retain

- Location of the builder/signer/crypto code
- Key hook points and observed runtime values
- A working replay request sample
- Preconditions, failure modes, and notes on anti-automation behavior

## References

- `references/02-client-api-reverse-and-burp.md` — overall client-reversing-to-Burp-replay workflow
- `references/android-authorized-app-pentest-sop.md` — Android app pentest SOP
- `references/browser-js-signing-workflow.md` — browser JS signing workflow
- `references/android-signing-and-crypto-workflow.md` — Android signing and crypto workflow
- `references/android-ui-driven-observation-and-packet-loop.md` — Android UI-driven observation loop
- `references/android-external-url-runtime-first-workflow.md` — Android external-URL testing
- `references/android-network-layer-testing-quick-reference.md` — Android network-layer testing quick-reference
- `references/MCP.md` — overall MCP-capabilities document
- `references/tool-selection-map.md` — tool-selection map
