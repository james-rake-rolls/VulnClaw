# WebSocket Security
English: WebSocket Security
- Entry Count: 3
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Cross-Site WebSocket Hijacking (CSWSH)
- ID: ws-hijack
- Difficulty: intermediate
- Subcategory: WebSocket hijacking
- Tags: WebSocket, CSWSH, Origin, cross-site, session hijacking
- Original Extracted Source: original extracted web-security-wiki source/ws-hijack.md
Description:
Exploit the lack of Origin validation during the WebSocket handshake to establish a cross-site WebSocket connection from a malicious page. The attacker can hijack the victim's WebSocket session, steal real-time data, or send messages as the victim. Similar to CSRF but targeting the WebSocket protocol.
Prerequisites:
- The target uses WebSocket communication
- The WebSocket handshake does not validate Origin
Execution Outline:
1. 1. Identify the WebSocket endpoint
2. 2. Build a cross-site-hijacking PoC page
3. 3. WebSocket message injection
4. 4. WebSocket traffic-analysis script
## WebSocket Smuggling Attack
- ID: ws-smuggling
- Difficulty: expert
- Subcategory: WebSocket smuggling
- Tags: WebSocket, smuggling, reverse proxy, H2C, internal pivoting
- Original Extracted Source: original extracted web-security-wiki source/ws-smuggling.md
Description:
Exploit differences in how a reverse proxy / load balancer handles the WebSocket protocol to smuggle HTTP requests to internal services via a WebSocket upgrade request. The attacker can bypass front-end security controls and communicate directly with the back end, reaching protected internal APIs or admin interfaces.
Prerequisites:
- The target uses a reverse proxy (Nginx/Varnish, etc.)
- The proxy allows WebSocket upgrades
- Internal services exist behind the back end
Execution Outline:
1. 1. Detect WebSocket-smuggling feasibility
2. 2. WebSocket-tunnel construction
3. 3. H2C smuggling to bypass access control
4. 4. Exploit reverse-proxy differences
## WebSocket Authentication and Authorization Bypass
- ID: ws-auth-bypass
- Difficulty: intermediate
- Subcategory: Authentication bypass
- Tags: WebSocket, authentication, authorization, privilege bypass, token replay
- Original Extracted Source: original extracted web-security-wiki source/ws-auth-bypass.md
Description:
Exploit the lack of ongoing authentication checks after a WebSocket connection is established, bypassing authentication and authorization via session fixation, token replay, and unauthorized channel subscription. WebSocket's long-lived connections keep the original connection valid even after a permission change.
Prerequisites:
- The target uses WebSocket for real-time communication
- A valid session/token has been obtained
Execution Outline:
1. 1. WebSocket authentication-mechanism analysis
2. 2. Token replay and session fixation
3. 3. Unauthorized channel/room subscription
4. 4. WebSocket rate-limit and DoS test

