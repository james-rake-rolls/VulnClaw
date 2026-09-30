---
name: vuln-discovery
description: Vulnerability-discovery workflow — scan for flaws based on recon results
---

# Vulnerability Discovery Skill

Based on the reconnaissance results, systematically discover the security vulnerabilities present in the target.

## Steps

### 1. Known-CVE matching
- Search for CVEs matching the identified service versions
- Prioritize Critical/High severity
- Record the CVE ID, affected versions, and exploitation preconditions

### 2. Web vulnerability scanning
- SQL injection detection
- XSS detection (reflected / stored / DOM-based)
- SSRF detection
- LFI/RFI detection
- Command-injection detection
- File-upload vulnerability detection

### 3. Misconfiguration detection
- Default-credential testing
- Information-disclosure detection
- Unauthorized-access detection
- CORS configuration detection
- HTTPS configuration detection

### 4. Output
- Vulnerability list (type, severity, URL, parameter, verification method)
