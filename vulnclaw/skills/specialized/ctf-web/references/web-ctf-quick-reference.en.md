# CTF Web Quick Reference

## Common flag Locations

### Linux
```
/flag
/flag.txt
/flag.php
/var/www/html/flag.php
/home/ctf/flag
/root/flag
/tmp/flag
/opt/flag
/srv/flag
```

### Docker / Environment Variables
```
/proc/self/environ
/environment
/.env
```

### PHP-Specific
```php
// the flag inside phpinfo()
// view the environment-variable section
// view custom sections

// common flag filenames
flag.php
flag.txt
f1ag.php
fl4g.php
fl@g.php
th1s_1s_flag.php
```

## First-Pass Workflow

```
1. Access the target URL
   -> view page source (Ctrl+U)
   -> check HTTP headers (Server, X-Powered-By, Set-Cookie)
   -> inspect cookie values (base64/JWT/serialized)

2. Check for hidden information
   → robots.txt
   → .git/HEAD
   → .svn/
   -> backup files: index.php.bak, www.zip, .index.php.swp, index.php~
   → DS_Store: .DS_Store

3. Directory scan
   → /flag, /admin, /login, /upload, /api, /debug
   → /phpinfo.php, /info.php, /test.php
   → /console (Flask Debug), /actuator (Spring Boot)

4. If source is available -> code audit
   -> see php-code-audit-checklist.md

5. If no source -> active probing
   -> SQL-injection testing
   -> XSS testing
   -> file upload
   -> SSTI testing
   → LFI/RFI
```

## Quick-Test Commands

```bash
# Check basic info
curl -I http://target/              # HTTP headers
curl http://target/robots.txt        # robots
curl http://target/.git/HEAD         # git leakage

# Common injection tests
' OR 1=1 --                          # SQLi
{{7*7}}                              # SSTI
<script>alert(1)</script>            # XSS
../../../etc/passwd                  # LFI
```

## Common Response-Header Hints

| Response header | Meaning | Next step |
|--------|------|--------|
| `X-Forwarded-For: 127.0.0.1` | requires local access | add an X-Forwarded-For header |
| `Server: nginx/1.x` | server type | search for known CVEs |
| `X-Powered-By: PHP/7.x` | PHP version | PHP-specific vulnerabilities |
| `Set-Cookie: role=guest` | access control | modify the cookie |
| `Hint: xxx` | a direct hint | follow the hint |
| `Flag: xxx` | sometimes right in the header | check all response headers |

## Common Chain Shapes

### PHP Simple Chain
```
URL -> source -> find the filter -> bypass the filter -> RCE -> read the flag
```

### PHP Multi-Step Chain
```
entry page -> find a hint -> follow the redirect -> find a new page -> get the source -> analyze and exploit -> RCE
```

### File-Inclusion Chain
```
LFI -> read source (php://filter) -> find an inclusion point -> log poisoning / session inclusion -> RCE
```

### SQL-Injection Chain
```
login box -> SQLi -> read data -> find the admin password -> log into the backend -> upload a webshell -> RCE
```

### Deserialization Chain
```
controllable serialized data -> analyze available gadgets -> build the exploit chain -> RCE/SSRF/file read
```

## Common Encoding/Encryption Clues

| Trait | Likely encoding | Decoding method |
|------|---------|---------|
| trailing `=` | Base64 | `crypto_decode base64_decode` |
| `0-9a-f` even length | Hex | `crypto_decode hex_decode` |
| `%XX` | URL encoding | `crypto_decode url_decode` |
| `&#xNN;` | HTML entity | `crypto_decode html_decode` |
| `\uXXXX` | Unicode escape | `crypto_decode unicode_decode` |
| three `.`-separated parts | JWT | `crypto_decode jwt_decode` |
| dots and dashes | Morse | `crypto_decode morse_decode` |
| Unreadable but looks like letters | ROT13/Caesar | `crypto_decode rot13_decode` |
