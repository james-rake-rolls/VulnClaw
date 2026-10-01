# Web fingerprinting

## Checklist

### HTTP Response-Header Fingerprint
| Response header | Inferred info | Example |
|--------|---------|------|
| `Server` | Web server | `nginx/1.18.0`, `Apache/2.4.41`, `GitHub.com` |
| `X-Powered-By` | Back-end language/framework | `PHP/7.4.3`, `Express`, `Next.js` |
| `X-AspNet-Version` | .NET version | `4.0.30319` |
| `Set-Cookie` | Framework trait | `PHPSESSID`->PHP, `JSESSIONID`->Java, `csrf_token`->Django |
| `X-Generator` | CMS | `Hugo`、`WordPress`、`Ghost` |
| `X-DRupal-Cache` | CMS | Drupal |
| `Via` | Proxy/CDN | `1.1 varnish`->Varnish CDN |

### HTML-Source Fingerprint
```python
import re

# WordPress
wp_signs = ['wp-content', 'wp-includes', 'wordpress']
# Hexo
hexo_signs = ['hexo', 'hexo-theme']
# Hugo
hugo_signs = ['hugo', 'gohugo']
# Jekyll
jekyll_signs = ['jekyll']
# Next.js
next_signs = ['__NEXT_DATA__', '_next/']
# Vue
vue_signs = ['data-v-', '__vue__']
# React
react_signs = ['data-reactroot', '__react']

def detect_framework(html):
    html_lower = html.lower()
    frameworks = []
    checks = {
        'WordPress': wp_signs,
        'Hexo': hexo_signs,
        'Hugo': hugo_signs,
        'Jekyll': jekyll_signs,
        'Next.js': next_signs,
        'Vue': vue_signs,
        'React': react_signs,
    }
    for name, signs in checks.items():
        if any(s in html_lower for s in signs):
            frameworks.append(name)
    return frameworks
```

### JavaScript-File Fingerprint
- Framework-specific JS paths: `/wp-includes/js/` -> WordPress
- Vue/React DevTools detection: `__VUE_DEVTOOLS_GLOBAL_HOOK__`, `__REACT_DEVTOOLS_GLOBAL_HOOK__`
- The framework version is usually in a JS comment or variable

### CSS Fingerprint
- `/wp-content/themes/` → WordPress
- Hexo-theme signature class names
- Bootstrap/Tailwind class traits

### Signature Files
| File path | Inferred info |
|---------|---------|
| `/robots.txt` | CMS info, hidden paths |
| `/sitemap.xml` | Site structure |
| `/favicon.ico` | Framework default icon |
| `/.well-known/security.txt` | Security contact |
| `/humans.txt` | Developer info |
| `/.git/HEAD` | Git-repository leakage |
| `/.env` | Environment-variable leakage |

## GitHub Pages Traits
- Response header `Server: GitHub.com`
- `X-GitHub-Request-Id` is present
- `X-Cache: HIT` + `X-Fastly-Request-ID` → Fastly CDN
- `Via: 1.1 varnish` -> Varnish cache
- Common frameworks: Jekyll, Hexo, Hugo

---

## WAF Detection

### Common WAF-Identification Traits
| WAF | Response-header / page trait | Block status code |
|-----|----------------|-----------|
| Cloudflare | `Server: cloudflare`, `CF-Ray` | 403 |
| AWS WAF | `x-amz-request-id`, `x-amz-cf-id` | 403 |
| Aliyun WAF | Cookie contains `acw_tc` | 405/403 |
| Tencent Cloud WAF | Specific JSON block page | 403 |
| BaoTa WAF | Block page contains "BaoTa" | 403 |
| SafeDog | Block page contains "safedog" | 403/404 |
| ModSecurity | Specific 403 + Server header | 403 |
| Nginx WAF | `HTTP/1.1 444` or a special 403 | 444/403 |

### WAF-Detection Method
1. **Normal vs attack request comparison** — send a request with attack traits and observe the difference
2. **Response-header check** — some WAFs add specific response headers
3. **Cookie check** — some WAFs set tracking cookies
4. **Abnormal status code** — the attack request returns an unusual status (403/406/429/444)

### Common WAF-Triggering Payloads
```
/?id=1' OR 1=1--
/?search=<script>alert(1)</script>
/../../../etc/passwd
/?file=php://filter/convert.base64-encode/resource=index
```

---

## Source-Leakage Check

### Common Source-Leakage Types and Detection
| Type | Path | Detection method | Severity |
|------|------|---------|---------|
| Git repo | `/.git/config`, `/.git/HEAD` | 200 and contains git content | 🔴 Critical |
| SVN repo | `/.svn/entries` | 200 and contains svn content | 🔴 Critical |
| .DS_Store | `/.DS_Store` | Download and parse the directory structure | 🟡 Medium |
| .env file | `/.env` | Contains DB_PASSWORD, etc. | 🔴 Critical |
| web.config | `/web.config` | IIS config leakage | 🟡 Medium |
| Backup files | `/.bak`, `/.swp`, `/.old`, `/.tar.gz` | Direct download | 🟡 Medium |
| Docker | `/Dockerfile`, `/docker-compose.yml` | Container config | 🟡 Medium |
| package.json | `/package.json` | Node.js dependencies | 🟢 Low |
| composer.json | `/composer.json` | PHP dependencies | 🟢 Low |
| webpack | `/webpack.json`, `/map Files` | Source maps | 🟡 Medium |

### Git-Leakage Exploitation Workflow
1. Access `/.git/HEAD` -> get the ref path
2. Access `/.git/config` -> get the remote-repo info
3. Access `/.git/objects/` -> enumerate Git objects
4. Use GitHack/scrabble to auto-recover the source

### Sensitive-File Scan-Path List
```
/.git/config
/.git/HEAD
/.svn/entries
/.DS_Store
/.env
/.env.bak
/.env.local
/web.config
/config.php
/config.yml
/backup.sql
/database.sql
/db.sql
/phpinfo.php
/test/
/debug/
/console/
/admin/
/wp-config.php
/robots.txt
/sitemap.xml
/.well-known/security.txt
```
