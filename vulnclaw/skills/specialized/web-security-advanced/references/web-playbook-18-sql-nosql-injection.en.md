# SQL/NoSQL Injection
English: SQL/NoSQL Injection
- Entry Count: 17
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## MySQL Injection - Basic Probing
- ID: sqli-mysql-basic
- Difficulty: beginner
- Subcategory: MySQL
- Tags: sqli, mysql, injection, database
- Original Extracted Source: original extracted web-security-wiki source/sqli-mysql-basic.md
Description:
MySQL basic-probing and data-extraction injection techniques
Prerequisites:
- The target has a SQL-injection point
- The back-end database is MySQL
- Understand basic SQL syntax
Execution Outline:
1. 1. Probe for injection points
2. 2. Determine the number of columns
3. 3. Determine the display location
4. 4. Obtain database information
## MySQL Injection - Advanced Techniques
- ID: sqli-mysql-advanced
- Difficulty: advanced
- Subcategory: MySQL
- Tags: sqli, mysql, advanced, file-read, rce
- Original Extracted Source: original extracted web-security-wiki source/sqli-mysql-advanced.md
Description:
MySQL advanced injection techniques: file read/write, UDF privilege escalation, command execution
Prerequisites:
- The MySQL user has the FILE privilege
- Know the site's absolute path
- secure_file_priv is configured to allow it
Execution Outline:
1. 1. Detect the FILE privilege
2. 2. Obtain the site path
3. 3. Read sensitive files
4. 4. Write a web shell
## MSSQL Injection - Basic Probing
- ID: sqli-mssql-basic
- Difficulty: intermediate
- Subcategory: MSSQL
- Tags: sqli, mssql, sqlserver, injection
- Original Extracted Source: original extracted web-security-wiki source/sqli-mssql-basic.md
Description:
Microsoft SQL Server database-injection techniques
Prerequisites:
- The target has a SQL-injection point
- The back end uses an MSSQL database
Execution Outline:
1. 1. Probe for injection points
2. 2. Obtain version information
3. 3. Obtain user information
4. 4. Obtain database information
## MSSQL Injection - Advanced Techniques
- ID: sqli-mssql-advanced
- Difficulty: advanced
- Subcategory: MSSQL
- Tags: sqli, mssql, xp_cmdshell, rce
- Original Extracted Source: original extracted web-security-wiki source/sqli-mssql-advanced.md
Description:
MSSQL advanced injection: command execution via xp_cmdshell and SP_OACREATE
Prerequisites:
- MSSQL has high privileges
- xp_cmdshell is available or can be enabled
Execution Outline:
1. 1. Detect the xp_cmdshell state
2. 2. Enable xp_cmdshell
3. 3. Execute system commands
4. 4. Write a web shell
## Oracle Injection - Basic Probing
- ID: sqli-oracle-basic
- Difficulty: intermediate
- Subcategory: Oracle
- Tags: sqli, oracle, injection
- Original Extracted Source: original extracted web-security-wiki source/sqli-oracle-basic.md
Description:
Oracle database basic-injection techniques
Prerequisites:
- The target has a SQL-injection point
- The back end uses an Oracle database
Execution Outline:
1. 1. Probe for injection points
2. 2. Obtain version information
3. 3. Obtain user information
4. 4. Obtain table names
## Oracle Injection - Advanced Techniques
- ID: sqli-oracle-advanced
- Difficulty: advanced
- Subcategory: Oracle
- Tags: sqli, oracle, advanced, rce
- Original Extracted Source: original extracted web-security-wiki source/sqli-oracle-advanced.md
Description:
Oracle advanced injection techniques: Java stored procedures, UTL_FILE file operations
Prerequisites:
- Oracle high privileges
- A Java Virtual Machine is available
Execution Outline:
1. 1. Detect Java privileges
2. 2. Create a Java execution function
3. 3. UTL_FILE file read
## PostgreSQL Injection - Basic Probing
- ID: sqli-postgres-basic
- Difficulty: intermediate
- Subcategory: PostgreSQL
- Tags: sqli, postgresql, postgres, injection
- Original Extracted Source: original extracted web-security-wiki source/sqli-postgres-basic.md
Description:
PostgreSQL database-injection techniques
Prerequisites:
- The target has a SQL-injection point
- The back end uses PostgreSQL
Execution Outline:
1. 1. Probe for injection points
2. 2. Obtain version information
3. 3. Obtain table names
4. 4. Obtain column names
## SQLite Injection
- ID: sqli-sqlite-basic
- Difficulty: intermediate
- Subcategory: SQLite
- Tags: sqli, sqlite
- Original Extracted Source: original extracted web-security-wiki source/sqli-sqlite-basic.md
Description:
SQLite database injection
Prerequisites:
- A SQLite database
- An injection point exists
Execution Outline:
1. 1. Probe for injection points
2. 2. Obtain the version
3. 3. Obtain table names
4. 4. Obtain the table structure
## MongoDB Injection
- ID: sqli-mongodb-basic
- Difficulty: intermediate
- Subcategory: MongoDB
- Tags: nosql, mongodb, injection
- Original Extracted Source: original extracted web-security-wiki source/sqli-mongodb-basic.md
Description:
NoSQL database injection techniques
Prerequisites:
- The target uses MongoDB
- User input is concatenated into a query
Execution Outline:
1. 1. Probe for injection points
2. 2. Bypass authentication
3. 3. Logical-operator injection
4. 4. Regex injection
## Redis Unauthorized Access
- ID: sqli-redis
- Difficulty: intermediate
- Subcategory: Redis
- Tags: redis, nosql, injection
- Original Extracted Source: original extracted web-security-wiki source/sqli-redis.md
Description:
Redis unauthorized access and command injection
Prerequisites:
- The Redis service is reachable
- Unauthenticated or a weak password
Execution Outline:
1. 1. Probe Redis
2. 2. Unauthorized access
3. 3. Write a webshell
4. 4. Write an SSH public key
## Boolean-Based Blind Injection
- ID: sqli-blind
- Difficulty: intermediate
- Subcategory: Blind injection
- Tags: sqli, blind, boolean
- Original Extracted Source: original extracted web-security-wiki source/sqli-blind.md
Description:
Boolean-condition-based blind SQL injection techniques
Prerequisites:
- A SQL injection exists
- The page has two distinct true/false responses
Execution Outline:
1. 1. Confirm blind injection
2. 2. Obtain the database-name length
3. 3. Enumerate the database name character by character
4. 4. Automate with tools
## Time-Based Blind Injection
- ID: sqli-time-based
- Difficulty: intermediate
- Subcategory: Blind injection
- Tags: sqli, blind, time
- Original Extracted Source: original extracted web-security-wiki source/sqli-time-based.md
Description:
Time-delay-based blind SQL injection techniques
Prerequisites:
- A SQL injection exists
- The page response time is controllable
Execution Outline:
1. 1. Confirm time-based blind injection
2. 2. Obtain the database-name length
3. 3. Character-by-character extraction
4. 4. Delay functions for different databases
## Error-Based Injection
- ID: sqli-error-based
- Difficulty: intermediate
- Subcategory: Error-based injection
- Tags: sqli, error, extractvalue
- Original Extracted Source: original extracted web-security-wiki source/sqli-error-based.md
Description:
SQL injection that extracts data via error messages
Prerequisites:
- A SQL injection exists
- Error messages are displayed on the page
Execution Outline:
1. 1. Confirm error-based injection
2. 2. Obtain database information
3. 3. Obtain table names
4. 4. Obtain data
## Second-Order SQL Injection
- ID: sqli-second-order
- Difficulty: advanced
- Subcategory: Second-order injection
- Tags: sqli, second-order, stored
- Original Extracted Source: original extracted web-security-wiki source/sqli-second-order.md
Description:
SQL injection triggered after storage
Prerequisites:
- A data-storage feature exists
- Stored data is reused later
Execution Outline:
1. 1. Probe for second-order injection
2. 2. Username injection
3. 3. Password-reset injection
4. 4. Order/comment injection
## Union-Based Injection
- ID: sqli-union
- Difficulty: beginner
- Subcategory: Union query
- Tags: sqli, union, select
- Original Extracted Source: original extracted web-security-wiki source/sqli-union.md
Description:
Use UNION SELECT to extract data
Prerequisites:
- An injection point exists
- Can display query results
Execution Outline:
1. 1. Determine the number of columns
2. 2. Determine the displayed columns
3. 3. Extract data
4. 4. Bypass filtering
## Stacked-Query Injection
- ID: sqli-stacked
- Difficulty: intermediate
- Subcategory: Stacked queries
- Tags: sqli, stacked, queries
- Original Extracted Source: original extracted web-security-wiki source/sqli-stacked.md
Description:
Injection that executes multiple SQL statements
Prerequisites:
- Multi-statement execution is supported
- MySQL/PostgreSQL/MSSQL
Execution Outline:
1. 1. Probe for stacked queries
2. 2. MySQL stacked queries
3. 3. MSSQL stacked queries
4. 4. PostgreSQL stacked queries
## SQL-Injection WAF Bypass
- ID: sqli-waf-bypass
- Difficulty: advanced
- Subcategory: WAF bypass
- Tags: sqli, waf, bypass
- Original Extracted Source: original extracted web-security-wiki source/sqli-waf-bypass.md
Description:
Techniques to bypass a web application firewall
Prerequisites:
- The target has a SQL-injection point
- A WAF is in place
Execution Outline:
1. Chunked transfer encoding
2. HTTP parameter pollution (HPP)
3. Equivalent-function substitution
4. Comma-less injection

