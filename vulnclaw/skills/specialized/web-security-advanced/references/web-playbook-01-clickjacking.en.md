# Clickjacking
English: Clickjacking
- Entry Count: 2
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Basic Clickjacking
- ID: clickjacking-basic
- Difficulty: beginner
- Subcategory: Basics
- Tags: clickjacking, ui-redressing, iframe
- Original Extracted Source: original extracted web-security-wiki source/clickjacking-basic.md
Description:
Use a transparent-iframe overlay to trick a user into unknowingly clicking a hidden malicious button or link
Prerequisites:
- The target site allows being nested in an iframe
- The target does not set the X-Frame-Options response header
- The target has no CSP frame-ancestors policy configured
- Basic HTML/CSS knowledge
Execution Outline:
1. Detect X-Frame-Options and CSP
2. Basic transparent-iframe overlay PoC
3. Multi-step drag-and-drop hijacking
4. Bypass using CSS pointer-events
## Clickjacking + XSS
- ID: clickjacking-xss
- Difficulty: intermediate
- Subcategory: XSS
- Tags: clickjacking, xss
- Original Extracted Source: original extracted web-security-wiki source/clickjacking-xss.md
Description:
Combine clickjacking with XSS: first use clickjacking to trigger the XSS vector, gaining deeper control
Prerequisites:
- The target has an XSS vulnerability
- The target allows being nested in an iframe
- The XSS payload can be triggered by a click
Execution Outline:
1. Identify an exploitable XSS + Clickjacking combination
2. Self-XSS + Clickjacking combined exploitation
3. Reflected XSS + iframe-nesting exploitation

