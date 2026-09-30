# Authentication Vulnerabilities
English: Authentication Vulnerabilities
- Entry Count: 10
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Authentication Bypass
- ID: auth-bypass
- Difficulty: intermediate
- Subcategory: Authentication bypass
- Tags: auth, bypass, authentication
- Original Extracted Source: original extracted web-security-wiki source/auth-bypass.md
Description:
Web-application authentication-bypass techniques
Prerequisites:
- The target has an authentication mechanism
- The authentication implementation is flawed
Execution Outline:
1. SQL-injection bypass
2. Array bypass
3. Type conversion
4. JSON bypass
## Brute Force
- ID: auth-brute
- Difficulty: beginner
- Subcategory: Brute force
- Tags: auth, brute-force, password
- Original Extracted Source: original extracted web-security-wiki source/auth-brute.md
Description:
Automated password-guessing attacks
Prerequisites:
- No verification code
- No lockout policy
Execution Outline:
1. Pitchfork
2. Cluster bomb
3. Username enumeration based on response differences
4. Verification-code / OTP brute force and bypass
## Session Hijacking
- ID: auth-session
- Difficulty: intermediate
- Subcategory: Session management
- Tags: auth, session, hijack
- Original Extracted Source: original extracted web-security-wiki source/auth-session.md
Description:
Exploit session-management flaws to hijack or forge user sessions and gain unauthorized access
Prerequisites:
- The target uses cookie- or token-based session management
- Can intercept or predict the session identifier
- Network communication is not fully encrypted (HTTP) or an XSS exists
Execution Outline:
1. Session-cookie attribute analysis
2. Session-fixation attack
3. Session hijacking (HTTP sniffing)
4. Session prediction (weak randomness)
## Password-Reset Vulnerabilities
- ID: auth-password-reset
- Difficulty: intermediate
- Subcategory: Logic vulnerability
- Tags: auth, password-reset, logic
- Original Extracted Source: original extracted web-security-wiki source/auth-password-reset.md
Description:
Bypass the password-reset flow
Prerequisites:
- The password-reset feature has a logic flaw
Execution Outline:
1. Host-header poisoning
2. Token brute force
3. Password-reset-token predictability analysis
4. Password-reset-flow logic flaws
## OAuth Vulnerabilities
- ID: auth-oauth
- Difficulty: advanced
- Subcategory: OAuth
- Tags: auth, oauth, redirect
- Original Extracted Source: original extracted web-security-wiki source/auth-oauth.md
Description:
OAuth authentication-flow vulnerabilities
Prerequisites:
- Uses OAuth login
Execution Outline:
1. CSRF attack
2. Redirect URI
3. OAuth state parameter missing / predictable CSRF
4. Token theft and scope over-privilege
## SAML Vulnerabilities
- ID: auth-saml
- Difficulty: advanced
- Subcategory: SAML
- Tags: auth, saml, xml
- Original Extracted Source: original extracted web-security-wiki source/auth-saml.md
Description:
SAML assertion attack
Prerequisites:
- Uses SAML SSO
Execution Outline:
1. XML-signature bypass
2. XXE attack
3. SAML Response tampering and replay
4. Advanced SAML-signature-bypass techniques
## 2FA Bypass
- ID: auth-2fa
- Difficulty: intermediate
- Subcategory: 2FA
- Tags: auth, 2fa, mfa
- Original Extracted Source: original extracted web-security-wiki source/auth-2fa.md
Description:
Bypass two-factor authentication
Prerequisites:
- Enable 2FA
Execution Outline:
1. Direct access
2. Verification-code brute force
3. Logic bypass
## CAPTCHA Bypass
- ID: auth-captcha
- Difficulty: beginner
- Subcategory: Verification code
- Tags: auth, captcha, bypass
- Original Extracted Source: original extracted web-security-wiki source/auth-captcha.md
Description:
Bypass a graphical CAPTCHA
Prerequisites:
- A verification code is present
Execution Outline:
1. Reuse
2. Null-value bypass
3. Delete the parameter
## Remember-Me Vulnerability
- ID: auth-remember-me
- Difficulty: intermediate
- Subcategory: Session management
- Tags: auth, remember-me, cookie
- Original Extracted Source: original extracted web-security-wiki source/auth-remember-me.md
Description:
Remember-Me feature vulnerabilities
Prerequisites:
- Remember Me is enabled
Execution Outline:
1. Cookie forgery
2. Base64 decoding
3. Reverse-analysis of the remember-password token
4. Shiro RememberMe deserialization RCE
## JWT Authentication Vulnerabilities
- ID: auth-jwt
- Difficulty: intermediate
- Subcategory: JWT
- Tags: auth, jwt, token
- Original Extracted Source: original extracted web-security-wiki source/auth-jwt.md
Description:
Exploit JWT (JSON Web Token) implementation flaws to forge or tamper with authentication tokens, achieving unauthorized access or privilege escalation
Prerequisites:
- The target uses JWT for authentication
- Can obtain or intercept the JWT token
- The JWT library has a known vulnerability or the server is misconfigured
Execution Outline:
1. JWT decoding and analysis
2. Algorithm-None attack
3. HS256 key brute force
4. RS256→HS256 algorithm-confusion attack

