# RCE (Remote Code Execution)
English: RCE Remote Code Execution
- Entry Count: 12
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Command Injection
- ID: rce-command-injection
- Difficulty: intermediate
- Subcategory: Command injection
- Tags: rce, command, injection, os
- Original Extracted Source: original extracted web-security-wiki source/rce-command-injection.md
Description:
Operating-system command-injection techniques
Prerequisites:
- A system-command-execution feature exists
- User input is not filtered
Execution Outline:
1. 1. Probe for command injection
2. 2. Linux command injection
3. 3. Windows command injection
4. 4. Blind command injection
## PHP Code Execution
- ID: rce-php
- Difficulty: intermediate
- Subcategory: PHP code execution
- Tags: rce, php, code, execution
- Original Extracted Source: original extracted web-security-wiki source/rce-php.md
Description:
PHP code-execution exploitation techniques
Prerequisites:
- A PHP code-execution point exists
- User input can control code
Execution Outline:
1. 1. Common dangerous functions
2. 2. Command execution
3. 3. One-line webshell
4. 4. AV-evading one-line webshell
## PHP Filter-Chain RCE
- ID: rce-php-filter
- Difficulty: advanced
- Subcategory: PHP filter chain
- Tags: rce, php, filter, chain
- Original Extracted Source: original extracted web-security-wiki source/rce-php-filter.md
Description:
Use a PHP filter chain to construct RCE
Prerequisites:
- A file-inclusion vulnerability exists
- The PHP version supports filter chains
Execution Outline:
1. 1. Filter-chain principle
2. 2. Build the filter chain
3. 3. Generate with tools
4. 4. Full exploitation example
## Blind Command Injection
- ID: rce-cmd-blind
- Difficulty: intermediate
- Subcategory: Blind command injection
- Tags: rce, blind, command, injection
- Original Extracted Source: original extracted web-security-wiki source/rce-cmd-blind.md
Description:
Blind (no-echo) command-injection techniques
Prerequisites:
- A command-injection point exists
- No direct echo
Execution Outline:
1. 1. Time-based blind injection
2. 2. DNS out-of-band exfiltration
3. 3. HTTP out-of-band exfiltration
4. 4. ICMP out-of-band exfiltration
## Deserialization Vulnerabilities
- ID: rce-deserialize
- Difficulty: advanced
- Subcategory: Deserialization
- Tags: rce, deserialize, java, php
- Original Extracted Source: original extracted web-security-wiki source/rce-deserialize.md
Description:
Exploit a deserialization vulnerability for RCE
Prerequisites:
- A deserialization point exists
- An exploitable gadget chain exists
Execution Outline:
1. 1. Java deserialization
2. 2. PHP deserialization
3. 3. Python deserialization
4. 4. .NET deserialization
## PHP Deserialization
- ID: rce-deserialize-php
- Difficulty: advanced
- Subcategory: PHP deserialization
- Tags: rce, php, deserialize, unserialize
- Original Extracted Source: original extracted web-security-wiki source/rce-deserialize-php.md
Description:
PHP deserialization exploitation techniques
Prerequisites:
- An unserialize call exists
- An exploitable class exists
Execution Outline:
1. 1. Magic methods
2. 2. Build the POP chain
3. 3. Phar deserialization
4. 4. Session deserialization
## Java Deserialization
- ID: rce-deserialize-java
- Difficulty: advanced
- Subcategory: Java deserialization
- Tags: rce, java, deserialize, ysoserial
- Original Extracted Source: original extracted web-security-wiki source/rce-deserialize-java.md
Description:
Java deserialization exploitation techniques
Prerequisites:
- A Java deserialization point exists
- A gadget chain exists
Execution Outline:
1. 1. Common gadget chains
2. 2. Use ysoserial
3. 3. JRMP attack
4. 4. In-memory-webshell injection
## File-Upload Vulnerabilities
- ID: rce-file-upload
- Difficulty: intermediate
- Subcategory: File upload
- Tags: rce, upload, webshell, file
- Original Extracted Source: original extracted web-security-wiki source/rce-file-upload.md
Description:
Exploit a file-upload vulnerability to obtain RCE
Prerequisites:
- A file-upload feature exists
- Can upload an executable file
Execution Outline:
1. 1. Basic upload
2. 2. Front-end bypass
3. 3. Back-end bypass
4. 4. Image-embedded webshell
## File-Inclusion RCE
- ID: rce-include
- Difficulty: intermediate
- Subcategory: File inclusion
- Tags: rce, include, lfi, rfi
- Original Extracted Source: original extracted web-security-wiki source/rce-include.md
Description:
Exploit a file-inclusion vulnerability for RCE
Prerequisites:
- A file-inclusion vulnerability exists
- Can include a malicious file
Execution Outline:
1. 1. Log poisoning
2. 2. Session file inclusion
3. 3. /proc/self/environ
4. 4. PHP pseudo-protocol
## Log-Poisoning RCE
- ID: rce-log-poison
- Difficulty: intermediate
- Subcategory: Log poisoning
- Tags: rce, log, poison, lfi
- Original Extracted Source: original extracted web-security-wiki source/rce-log-poison.md
Description:
Use log poisoning to achieve RCE
Prerequisites:
- A file-inclusion vulnerability exists
- Can read the log file
Execution Outline:
1. 1. Apache log poisoning
2. 2. Nginx log poisoning
## Image-Embedded Webshell RCE
- ID: rce-image
- Difficulty: intermediate
- Subcategory: Image-embedded webshell
- Tags: rce, image, webshell, upload
- Original Extracted Source: original extracted web-security-wiki source/rce-image.md
Description:
Use an image-embedded webshell for RCE
Prerequisites:
- A file upload exists
- A file inclusion exists
Execution Outline:
1. 1. Craft an image-embedded webshell
2. 2. Image-embedded-webshell content
3. 3. Execute via file inclusion
4. 4. Combine with .htaccess
## .htaccess Abuse
- ID: rce-htaccess
- Difficulty: intermediate
- Subcategory: .htaccess
- Tags: rce, htaccess, apache, upload
- Original Extracted Source: original extracted web-security-wiki source/rce-htaccess.md
Description:
Achieve RCE via an .htaccess file
Prerequisites:
- An Apache server
- Can upload .htaccess
Execution Outline:
1. 1. Parse other extensions
2. 2. Auto-inclusion
3. 3. Pseudo-static RCE
4. 4. Error-page inclusion

