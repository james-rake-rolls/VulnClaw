# PHP Code-Audit Checklist

## Step 1: Identify Input Entry Points

### Superglobals
```php
$_GET['param']        // URL query parameter
$_POST['param']       // POST form data
$_REQUEST['param']    // GET + POST + COOKIE
$_COOKIE['param']     // cookie value
$_SERVER['HTTP_X']    // HTTP request header
$_FILES['file']       // uploaded file
$_SESSION['key']      // session data (if controllable)
```

### Hidden Input
```php
php://input           // raw POST data
getallheaders()       // all HTTP headers
getenv()              // environment variables
file_get_contents()   // read from a file/URL
```

## Step 2: Identify Dangerous Functions

### Code Execution
```php
eval()                // execute arbitrary PHP code
assert()              // executes code in PHP < 7
preg_replace(/e)      // the /e modifier executes the replacement result
create_function()     // create an anonymous function
call_user_func()      // call a callback function
call_user_func_array()// call a callback function (array args
array_map()           // apply a callback to array elements
usort()               // custom sort (callback injectable
array_filter()        // filter an array (callback injectable
```

### Command Execution
```php
system()              // run an external program, output the result
exec()                // run an external program, return the last line
shell_exec()          // run a command, return the full output
passthru()            // run an external program, output raw data
popen()               // open a process pipe
proc_open()           // open a process (more flexible
pcntl_exec()          // execute a program (requires the pcntl extension
backticks `cmd`        // equivalent to shell_exec()
```

### File Operations
```php
include() / require()          // file inclusion
include_once() / require_once()
file_get_contents()            // read a file
file_put_contents()            // write a file
fopen() + fread()              // open and read
readfile()                     // output file contents
highlight_file() / show_source()// display highlighted source
unlink()                       // delete a file
rename()                       // rename a file
copy()                         // copy a file
move_uploaded_file()           // move an uploaded file
```

### Deserialization
```php
unserialize()        // deserialize an object
__wakeup()           // called during deserialization
__destruct()         // called when the object is destroyed
__toString()         // called when the object is used as a string
__call()             // triggered when calling a non-existent method
__get()              // triggered when accessing a non-existent property
```

## Step 3: Analyze Filter/Check Logic

### Regex-Filter Analysis Checklist
```php
preg_match("/pattern/flags", $input)

□ Is there an i modifier? -> no -> case bypass possible
□ Is there an m modifier? -> yes -> consider a newline bypass of ^$
□ Is there an s modifier? -> yes -> . matches newline
□ Is it checking a string or an array? -> array bypass
□ Can you exceed the backtracking limit? -> PCRE backtracking-limit bypass
```

### Common Filter Functions
```php
str_replace()        // string replace (double-write bypass possible)
str_ireplace()       // case-insensitive replace
strstr() / strpos()  // string search (case / array bypass possible)
strlen()             // length check (feature bypass possible)
in_array()           // array check (loose comparison)
is_numeric()         // numeric check (hex / scientific notation)
intval()             // integer conversion (feature bypass)
trim()               // strip whitespace (%0a%0d bypass)
htmlspecialchars()   // HTML-escape (does not escape single quotes by default)
addslashes()         // add slashes (wide-byte / GBK bypass)
mysql_real_escape_string() // escape (wide-byte / GBK bypass)
```

## Step 4: Draw the Data-Flow Diagram

```
user input -> [filter A] -> [filter B] -> dangerous function
          ↓
          Filtered?
          ↓ no
          [bypass the check] -> dangerous function executes
```

### Path-Selection Principles
1. **Prefer the least-filtered path**
2. **Prefer the path with the fewest parameters** (3-param path < 5-param path)
3. **Prefer the path with visible results** (system() over exec())
4. **Prefer simple bypasses** (case < encoding < chained)

## Step 5: Output-Visibility Analysis

### Confirm Whether Command Output Is Visible
```
1. system() output -> directly in the HTTP response
2. exec() output -> needs an extra echo
3. eval() + system() -> output is in the eval context
4. highlight_file() + system() -> output comes after the highlighted source
```

### When Unsure, Test First
```php
// first test output visibility with a simple command
system('id');
system('echo TESTFLAG123');
// search for TESTFLAG123 in the HTTP response
```

### Response-Analysis Techniques
```python
# Use python_execute to analyze the response
import requests
r = requests.get(url, params=payload)
print(f"Status: {r.status_code}")
print(f"Length: {len(r.text)}")
print(f"Headers: {dict(r.headers)}")
# Look at only the last N chars (the flag is often at the end)
print(f"Tail: {r.text[-500:]}")
# Search for the flag pattern
import re
flags = re.findall(r'(NSSCTF\{[^}]+\}|flag\{[^}]+\}|CTF\{[^}]+\})', r.text)
if flags:
    print(f"FLAG FOUND: {flags}")
```
