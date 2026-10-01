# OSINT Tool Usage Manual

## 1. crt.sh — Certificate-Transparency Subdomain Lookup

### Usage
```python
import requests

def query_crtsh(domain):
    """Query subdomains via crt.sh"""
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            data = r.json()
            subdomains = set()
            for entry in data:
                name = entry.get('name_value', '')
                for n in name.split('\n'):
                    n = n.strip().lower()
                    if n and '*' not in n:
                        subdomains.add(n)
            return sorted(subdomains)
    except Exception as e:
        return [f"query failed: {e}"]
    return []
```

### Note
- crt.sh can be slow; set a 30s timeout
- Results include wildcard certs (`*.example.com`); filter them out
- Return after de-duplication

## 2. GitHub API — Code and User Search

### Search Code (detect leakage)
```python
def search_github_code(query, max_results=10):
    """Search GitHub code (detect key/config leakage)"""
    url = "https://api.github.com/search/code"
    params = {'q': query, 'per_page': max_results}
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200:
        items = r.json().get('items', [])
        return [{
            'repo': item['repository']['full_name'],
            'path': item['path'],
            'url': item['html_url'],
        } for item in items]
    return []
```

### Common Search Dorks
```
"domain.com" password
"domain.com" api_key
"domain.com" secret
"domain.com" .env
filename:.env domain.com
filename:config domain.com
org:company-name password
```

## 3. DNS Queries

### Python Built-in DNS Query
```python
import socket

def dns_lookup(domain):
    """Basic DNS query"""
    results = {}
    try:
        # A record
        results['A'] = socket.gethostbyname_ex(domain)[2]
    except:
        results['A'] = 'resolution failed'
    
    return results
```

### Full DNS Query (requires dnspython)
```python
# If dnspython is available
try:
    import dns.resolver
    
    def full_dns_lookup(domain):
        record_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS']
        results = {}
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                results[rtype] = [str(r) for r in answers]
            except:
                pass
        return results
except ImportError:
    pass
```

## 4. WHOIS Lookup

### Online WHOIS APIs
```python
def whois_lookup(domain):
    """Query WHOIS via an online API"""
    # Use the whoisjson.com free API
    url = f"https://whoisjson.com/api/v1/whois?domain={domain}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {
                'registrar': data.get('registrar'),
                'creation_date': data.get('creation_date'),
                'expiration_date': data.get('expiration_date'),
                'name_servers': data.get('name_servers'),
                'registrant': data.get('registrant'),
            }
    except:
        pass
    return {}
```

## 5. Google Dorking

### Common Search Syntax
| Syntax | Purpose | Example |
|------|------|------|
| `site:` | Restrict to a domain | `site:github.com "unclec"` |
| `intitle:` | Title keyword | `intitle:"index of" site:example.com` |
| `inurl:` | URL keyword | `inurl:admin site:example.com` |
| `filetype:` | File type | `filetype:pdf site:example.com` |
| `"exact phrase"` | Exact match | `"UncleCheng" security` |
| `related:` | Related sites | `related:github.com` |

### Common Info-Gathering Dorks
```
site:github.com "target username"
site:bilibili.com "target username"
site:zhihu.com "target username"
"email@domain.com"
"phone number"
```

## 6. Shodan/Censys (API key required)

### Shodan Search
```python
def shodan_search(api_key, query):
    import shodan
    api = shodan.Shodan(api_key)
    try:
        results = api.search(query)
        return [{
            'ip': result['ip_str'],
            'port': result['port'],
            'org': result.get('org', ''),
            'data': result['data'][:200],
        } for result in results['matches'][:10]]
    except Exception as e:
        return [f"Shodan query failed: {e}"]
```

## 7. Wayback Machine

### Query Historical Snapshots
```python
def wayback_query(domain):
    """Query Wayback Machine historical snapshots"""
    url = f"http://archive.org/wayback/available?url={domain}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            snapshots = data.get('archived_snapshots', {})
            if snapshots.get('closest'):
                return snapshots['closest']['url']
    except:
        pass
    return None
```

## 8. Same-Server Lookup (reverse-lookup domains on the same IP)

### Online Tools
| Tool | URL | Notes |
|------|-----|------|
| Chinaz tools | https://stool.chinaz.com/same | Most common in China |
| Threatbook | https://x.threatbook.cn | Threat intel + same-server |
| crt.sh | https://crt.sh | Look up cert-associated domains by IP |
| Censys | https://search.censys.io | Global asset search |
| Fofa | https://fofa.info | Cyberspace search engine |

### python_execute Same-Server Lookup
```python
import requests

def reverse_ip_lookup(ip):
    """Reverse-lookup same-IP domains via crt.sh"""
    domains = set()
    try:
        r = requests.get(f"https://crt.sh/?q={ip}&output=json", timeout=30)
        if r.status_code == 200:
            for entry in r.json():
                for name in entry.get('name_value', '').split('\n'):
                    name = name.strip()
                    if name and '*' not in name:
                        domains.add(name)
    except Exception as e:
        print(f"crt.sh query failed: {e}")
    return sorted(domains)

# Usage
ip = "1.2.3.4"
result = reverse_ip_lookup(ip)
print(f"[+] Same-IP domains ({len(result)}):")
for d in result:
    print(f"  - {d}")
```

## 9. C-Block Lookup (live hosts in the same subnet)

### Online Tools
| Tool | URL | Notes |
|------|-----|------|
| Fofa | https://fofa.info | `ip="1.2.3.0/24"` |
| Shodan | https://www.shodan.io | `net:1.2.3.0/24` |
| Censys | https://search.censys.io | `ip:/1.2.3.0-1.2.3.255/` |

### python_execute C-Block Scan
```python
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_c_segment(ip, timeout=1, max_workers=100):
    """Scan the C-block for live hosts"""
    prefix = ".".join(ip.split(".")[:3])
    alive = []

    def check(host_ip):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            result = s.connect_ex((host_ip, 80))
            s.close()
            if result == 0:
                return host_ip
        except:
            pass
        return None

    targets = [f"{prefix}.{i}" for i in range(1, 255)]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check, t): t for t in targets}
        for future in as_completed(futures):
            result = future.result()
            if result:
                alive.append(result)

    return sorted(alive, key=lambda x: int(x.split(".")[-1]))

# Usage
ip = "1.2.3.4"
hosts = scan_c_segment(ip)
print(f"[+] Live hosts in the C-block ({len(hosts)}):")
for h in hosts:
    print(f"  - {h}")
```

## 10. ICP-Filing Lookup

### Online Tools
| Tool | URL | Notes |
|------|-----|------|
| MIIT filing lookup | https://beian.miit.gov.cn | Official authority |
| Chinaz filing lookup | https://icp.chinaz.com | Convenient lookup |
| Tianyancha | https://www.tianyancha.com | Company + filing correlation |
| Aizhan filing lookup | https://www.aizhan.com/cha/ | Batch lookup |

### python_execute ICP-Filing Lookup
```python
import requests

def icp_lookup(domain):
    """Query ICP filing info (via a public API)"""
    # Method 1: use the chinaz API (API key required)
    # Method 2: use a public lookup endpoint
    try:
        # Use whois to look up Chinese-domain info
        url = f"https://whois.chinaz.com/{domain}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get(url, headers=headers, timeout=10)
        # Parse the filing info
        import re
        icp_match = re.search(r'备案号[：:]\s*([^<\s]+)', r.text)
        if icp_match:
            return icp_match.group(1)
    except:
        pass

    # Overseas domains usually have no ICP filing
    return "no filing found (possibly an overseas domain)"
```

## 11. Subdomain Discovery (multiple methods)

### Method-Combination Strategy
1. **crt.sh** — certificate transparency (fastest)
2. **Search-engine dorks** — Google/Bing site: searches
3. **DNS brute force** — a common-prefix wordlist
4. **DNS zone transfer** — try axfr
5. **JS-file analysis** — extract subdomains from the page's JS

### python_execute Subdomain Brute Force
```python
import socket
from concurrent.futures import ThreadPoolExecutor

def subdomain_brute(domain, wordlist=None, max_workers=20):
    """Subdomain brute force"""
    if wordlist is None:
        wordlist = [
            'www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'staging',
            'api', 'test', 'portal', 'cdn', 'ns1', 'ns2', 'mx',
            'app', 'web', 'git', 'ci', 'jenkins', 'jira',
            'vpn', 'remote', 'shop', 'store', 'news',
        ]

    found = []
    def check(sub):
        fqdn = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(fqdn)
            return (fqdn, ip)
        except:
            return None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(check, wordlist)
        found = [r for r in results if r]

    return sorted(found, key=lambda x: x[0])

# Usage
domain = "example.com"
subs = subdomain_brute(domain)
print(f"[+] Subdomains found ({len(subs)}):")
for sub, ip in subs:
    print(f"  - {sub} → {ip}")
```

### DNS Zone-Transfer Attempt
```python
import socket

def try_zone_transfer(domain):
    """Attempt a DNS zone transfer"""
    # Get the NS records
    try:
        ns_servers = socket.getaddrinfo(domain, None)
    except:
        return []

    # Try a zone transfer against each NS server
    # Note: modern DNS servers usually disable this
    import subprocess
    results = []
    try:
        result = subprocess.run(
            ['dig', 'axfr', domain, '@' + domain],
            capture_output=True, text=True, timeout=10
        )
        if 'XFR size' in result.stdout:
            results.append(result.stdout)
    except:
        pass

    return results
```
