# Website Information-Gathering Reference

## 1. Site-Architecture Identification

### Tech-Stack Inference Methods
1. **HTTP response headers** — Server, X-Powered-By, Set-Cookie traits
2. **HTML-source traits** — meta generator, specific class/id naming
3. **JS-file paths** — /static/js/app.js, /wp-content/, /assets/
4. **Cookie names** — PHPSESSID (php), JSESSIONID (Java), _rails_session (Rails)
5. **URL paths** — ?id= (PHP), /api/ (REST), /wp-admin/ (WordPress)

### Common Architecture Combinations
| Language | Framework | Database | Server | Traits |
|------|------|--------|--------|------|
| PHP | Laravel | MySQL | Apache/Nginx | Set-Cookie: laravel_session |
| PHP | WordPress | MySQL | Apache | /wp-content/, /wp-admin/ |
| Python | Django | PostgreSQL | Nginx+Gunicorn | CSRF middleware cookie |
| Python | Flask | SQLite/MySQL | Nginx+uWSGI | Set-Cookie: session= |
| Java | Spring | MySQL/Oracle | Tomcat | JSESSIONID |
| Node.js | Express | MongoDB | Nginx | X-Powered-By: Express |
| Ruby | Rails | PostgreSQL | Nginx+Puma | _rails_session |

### python_execute Architecture Probing
```python
import requests

url = "https://target.com"
r = requests.get(url, timeout=10)

# 1. Response-header analysis
headers = r.headers
print(f"Server: {headers.get('Server', 'N/A')}")
print(f"X-Powered-By: {headers.get('X-Powered-By', 'N/A')}")

# 2. Cookie analysis
cookies = r.cookies
for cookie in cookies:
    print(f"Cookie: {cookie.name} = {cookie.value[:20]}...")

# 3. HTML-trait analysis
html = r.text
# WordPress
if 'wp-content' in html or 'wp-includes' in html:
    print("[+] WordPress detected")
# Laravel
if 'laravel_session' in str(cookies):
    print("[+] Laravel detected")
# Django
if 'csrftoken' in str(cookies) or 'csrfmiddlewaretoken' in html:
    print("[+] Django detected")
# Hexo
if 'hexo' in html.lower():
    print("[+] Hexo blog detected")
# Hugo
if 'hugo' in html.lower():
    print("[+] Hugo blog detected")
```

## 2. Web Fingerprinting

### CMS Fingerprint Traits
| CMS | Signature path | Signature string |
|-----|---------|-----------|
| WordPress | /wp-login.php, /wp-content/ | wp-content, xmlrpc.php |
| Joomla | /administrator/ | /media/jui/ |
| Drupal | /misc/drupal.js | Drupal.settings |
| Discuz | /forum.php | discuz_uid |
| Typecho | /admin/login.php | typecho |
| Hexo | /archives/ | hexo |
| Ghost | /ghost/ | ghost-frontend |

### Front-End Framework Traits
| Framework | Traits |
|------|------|
| React | data-reactroot, __NEXT_DATA__ |
| Vue.js | data-v-xxx, __vue__ |
| Angular | ng-version, _nghost |
| jQuery | jQuery in scripts |
| Bootstrap | bootstrap.css/js |

### python_execute Fingerprinting
```python
import requests, re

url = "https://target.com"
r = requests.get(url, timeout=10)
html = r.text

# CMS detection
cms_signatures = {
    "WordPress": ["wp-content", "wp-includes", "wp-admin"],
    "Joomla": ["/administrator/", "media/jui"],
    "Drupal": ["Drupal.settings", "/misc/drupal"],
    "Hexo": ["hexo", "/archives/"],
    "Hugo": ["hugo", "gohugo"],
    "Ghost": ["ghost-frontend", "/ghost/"],
}

for cms, sigs in cms_signatures.items():
    if any(sig in html for sig in sigs):
        print(f"[+] CMS: {cms}")

# Front-end framework detection
fw_signatures = {
    "React": ["data-reactroot", "__NEXT_DATA__", "react"],
    "Vue.js": ["data-v-", "__vue__", "vue"],
    "Angular": ["ng-version", "_nghost", "angular"],
    "jQuery": ["jquery", "jQuery"],
    "Bootstrap": ["bootstrap"],
}

for fw, sigs in fw_signatures.items():
    if any(sig.lower() in html.lower() for sig in sigs):
        print(f"[+] Front-end framework: {fw}")

# Extract JS files
js_files = re.findall(r'src=["\']([^"\']*\.js[^"\']*)["\']', html)
print(f"JS files: {js_files[:10]}")
```

## 3. WAF Detection

### Common WAF Traits
| WAF | Block trait |
|-----|---------|
| Cloudflare | Server: cloudflare, CF-Ray header |
| AWS WAF | Server: AmazonS3, x-amz-request-id |
| Aliyun WAF | Set-Cookie contains acw_tc |
| Tencent Cloud WAF | Specific block page |
| BaoTa WAF | Block page contains "BaoTa" |
| SafeDog | Block page contains "safedog" |
| ModSecurity | Specific 403 response |

### python_execute WAF Detection
```python
import requests

url = "https://target.com"

# 1. Normal request
r1 = requests.get(url)

# 2. WAF-triggering request
waf_payloads = [
    "/?id=1' OR 1=1--",
    "/?search=<script>alert(1)</script>",
    "/../../../etc/passwd",
    "/?file=php://filter/convert.base64-encode/resource=index",
]

for payload in waf_payloads:
    r2 = requests.get(url + payload, allow_redirects=False)
    # Status-code change
    if r2.status_code in [403, 406, 429, 501]:
        print(f"[!] WAF detected: {payload} -> {r2.status_code}")
    # Significant response-length change
    if abs(len(r2.text) - len(r1.text)) > 500:
        print(f"[!] Response-length change: normal={len(r1.text)}, attack={len(r2.text)}")

# 3. Check WAF-specific response headers
waf_headers = {
    "cloudflare": ["cf-ray", "server: cloudflare"],
    "aws": ["x-amz-request-id", "x-amz-cf-id"],
    "Aliyun": ["acw_tc"],
}
for waf_name, sigs in waf_headers.items():
    for sig in sigs:
        if sig in str(r1.headers).lower():
            print(f"[+] WAF detected: {waf_name}")
```

## 4. Sensitive Directories & Files

### Common Sensitive-Path List
```
/robots.txt
/sitemap.xml
/.git/
/.svn/
/.env
/.DS_Store
/web.config
/config.php
/config.yml
/backup/
/admin/
/login/
/api/
/swagger/
/graphql
/phpinfo.php
/test/
/debug/
/console/
/actuator/
/.well-known/
```

### python_execute Directory Scan
```python
import requests

target = "https://target.com"
paths = [
    "/robots.txt", "/sitemap.xml", "/.git/", "/.env", "/.DS_Store",
    "/admin/", "/backup/", "/config.php", "/api/", "/phpinfo.php",
    "/.git/config", "/.git/HEAD", "/wp-config.php",
    "/swagger/", "/graphql", "/actuator/",
]

for path in paths:
    try:
        r = requests.get(target + path, timeout=5, allow_redirects=False)
        if r.status_code in [200, 301, 302, 401, 403]:
            print(f"[{r.status_code}] {path}")
    except:
        pass
```

## 5. Source-Leakage Check

### Common Source-Leakage Types
| Type | Path | Detection method |
|------|------|---------|
| Git repo | /.git/config, /.git/HEAD | 200 and contains git content |
| SVN repo | /.svn/entries | 200 and contains svn content |
| .DS_Store | /.DS_Store | Download and parse |
| .env file | /.env | Contains DB_PASSWORD, etc. |
| web.config | /web.config | IIS config |
| Backup files | /.bak, /.swp, /.old, /~ | Direct download |
| Docker | /Dockerfile, /docker-compose.yml | Container config |
| package.json | /package.json | Node.js dependencies |
| composer.json | /composer.json | PHP dependencies |

### Git-Repository Leakage Exploitation
```python
import requests

target = "https://target.com"

# 1. Check .git/HEAD
r = requests.get(f"{target}/.git/HEAD")
if r.status_code == 200 and "ref:" in r.text:
    print("[!] Git repository leaked!")
    # 2. Try to get the ref
    ref_path = r.text.strip().split("ref: ")[1] if "ref: " in r.text else ""
    if ref_path:
        r2 = requests.get(f"{target}/.git/{ref_path}")
        if r2.status_code == 200:
            print(f"[+] Git ref: {r2.text.strip()}")

# 3. Try to get the config
r3 = requests.get(f"{target}/.git/config")
if r3.status_code == 200:
    print(f"[+] Git config:\n{r3.text}")
```

## 6. Same-Server Lookup (reverse-lookup domains on the same IP)

### Lookup Methods
1. **Chinaz webmaster tools** — https://stool.chinaz.com/same
2. **Threatbook** — https://x.threatbook.cn
3. **crt.sh** — look up cert-associated domains by IP
4. **Censys** — https://search.censys.io

### python_execute Same-Server Lookup
```python
import requests, json

ip = "1.2.3.4"

# Method 1: query same-IP certs via crt.sh
r = requests.get(f"https://crt.sh/?q={ip}&output=json", timeout=15)
if r.status_code == 200:
    domains = set()
    for entry in r.json():
        for name in entry.get('name_value', '').split('\n'):
            if name.strip() and '*' not in name:
                domains.add(name.strip())
    print(f"[+] Same-IP domains ({len(domains)}):")
    for d in sorted(domains):
        print(f"  - {d}")
```

## 7. C-Block Lookup (live hosts in the same subnet)

### python_execute C-Block Scan
```python
import requests, socket
from concurrent.futures import ThreadPoolExecutor

# Get the IP from the domain
domain = "target.com"
ip = socket.gethostbyname(domain)
# Extract the C-block
c_segment = ".".join(ip.split(".")[:3])

def check_host(ip, timeout=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, 80))
        s.close()
        if result == 0:
            return ip
    except:
        pass
    return None

# Scan the C-block (1-254)
alive_hosts = []
with ThreadPoolExecutor(max_workers=50) as executor:
    ips = [f"{c_segment}.{i}" for i in range(1, 255)]
    results = executor.map(check_host, ips)
    alive_hosts = [ip for ip in results if ip]

print(f"[+] Live hosts in the C-block: {alive_hosts}")
```
