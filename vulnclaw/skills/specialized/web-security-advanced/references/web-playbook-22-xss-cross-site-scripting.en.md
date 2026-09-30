# XSS (Cross-Site Scripting)
English: XSS Cross-Site Scripting
- Entry Count: 12
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Reflected XSS
- ID: xss-reflected
- Difficulty: beginner
- Subcategory: Reflected
- Tags: xss, reflected, javascript
- Original Extracted Source: original extracted web-security-wiki source/xss-reflected.md
Description:
Reflected cross-site scripting techniques
Prerequisites:
- User input is reflected into the page
- Input is not filtered or encoded
Execution Outline:
1. 1. Probe for XSS injection points
2. 2. Event-handler bypass
3. 3. Tag bypass
4. 4. Steal cookies
## Stored XSS
- ID: xss-stored
- Difficulty: intermediate
- Subcategory: Stored
- Tags: xss, stored, persistent
- Original Extracted Source: original extracted web-security-wiki source/xss-stored.md
Description:
Stored cross-site scripting techniques
Prerequisites:
- A data-storage feature exists
- Stored data is displayed without filtering
Execution Outline:
1. 1. Probe for storage points
2. 2. Stealthy payload
3. 3. Persistent control
4. 4. BeEF Hook
## DOM-Based XSS
- ID: xss-dom
- Difficulty: intermediate
- Subcategory: DOM-based
- Tags: xss, dom, javascript
- Original Extracted Source: original extracted web-security-wiki source/xss-dom.md
Description:
DOM-based cross-site scripting
Prerequisites:
- JavaScript dynamically manipulates the DOM
- User input is written directly into the DOM
Execution Outline:
1. 1. Probe for DOM XSS
2. 2. Common sink points
3. 3. location.hash abuse
4. 4. postMessage abuse
## CSP Bypass
- ID: xss-csp-bypass
- Difficulty: advanced
- Subcategory: CSP bypass
- Tags: xss, csp, bypass
- Original Extracted Source: original extracted web-security-wiki source/xss-csp-bypass.md
Description:
XSS techniques that bypass the Content Security Policy (CSP)
Prerequisites:
- An XSS vulnerability exists
- A CSP policy exists but is misconfigured
Execution Outline:
1. 1. Analyze the CSP policy
2. 2. Exploit unsafe-inline
3. 3. Exploit unsafe-eval
4. 4. JSONP bypass
## Mutation XSS (mXSS)
- ID: xss-mxss
- Difficulty: advanced
- Subcategory: Mutation-based
- Tags: xss, mxss, mutation, bypass
- Original Extracted Source: original extracted web-security-wiki source/xss-mxss.md
Description:
XSS attacks caused by browser-parsing differences
Prerequisites:
- An HTML output point exists
- Browser-parsing differences
Execution Outline:
1. 1. Basic mXSS probing
2. 2. SVG mXSS
3. 3. Math mXSS
4. 4. Combine with DOM clobbering
## Unicode XSS
- ID: xss-unicode
- Difficulty: intermediate
- Subcategory: Unicode encoding
- Tags: xss, unicode, encoding, bypass
- Original Extracted Source: original extracted web-security-wiki source/xss-unicode.md
Description:
Use Unicode-encoding traits to bypass filtering
Prerequisites:
- An XSS injection point exists
- The filter checks for keywords
Execution Outline:
1. 1. Unicode escaping
2. 2. HTML entity encoding
3. 3. Unicode-normalization attack
4. 4. UTF-7 encoding
## XSS Filter Bypass
- ID: xss-filter-bypass
- Difficulty: intermediate
- Subcategory: Filter bypass
- Tags: xss, filter, bypass, waf
- Original Extracted Source: original extracted web-security-wiki source/xss-filter-bypass.md
Description:
Various techniques to bypass XSS filters
Prerequisites:
- An XSS injection point exists
- A filtering mechanism is present
Execution Outline:
1. 1. Case obfuscation
2. 2. Double-write bypass
3. 3. Comment obfuscation
4. 4. Null-byte truncation
## XSS Encoding Bypass
- ID: xss-encoding
- Difficulty: intermediate
- Subcategory: Encoding bypass
- Tags: xss, encoding, bypass
- Original Extracted Source: original extracted web-security-wiki source/xss-encoding.md
Description:
Use various encoding techniques to bypass XSS filtering
Prerequisites:
- An XSS injection point exists
- Encoding handling is present
Execution Outline:
1. 1. URL encoding
2. 2. HTML entity encoding
3. 3. JavaScript encoding
4. 4. CSS encoding
## Polyglot XSS
- ID: xss-polyglot
- Difficulty: intermediate
- Subcategory: Polyglot
- Tags: xss, polyglot, universal
- Original Extracted Source: original extracted web-security-wiki source/xss-polyglot.md
Description:
XSS payloads that work across many environments
Prerequisites:
- An XSS injection point exists
- The exact environment is uncertain
Execution Outline:
1. 1. Classic polyglot
2. 2. Short polyglot
3. 3. Attribute-injection polyglot
4. 4. URL-parameter polyglot
## XSS Cookie Theft
- ID: xss-cookie-theft
- Difficulty: beginner
- Subcategory: Cookie theft
- Tags: xss, cookie, theft, session
- Original Extracted Source: original extracted web-security-wiki source/xss-cookie-theft.md
Description:
Use XSS to steal a user's cookie
Prerequisites:
- An XSS vulnerability exists
- The cookie is not set HttpOnly
Execution Outline:
1. 1. Basic cookie theft
2. 2. Fetch-API exfiltration
3. 3. XMLHttpRequest exfiltration
4. 4. Encoded transport
## XSS Keylogging
- ID: xss-keylogger
- Difficulty: intermediate
- Subcategory: Keylogging
- Tags: xss, keylogger, credential
- Original Extracted Source: original extracted web-security-wiki source/xss-keylogger.md
Description:
Use XSS to record a user's keystrokes
Prerequisites:
- A stored XSS exists
- The target page has sensitive inputs
Execution Outline:
1. 1. Basic keylogging
2. 2. Full keylogging
3. 3. Form exfiltration
4. 4. Form-submission hijacking
## BeEF Framework Exploitation
- ID: xss-beef
- Difficulty: advanced
- Subcategory: BeEF exploitation
- Tags: xss, beef, framework, exploitation
- Original Extracted Source: original extracted web-security-wiki source/xss-beef.md
Description:
Use the BeEF framework for XSS exploitation
Prerequisites:
- An XSS vulnerability exists
- Deploy a BeEF server
Execution Outline:
1. 1. Deploy BeEF
2. 2. Inject a hook script
3. 3. Common commands
4. 4. Module abuse

