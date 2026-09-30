# SQL Injection One-Pass Field Quick Reference

> Source: fushuling, "SQL Injection One-Pass!"
> URL: https://fushuling.com/index.php/2023/04/07/sql%E6%B3%A8%E5%85%A5%E4%B8%80%E5%91%BD%E9%80%9A%E5%85%B3/
> Published: 2023-04-07
>
> This entry is an original quick-reference note compiled by VulnClaw from public articles, not a full mirror of the originals. Use it only within authorized CTF, ranges, SRC, or explicitly authorized testing.

## Applicable Scenarios

- A controllable parameter exists in a page, endpoint, cookie, or request header, e.g. `id`, `search`, `keyword`, `user`, `pass`, `sort`, `page`.
- The target exhibits SQL errors, boolean differences, delayed responses, echo positions, login bypass, or WAF-filtering traces.
- When a CTF web challenge already shows a clear form, GET parameter, or hint, test the visible entry first; don't burn many rounds on directory brute-forcing first.
- You need to organize manual SQLi evidence, sqlmap acceleration, tamper/WAF bypass, blind injection, and report evidence into one reproducible path.

## Model-Led Execution Principles

1. First find the real input surface: HTML form `action/method/name`, URL query string, XHR/API, cookies, Referer, User-Agent, X-Forwarded-For.
2. If the page source already shows a `form` or `name=id`, request that endpoint directly and build parameters; don't get dragged off by uniform 200s, pointless directory scans, or a templating phase.
3. Verify one hypothesis at a time: closure, column count, echo position, database type, filter rules, and whether multiple statements are supported.
4. Use `fetch` for simple requests; use `http_probe_batch` when you need to batch-compare true/false, order by, union, or time payloads; use `python_execute` only for blind-injection loops, encoding combinations, or complex parsing.
5. Judging results relies on evidence differences: status code, length, body hash, title, key fragments, error text, response time. Don't call it success just because "the payload was sent."

## Minimum Evidence Gate

| Conclusion | evidence that must be recorded |
| --- | --- |
| SQL injection present | original URL/method/parameters, baseline response, true/false or error/time differences |
| Union-queryable | `order by` or equivalent column-probing evidence, echo-position evidence, a successfully echoed test value |
| Blind-injectable | a stable true/false or delay difference, cross-verified over at least two rounds |
| Stackable | observable side effects or echo changes from multiple statements; confirm authorization in real environments |
| Flag/sensitive data obtained | data appearing verbatim in tool output; keep the request, response, and evidence numbers |
| Writable file / command execution | explicit authorization scope, database privileges, target-path / command-output evidence |

## Manual-Verification Decision Tree

### 1. Baseline and Closure

- First request a normal value, e.g. `id=1`, and save the length, hash, page title, and key fragments.
- Try single quote, double quote, parenthesis, backslash, and comment characters in turn, watching for errors or changes in page structure.
- For numeric parameters prefer comparing `id=1`, `id=2-1`, `id=1*1`; for string parameters prefer comparing true/false after closure.

### 2. Boolean and Time Differences

- Boolean verification: construct always-true/always-false conditions and compare response content, not just the status code.
- Time verification: use only when boolean is blind or page differences are unstable; first establish the normal response-time range, then confirm with a delay function over two rounds.
- When delay functions are filtered, try database-specific alternatives: compute-heavy delays, lock waits, regex backtracking, Cartesian products, or error-function side effects.

### 3. Union Query

- Use `order by N` or `group by N` to determine the column count; the failure boundary is the upper bound on columns.
- Use a negative or nonexistent ID so the original query returns nothing, then `union select` recognizable numbers to confirm the echo positions.
- For MySQL 5.0+ prefer `information_schema`: database → table → column → data.
- When there is no `information_schema` or filtering is heavy, switch to blind injection, no-column-name injection, join-based column-name extraction, or guessing business table names.

### 4. Stacked Queries, Prepared Statements, and Special Syntax

- Stacked injection only works when the target's execution environment supports multiple statements; many front ends only echo the first query's result.
- If keywords are filtered, consider CTF tricks such as prepared statements, string concatenation, `handler` reads, and renaming tables/columns.
- Such operations can change database state; they are forbidden by default on real SRC/production targets, and even on CTF/ranges keep evidence of the operation.

### 5. Error-Based Injection

- When the target returns database errors, prefer error functions to exfiltrate query results.
- Common MySQL error-based paths include XML/geometry/math errors; available functions differ by version, so probe the version and error format first.
- If errors are uniformly hidden, fall back to boolean, time, or union-query approaches.

### 6. Unconventional Entry Points

- Relayed injection: when data written by request A is concatenated and executed by request B, record the full trigger chain.
- DNSLog out-of-band: use only within authorized scope; suited to blind scenarios that can trigger outbound DNS/HTTP.
- For pseudo-static, LIMIT, second-order, encoded, HTTP-header, and file-type injection, first prove the location really reaches the SQL semantic layer.

## WAF and Filter-Bypass Strategy

| Filtering behavior | preferred strategy |
| --- | --- |
| Case-sensitive keyword filtering | random case, keyword splitting, double-writing |
| Spaces filtered | comments, newlines, tabs, parentheses, plus signs, database whitespace characters |
| Quotes filtered | hex, `CHAR()`, backslash closure, numeric semantics |
| Commas filtered | `from ... to`, `join`, `offset`, function substitutes |
| Comparison operators filtered | `between`, `like`, `regexp/rlike`, `in`, string-comparison functions |
| `and/or/not/xor` filtered | symbol substitution, nested conditions, arithmetic or bitwise equivalents |
| Comment characters filtered | complete the statement after closure, balance parentheses, newline or inline-comment variants |
| sqlmap signatures uniformly blocked | `--random-agent`, lower concurrency, specify the parameter, choose tamper by evidence |

## sqlmap Acceleration Rules

sqlmap suits accelerating enumeration after an injection point is confirmed manually; it should not replace the earlier entry-point identification.

```bash
# GET injection point
sqlmap -u "https://target/path.php?id=1" -p id --batch

# POST / complex request: save the original request packet first
sqlmap -r request.txt -p id --batch

# Current database, tables/columns, field data
sqlmap -u "https://target/path.php?id=1" --current-db --batch
sqlmap -u "https://target/path.php?id=1" -D dbname --tables --batch
sqlmap -u "https://target/path.php?id=1" -D dbname -T users --columns --batch
sqlmap -u "https://target/path.php?id=1" -D dbname -T users -C username,password --dump --batch

# Custom SQL shell, authorized environments only
sqlmap -r request.txt -p id --sql-shell
```

Use high-risk parameters only in authorized ranges/CTFs: `--file-read`, `--file-write`, `--file-dest`, `--os-cmd`, `--os-shell`, stacked writes, or writing a webshell.

## tamper Selection Quick Reference

| Goal | common tamper direction |
| --- | --- |
| Whitespace mutation | `space2comment`, `space2plus`, `space2randomblank`, database-specific whitespace |
| Encoding mutation | URL encoding, Unicode encoding, Base64 wrapping, percent-sign insertion |
| Keyword forms | random case, double-writing, inline comments, `union all` → `union` |
| Comparison-operator substitutes | `between`, `greatest/least`, `like`, `regexp/rlike` |
| Specific databases | MSSQL log obfuscation, ASP/ASP.NET encoding, MySQL version comments |
| Custom WAF | write a minimal tamper: change only the blocked token, keeping the payload's semantics and readable evidence |

## VulnClaw Self-Check Notes

- If three requests yield no new evidence, review the HTML source/forms/network requests first; don't keep trying random paths or payloads.
- If the target returns 200 for any path, a directory scan can only conclude "path enumeration is ineffective" and cannot invalidate a known endpoint.
- If the user's goal is a CTF flag, take the shortest verifiable path: entry → parameter → difference → enumeration → flag.
- If the model wants to use sqlmap, first require it to state the confirmed parameter, method, closure, or response differences.
- If the current direction is making progress but isn't done, don't stop at a fixed round count; keep iterating around the confirmed entry until flag/report/asking the user.

## Retrieval Keywords

SQL injection, SQLi, sqlmap, tamper, WAF bypass, union injection, boolean blind, time blind, error based, stacked query, information_schema, DNSLog, second order injection, wide byte, no column name injection, handler, prepare, CTF Web, SRC evidence.
