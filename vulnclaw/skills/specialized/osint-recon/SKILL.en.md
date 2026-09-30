---
name: osint-recon
description: OSINT open-source-intelligence knowledge base — four-dimension information-gathering model (server → website → domain → people), with the people dimension triggered conditionally
routing:
  phases: [recon]
  task_types: [osint, recon]
---

# OSINT Open-Source-Intelligence Knowledge Base

A practical knowledge base for information-gathering / reconnaissance / social-engineering scenarios, providing a **four-dimension information-gathering model** (server info → website info → domain info → people info) plus concrete tool usage and data-extraction techniques.

**Difference from the `recon` skill**:
- `recon` → technical reconnaissance (port scanning, DNS, directory enumeration) — the basic version
- `osint-recon` → full-dimension reconnaissance (server + website + domain + people/social engineering) — the in-depth version

## Core principles

1. **Cover all four dimensions** — the server/website/domain dimensions are always run; the people dimension is triggered conditionally
2. **Extract everything extractable from the page** — not just HTTP headers, but also HTML content, JS files, and comments
3. **Passive before active** — first review response headers, DNS, and WHOIS (passive), then do port scanning / directory enumeration (active)
4. **Dimension-completeness self-check** — each round, check which dimensions are done ✅ and which are not ❌; only allow [DONE] once all are complete
5. **External links are leads** — every external link on the page may be an information source
6. **Structured output** — aggregate all findings into a Markdown report

## Four-dimension information-gathering model

### Dimension 1: Server info
| Check | Tool/method | Notes |
|--------|----------|------|
| Open ports & service versions | MCP nmap / `python_execute` + socket | Full-port scan or common ports (21/22/80/443/3306/6379/8080/8443) |
| Real-IP discovery | DNS history / global ping / email-header extraction | Origin IP behind a CDN — SecurityTrails/DNSHistory/global ping |
| OS fingerprint | TTL inference + nmap OS detection | Linux TTL≈64, Windows TTL≈128, Unix TTL≈255 |
| Middleware version | Server response header + error page + signature files | Apache/Nginx/IIS/Tomcat version identification |
| Database identification | Port probing + error messages + behavior | MySQL(3306)/Redis(6379)/MongoDB(27017)/MSSQL(1433) |

### Dimension 2: Website info
| Check | Tool/method | Notes |
|--------|----------|------|
| Site architecture | Response headers + page traits + JS libraries | OS + middleware + database + language + framework → full tech stack |
| Web fingerprint | `fetch` + response-trait matching | CMS type, front-end framework, JS libraries, template engine |
| WAF detection | wafw00f logic + response traits | Block pages / special response headers / abnormal status codes |
| Sensitive directories & files | `python_execute` + common-path wordlist | /admin /backup /config /api /robots.txt /sitemap.xml |
| Source-code leakage | Check common leak paths | .git/.svn/.DS_Store/.env/web.config/backup files (.bak/.swp/.old) |
| Same-server sites | Reverse-lookup domains on the same IP | Webmaster tools / Threatbook / crt.sh same-IP lookup |
| C-block lookup | Scan live hosts in the same subnet | nmap -sn scan of the /24 subnet |

### Dimension 3: Domain info
| Check | Tool/method | Notes |
|--------|----------|------|
| WHOIS registration | `python_execute` + whois API/command | Registrant / registrar / NS servers / registration date / expiry date |
| ICP filing info | MIIT filing-lookup API | Only needed for mainland-China domains; overseas domains have no filing |
| Subdomain discovery | crt.sh + brute force + search engines + DNS zone transfer | Cross-verify across methods for full coverage |
| Full DNS records | `python_execute` + dnspython/socket | A/CNAME/MX/TXT/NS/SPF/SOA full query |
| Certificate-transparency logs | crt.sh / Censys / certspotter | Discover historical certificates, subdomains, related domains |

### Dimension 4: People info ⚡ conditionally triggered
**⚠️ This dimension runs only when at least one of the following holds:**
- The user's command explicitly mentions "social engineering / people info / author tracking / persona profiling" or similar
- The target site has explicit author info (meta author, about page, contact details)

**When you should NOT do social engineering**: an ordinary corporate site with no personal author / the user only asked to "scan the target" / the target is an IP or internal address

| Tracking direction | Method | Notes |
|----------|------|------|
| Author-identifier extraction | Page meta author, about page | Username, nickname, email |
| GitHub tracking | `fetch` + GitHub API | Repos, language preference, contribution history, email |
| Social media | Extract links from the page → visit | Bilibili, Weibo, Zhihu, Twitter, LinkedIn |
| Cross-platform correlation | Search other platforms by username/email | Same-ID cross-platform search |
| Commit history | GitHub commits → commit email | Correlate other projects and identities |
| Leak detection | GitHub historical-code search | .env, config, key leakage |

## First-pass workflow

1. **Access the target** → `fetch` the home page, extract HTTP headers + HTML content
2. **Dimension 1: server info** → port scanning, real IP, OS fingerprint, middleware/database identification
3. **Dimension 2: website info** → web fingerprint, WAF detection, sensitive dirs/source leakage, same-server/C-block
4. **Dimension 3: domain info** → WHOIS, ICP filing, subdomains, DNS records, certificate transparency
5. **Dimension 4 (conditional)** → extract author info, cross-platform tracking, information aggregation
6. **Dimension-completeness self-check** → confirm each dimension has had at least one round of checks
7. **Aggregate report** → produce a Markdown-format reconnaissance report

## Scenario routing

| Scenario | Reference | Core content |
|------|---------|---------|
| Server information gathering | `server-recon.md` | Port scanning, real IP, OS fingerprint, middleware/database identification |
| Website information gathering | `website-recon.md` | Architecture/fingerprint/WAF/sensitive dirs/source leakage/same-server/C-block |
| Web fingerprinting | `web-fingerprinting.md` | Framework detection, version identification, tech-stack inference |
| Author-tracking methods | `author-tracking.md` | Extract the author from the page → cross-platform tracking → aggregation |
| OSINT tool usage | `osint-toolkit.md` | crt.sh, GitHub API, search-engine dorks, same-server/C-block/ICP |
| Social-engineering intel aggregation | `social-engineering-intel.md` | Persona profiling, relationship networks, cross-verification |
| Recon report template | `recon-report-template.md` | Standard Markdown report format (four dimensions) |

## ⭐ Common extraction snippets

### Extract all external links from HTML
```python
import re
html = "..."  # HTML obtained via fetch
links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
for link in set(links):
    print(link)
```

### Extract author info from HTML
```python
import re
# meta author
author = re.findall(r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']+)["\']', html)
# about-page links
about_links = re.findall(r'href=["\']([^"\']*(?:about|me|contact)[^"\']*)["\']', html, re.I)
```

### Query crt.sh for subdomains
```python
import requests
domain = "example.com"
r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json")
if r.status_code == 200:
    for entry in r.json():
        print(entry['name_value'])
```

### GitHub user info
```python
import requests
username = "target_user"
r = requests.get(f"https://api.github.com/users/{username}")
if r.status_code == 200:
    data = r.json()
    print(f"Name: {data.get('name')}")
    print(f"Bio: {data.get('bio')}")
    print(f"Email: {data.get('email')}")
    print(f"Blog: {data.get('blog')}")
    print(f"Location: {data.get('location')}")
    print(f"Company: {data.get('company')}")
```

### WAF detection (response-trait method)
```python
import requests
url = "https://target.com"
# normal request
r1 = requests.get(url)
# request that triggers the WAF (with attack traits)
r2 = requests.get(url + "/?id=1' OR 1=1--")
# compare responses
if r1.status_code != r2.status_code or len(r1.text) != len(r2.text):
    print("[!] A WAF may be present")
    print(f"Normal status: {r1.status_code}, attack status: {r2.status_code}")
```

### Same-server lookup (reverse-lookup domains on the same IP)
```python
import requests
ip = "1.2.3.4"
# use the chinaz API or another reverse-lookup service
# you can also query crt.sh for certificates on the same IP
r = requests.get(f"https://crt.sh/?q={ip}&output=json")
```
