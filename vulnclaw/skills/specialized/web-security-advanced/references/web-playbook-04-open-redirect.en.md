# Open redirect
English: Open Redirect
- Entry Count: 3
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Basic Open Redirect
- ID: redirect-basic
- Difficulty: beginner
- Subcategory: Basics
- Tags: redirect, url, phishing
- Original Extracted Source: original extracted web-security-wiki source/redirect-basic.md
Description:
URL-redirect vulnerability exploitation
Prerequisites:
- A target parameter controls the redirect destination
Execution Outline:
1. Direct redirect
2. Bypass validation
3. Slash bypass
## Redirect Bypass
- ID: redirect-bypass
- Difficulty: intermediate
- Subcategory: Bypass
- Tags: redirect, bypass
- Original Extracted Source: original extracted web-security-wiki source/redirect-bypass.md
Description:
Open-redirect bypass techniques
Prerequisites:
- A redirect parameter exists
Execution Outline:
1. URL encoding
2. The @ symbol
3. Backslash
## Redirect to SSRF
- ID: redirect-ssrf
- Difficulty: intermediate
- Subcategory: SSRF
- Tags: redirect, ssrf
- Original Extracted Source: original extracted web-security-wiki source/redirect-ssrf.md
Description:
Use an open-redirect vulnerability as a pivot to direct SSRF probing into the internal network, bypassing SSRF URL whitelist/blacklist restrictions
Prerequisites:
- The target has an open-redirect vulnerability
- The target has an SSRF-capable feature (URL parameter/webhook, etc.)
- The SSRF filter only checks the initial URL and does not follow redirects
Execution Outline:
1. Identify open-redirect points
2. Bypass the SSRF filter via a redirect
3. Assist with short links and DNS rebinding
4. Full exploitation chain: redirect → SSRF → internal probing

