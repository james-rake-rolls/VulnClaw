# Business-Logic Vulnerabilities
English: Business Logic Vulnerabilities
- Entry Count: 5
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## IDOR Unauthorized Access
- ID: biz-idor
- Difficulty: beginner
- Subcategory: Authorization-bypass vulnerability
- Tags: IDOR, authorization bypass, business logic, OWASP, A01
- Original Extracted Source: original extracted web-security-wiki source/biz-idor.md
Description:
Insecure direct object reference (IDOR): by tampering with the object ID in a request parameter, access others' data without authorization. An attacker can enumerate parameters such as user IDs and order numbers to obtain unauthorized resources.
Prerequisites:
- The target has an ID-based resource-access endpoint
- Logged in as an ordinary user account
Execution Outline:
1. 1. Identify traversable parameters
2. 2. Horizontal-privilege-escalation test
3. 3. Vertical-privilege-escalation test
4. 4. Parameter-pollution privilege bypass
## Race-Condition Attack
- ID: biz-race-condition
- Difficulty: intermediate
- Subcategory: Race condition
- Tags: race condition, Race Condition, TOCTOU, concurrency, business logic
- Original Extracted Source: original extracted web-security-wiki source/biz-race-condition.md
Description:
Exploit a server-side TOCTOU (Time-of-Check to Time-of-Use) vulnerability, using concurrent requests to trigger the same operation multiple times in the window between check and execution, achieving business-logic breaks such as duplicate coupon claims, duplicate withdrawals, and over-purchasing.
Prerequisites:
- The target has operations on quantifiable resources such as balance/points/coupons
- A Python / Turbo Intruder environment
Execution Outline:
1. 1. Identify the race-condition target
2. 2. Python concurrency test script
3. 3. Burp Turbo Intruder test
4. 4. Verify the race succeeded
## Payment-Logic Tampering
- ID: biz-payment-tamper
- Difficulty: intermediate
- Subcategory: Payment security
- Tags: payment, amount tampering, business logic, zero-cost purchase, e-commerce security
- Original Extracted Source: original extracted web-security-wiki source/biz-payment-tamper.md
Description:
Manipulate transaction logic by modifying parameters such as amount, quantity, and discount in a payment request. Common in e-commerce platforms and online payment systems, it can cause serious business risks such as zero-cost purchases, negative prices, and discount stacking.
Prerequisites:
- The target has a payment/ordering feature
- Can intercept and modify HTTP requests
Execution Outline:
1. 1. Amount-tampering test
2. 2. Quantity and shipping-fee tampering
3. 3. Coupon stacking and substitution
4. 4. Payment-callback tampering
## Password-Reset Logic Flaws
- ID: biz-password-reset
- Difficulty: intermediate
- Subcategory: Authentication flaw
- Tags: password reset, authentication bypass, business logic, verification code, Host injection
- Original Extracted Source: original extracted web-security-wiki source/biz-password-reset.md
Description:
Logic vulnerabilities in the password-reset flow, including reset-token leakage, verification-code brute force, response manipulation, and Host-header injection, which can enable resetting any user's password.
Prerequisites:
- The target has a password-reset/recovery feature
- Can intercept HTTP requests
Execution Outline:
1. 1. Host-header injection to steal the reset link
2. 2. Verification-code brute force
3. 3. Response-manipulation bypass
4. 4. Weak randomness of the reset token
## CAPTCHA Bypass Techniques
- ID: biz-captcha-bypass
- Difficulty: beginner
- Subcategory: Verification-code security
- Tags: verification code, CAPTCHA, bypass, SMS code, human verification
- Original Extracted Source: original extracted web-security-wiki source/biz-captcha-bypass.md
Description:
Various techniques to bypass human-verification mechanisms such as graphical CAPTCHAs, SMS codes, and slider verification, including response leakage, reuse attacks, OCR recognition, and logic-flaw exploitation.
Prerequisites:
- The target has a feature protected by a verification code
- A Python environment
Execution Outline:
1. 1. Verification-code response leak
2. 2. Verification-code-reuse attack
3. 3. Delete the verification-code parameter
4. 4. Universal verification code

