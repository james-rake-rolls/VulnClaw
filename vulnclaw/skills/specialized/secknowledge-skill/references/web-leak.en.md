# Web Security - Information Disclosure

> Source: WooYun vulnerability database | split from web-file-infra.md

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

