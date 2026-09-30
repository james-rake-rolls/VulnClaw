---
name: reporting
description: Report-generation workflow — produce a structured pentest report and PoCs
routing:
  phases: [reporting]
  task_types: [report]
---

# Report Generation Skill

Organize the penetration-test results into a structured report, including detailed findings, PoC scripts, and remediation recommendations.

## Report structure

### 1. Project overview
- Test target
- Test dates
- Test scope
- Test methodology

### 2. Executive summary
- Overview of high-severity findings
- Risk-level distribution
- Key recommendations

### 3. Detailed findings
For each vulnerability:
- Name and severity
- Vulnerability type
- Impact scope
- Verification steps
- Key evidence (request / response / screenshot)
- PoC script
- Remediation recommendations

### 4. Attack path
- A diagram of the complete attack chain
- The path from initial access to the final objective

### 5. Appendices
- PoC scripts
- Traffic captures
- Screenshot evidence
