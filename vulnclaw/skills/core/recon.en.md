---
name: recon
description: Reconnaissance workflow — passive + active recon
routing:
  phases: [recon]
  task_types: [recon]
---

# Reconnaissance Skill

Perform passive and active information gathering to build a target profile and an attack-surface map.

## Steps

### 1. Passive reconnaissance
- Access the target via the fetch tool and collect HTTP response headers
- Identify the server type, version, and any WAF
- Analyze tech-stack indicators in the HTML source

### 2. Active reconnaissance
- Probe common web ports
- Enumerate directories and paths
- Check sensitive files (robots.txt, .env, .git)
- Discover API endpoints

### 3. Tech-stack identification
- Front-end frameworks (React/Vue/Angular/jQuery)
- Back-end frameworks (Express/Django/Flask/Spring)
- CMS platforms (WordPress/Joomla/custom)
- Database type

### 4. Output
- Target profile (IP / domain / ports / services / tech stack)
- Attack-surface map (reachable paths, APIs, admin entry points)
