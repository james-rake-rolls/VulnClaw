# XXE (Entity Injection)
English: XXE Entity Injection
- Entry Count: 9
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## XXE Basic Attack
- ID: xxe-basic
- Difficulty: intermediate
- Subcategory: Basic attack
- Tags: xxe, xml, external, entity
- Original Extracted Source: original extracted web-security-wiki source/xxe-basic.md
Description:
XML external-entity injection basic techniques
Prerequisites:
- An XML-parsing feature exists
- External entities are not disabled
Execution Outline:
1. 1. Probe for XXE
2. 2. Read a file
3. 3. Read the PHP source
4. 4. SSRF attack
## Blind XXE Attack
- ID: xxe-blind
- Difficulty: intermediate
- Subcategory: Blind XXE
- Tags: xxe, blind, oob, xml
- Original Extracted Source: original extracted web-security-wiki source/xxe-blind.md
Description:
Blind (no-echo) XXE techniques
Prerequisites:
- XML parsing is present
- No direct echo
Execution Outline:
1. 1. External-entity probing
2. 2. Parameter entities
3. 3. OOB data exfiltration
## XXE OOB Exfiltration Attack
- ID: xxe-oob
- Difficulty: intermediate
- Subcategory: OOB exfiltration
- Tags: xxe, oob, exfiltration, xml
- Original Extracted Source: original extracted web-security-wiki source/xxe-oob.md
Description:
Use OOB techniques to exfiltrate XXE data
Prerequisites:
- An XXE vulnerability exists
- Can initiate external requests
Execution Outline:
1. 1. HTTP out-of-band exfiltration
2. 2. FTP out-of-band exfiltration
3. 3. DNS out-of-band exfiltration
## XXE+SSRF Combined Attack
- ID: xxe-ssrf
- Difficulty: intermediate
- Subcategory: XXE+SSRF
- Tags: xxe, ssrf, combination, xml
- Original Extracted Source: original extracted web-security-wiki source/xxe-ssrf.md
Description:
Use XXE to perform an SSRF attack
Prerequisites:
- An XXE vulnerability exists
- The internal network is reachable
Execution Outline:
1. 1. Scan internal ports
2. 2. Access internal services
## XXE to RCE
- ID: xxe-rce
- Difficulty: advanced
- Subcategory: XXE to RCE
- Tags: xxe, rce, php, expect
- Original Extracted Source: original extracted web-security-wiki source/xxe-rce.md
Description:
Use XXE for remote code execution
Prerequisites:
- An XXE vulnerability exists
- The PHP expect extension is loaded
Execution Outline:
1. 1. Expect-extension RCE
2. 2. Write a web shell
## XXE File Read
- ID: xxe-file-read
- Difficulty: beginner
- Subcategory: File read
- Tags: xxe, file, read, lfi
- Original Extracted Source: original extracted web-security-wiki source/xxe-file-read.md
Description:
Use XXE to read server files
Prerequisites:
- An XXE vulnerability exists
- Has file-read permission
Execution Outline:
1. 1. Read Linux files
2. 2. Read Windows files
3. 3. Read the web config
4. 4. Read the source code
## XXE External-DTD Abuse
- ID: xxe-dtd
- Difficulty: intermediate
- Subcategory: External DTD
- Tags: xxe, dtd, external, xml
- Original Extracted Source: original extracted web-security-wiki source/xxe-dtd.md
Description:
Use an external DTD file for an XXE attack
Prerequisites:
- An XXE vulnerability exists
- Can access an external DTD
Execution Outline:
1. 1. Host a malicious DTD
2. 2. Reference an external DTD
3. 3. Multi-step exfiltration
4. 4. Error-message leak
## XLSX File XXE
- ID: xxe-xlsx
- Difficulty: intermediate
- Subcategory: XLSX-file XXE
- Tags: xxe, xlsx, excel, office
- Original Extracted Source: original extracted web-security-wiki source/xxe-xlsx.md
Description:
Use an XLSX file for an XXE attack
Prerequisites:
- The application parses XLSX files
- An XXE vulnerability exists
Execution Outline:
1. 1. Unzip the XLSX file
2. 2. Inject the XXE payload
## DOCX File XXE
- ID: xxe-docx
- Difficulty: intermediate
- Subcategory: DOCX-file XXE
- Tags: xxe, docx, word, office
- Original Extracted Source: original extracted web-security-wiki source/xxe-docx.md
Description:
Use a DOCX file for an XXE attack
Prerequisites:
- The application parses DOCX files
- An XXE vulnerability exists
Execution Outline:
1. 1. Unzip the DOCX file
2. 2. Inject the XXE payload

