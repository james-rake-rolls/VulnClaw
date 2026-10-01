# CSRF (Cross-Site Request Forgery)
English: CSRF Cross-Site Request Forgery
- Entry Count: 8
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## CSRF Basic Attack
- ID: csrf-basic
- Difficulty: beginner
- Subcategory: Basic attack
- Tags: csrf, cross-site, request, forgery
- Original Extracted Source: original extracted web-security-wiki source/csrf-basic.md
Description:
Cross-site request forgery basic techniques
Prerequisites:
- The target has sensitive operations
- CSRF protection is missing
Execution Outline:
1. 1. Build a CSRF form
2. 2. GET-request CSRF
3. 3. JSON CSRF
4. 4. Link luring
## JSON CSRF Attack
- ID: csrf-json
- Difficulty: intermediate
- Subcategory: JSON CSRF
- Tags: csrf, json, api, post
- Original Extracted Source: original extracted web-security-wiki source/csrf-json.md
Description:
CSRF techniques targeting JSON requests
Prerequisites:
- The target uses JSON-formatted requests
- CSRF protection is missing
- CORS is misconfigured
Execution Outline:
1. 1. Simple JSON CSRF
2. 2. Flash JSON CSRF
3. 3. XSSI attack
4. 4. SWF-file attack
## CSRF Bypass Techniques
- ID: csrf-bypass
- Difficulty: intermediate
- Subcategory: Bypass techniques
- Tags: csrf, bypass, token, referer
- Original Extracted Source: original extracted web-security-wiki source/csrf-bypass.md
Description:
Various techniques to bypass CSRF protection
Prerequisites:
- The target has CSRF protection
- The protection mechanism is flawed
Execution Outline:
1. 1. Token-validation bypass
2. 2. Referer-validation bypass
3. 3. Origin-validation bypass
4. 4. SameSite bypass
## SameSite Bypass Techniques
- ID: csrf-samesite
- Difficulty: intermediate
- Subcategory: SameSite bypass
- Tags: csrf, samesite, cookie, bypass
- Original Extracted Source: original extracted web-security-wiki source/csrf-samesite.md
Description:
CSRF attacks that bypass the SameSite cookie attribute
Prerequisites:
- The cookie has the SameSite attribute set
- The SameSite configuration is flawed
Execution Outline:
1. 1. SameSite=Lax bypass
2. 2. SameSite=Strict bypass
3. 3. SameSite not set
4. 4. Abuse the OAuth flow
## Token Bypass Techniques
- ID: csrf-token-bypass
- Difficulty: intermediate
- Subcategory: Token bypass
- Tags: csrf, token, bypass, predictable
- Original Extracted Source: original extracted web-security-wiki source/csrf-token-bypass.md
Description:
Techniques to bypass CSRF-token validation
Prerequisites:
- The target uses a CSRF token
- The token mechanism is flawed
Execution Outline:
1. 1. Predictable token
2. 2. Token not bound to the session
3. 3. Token leak
4. 4. Token replay
## Referer Bypass Techniques
- ID: csrf-referer-bypass
- Difficulty: intermediate
- Subcategory: Referer bypass
- Tags: csrf, referer, bypass, header
- Original Extracted Source: original extracted web-security-wiki source/csrf-referer-bypass.md
Description:
CSRF attacks that bypass Referer validation
Prerequisites:
- The target validates the Referer header
- The validation logic is flawed
Execution Outline:
1. 1. Regex-match bypass
2. 2. Empty-Referer bypass
3. 3. Subdomain bypass
4. 4. Referrer-Policy abuse
## Flash CSRF Attack
- ID: csrf-flash
- Difficulty: advanced
- Subcategory: Flash CSRF
- Tags: csrf, flash, swf, crossdomain
- Original Extracted Source: original extracted web-security-wiki source/csrf-flash.md
Description:
Use Flash for a CSRF attack
Prerequisites:
- The target allows Flash requests
- crossdomain.xml is misconfigured
Execution Outline:
1. 1. crossdomain.xml abuse
2. 2. Create a malicious SWF
3. 3. Send a JSON request
4. 4. Custom header
## CORS Misconfiguration Exploitation
- ID: csrf-cors
- Difficulty: intermediate
- Subcategory: CORS misconfiguration
- Tags: csrf, cors, misconfiguration, api
- Original Extracted Source: original extracted web-security-wiki source/csrf-cors.md
Description:
Exploit a CORS misconfiguration for a CSRF attack
Prerequisites:
- CORS misconfiguration
- Cross-origin credential sending is allowed
Execution Outline:
1. 1. Detect CORS configuration
2. 2. Reflected-Origin attack
3. 3. null-origin attack
4. 4. Regex bypass

