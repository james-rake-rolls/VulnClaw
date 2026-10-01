# CTF Web Source-Extraction Method Reference

## Core Understanding

- CTF Web challenges often use `highlight_file(__FILE__)` to display source, which outputs HTML-colored code
- Some challenges expose part of the source only in HTML comments or hidden elements — this is by design
- **Source is an important clue but not the only one** — some challenges hide the key entry in robots.txt, response headers, hidden files, etc.

---

## Method 1: strip_tags extraction (preferred for highlight_file)

**Applies to**: pages that display source via `highlight_file()` / `show_source()`

```python
import requests, re
r = requests.get(url)
# Strip all HTML tags to get plain text
clean = re.sub(r'<[^>]+>', '', r.text)
# Optional: remove extra blank lines
clean = re.sub(r'\n{3,}', '\n\n', clean)
print(clean)
```

**Note:**
- It strips all HTML tags, so HTML strings that are genuinely part of the source are also removed
- The HTML-colored output the fetch tool returns is **not suitable for eyeballing back to source**; verify with python_execute

---

## Method 2: php://filter to read source

**Applies to**: scenarios with a file-inclusion vulnerability (`include`/`require`)

```
?page=php://filter/convert.base64-encode/resource=index.php
?page=php://filter/read=convert.base64-encode/resource=flag.php
```

After obtaining the base64-encoded source:
```python
import base64
source = base64.b64decode(base64_string).decode('utf-8')
print(source)
```

---

## Method 3: .phps extension

**Applies to**: servers configured to display PHP source

```
/learning.phps
/index.phps
```

---

## Method 4: backup files / version-control leakage

| Path | Notes |
|------|------|
| `.git/HEAD` | Git-repository leakage |
| `.svn/entries` | SVN-repository leakage |
| `index.php.bak` | backup file |
| `index.php~` | editor temp file |
| `www.zip` / `web.tar.gz` | full-site archive |
| `.index.php.swp` | Vim swap file |

---

## Method 5: HTML comments and hidden elements

Some challenges put source or hints in HTML comments:

```python
import requests, re
r = requests.get(url)
# Extract HTML-comment content
comments = re.findall(r'<!--(.*?)-->', r.text, re.DOTALL)
for c in comments:
    print(c)
```

---

## Method 6: response headers and cookies

Some challenges hide hints in the response headers:

```python
import requests
r = requests.get(url)
print("Headers:", dict(r.headers))
print("Cookies:", dict(r.cookies))
```

---

## Judging Source Completeness

After extracting the source, check whether it is complete:

| Check | Notes |
|--------|------|
| Brace matching | an `if` with no closing `}` may mean the source is truncated, or the challenge is intentionally so |
| Output statements present | if there is no `echo`/`print`/`die`, there may be code you have not seen |
| Dangerous functions present | if there is no `eval`/`system`, the RCE entry may be on another page |

**Note**: incomplete source has two possible causes —
1. The extraction method is faulty -> switch methods and re-extract
2. The challenge really exposes only this much -> keep exploring other clues (other pages, parameters, files)
