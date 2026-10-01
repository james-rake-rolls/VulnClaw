# LFI/RFI File Inclusion
English: LFI/RFI File Inclusion
- Entry Count: 12
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Local File Inclusion
- ID: lfi-basic
- Difficulty: intermediate
- Subcategory: Local inclusion
- Tags: lfi, local, file, inclusion
- Original Extracted Source: original extracted web-security-wiki source/lfi-basic.md
Description:
Local file-inclusion exploitation techniques
Prerequisites:
- A file-inclusion feature exists
- The user can control the inclusion path
Execution Outline:
1. 1. Probe for LFI
2. 2. Read sensitive files
3. 3. PHP pseudo-protocol
4. 4. Log poisoning
## Remote File Inclusion
- ID: rfi-basic
- Difficulty: intermediate
- Subcategory: Remote inclusion
- Tags: rfi, remote, file, inclusion
- Original Extracted Source: original extracted web-security-wiki source/rfi-basic.md
Description:
Remote file-inclusion exploitation techniques
Prerequisites:
- A file-inclusion feature exists
- allow_url_include=On
- The user can control the inclusion path
Execution Outline:
1. 1. Probe for RFI
2. 2. Host a malicious file
3. 3. Reverse shell
4. 4. Use the data protocol
## Log-Poisoning LFI
- ID: lfi-log-poison
- Difficulty: intermediate
- Subcategory: Log poisoning
- Tags: lfi, log, poison, rce
- Original Extracted Source: original extracted web-security-wiki source/lfi-log-poison.md
Description:
Use log poisoning to escalate LFI to RCE
Prerequisites:
- An LFI vulnerability exists
- Can include a log file
- The log file is writable
Execution Outline:
1. 1. Probe for the log-file location
2. 2. Poison the User-Agent
3. 3. Poison the request path
4. 4. Execute a command
## PHP Pseudo-Protocol Abuse
- ID: lfi-wrapper
- Difficulty: intermediate
- Subcategory: Pseudo-protocol
- Tags: lfi, wrapper, php, protocol
- Original Extracted Source: original extracted web-security-wiki source/lfi-wrapper.md
Description:
Use PHP pseudo-protocols for an LFI attack
Prerequisites:
- An LFI vulnerability exists
- A PHP environment
- Pseudo-protocols are not disabled
Execution Outline:
1. 1. php://filter
2. 2. php://input
3. 3. data:// protocol
4. 4. phar:// protocol
## Directory-Traversal Techniques
- ID: lfi-traversal
- Difficulty: beginner
- Subcategory: Directory traversal
- Tags: lfi, traversal, bypass, path
- Original Extracted Source: original extracted web-security-wiki source/lfi-traversal.md
Description:
LFI directory-traversal bypass techniques
Prerequisites:
- An LFI vulnerability exists
- Path filtering is present
Execution Outline:
1. 1. Basic traversal
2. 2. Bypass ../ stripping
3. 3. URL-encoding bypass
4. 4. Unicode-encoding bypass
## PHP Filter-Chain Attack
- ID: lfi-php-filter
- Difficulty: intermediate
- Subcategory: PHP Filter
- Tags: lfi, php, filter, chain
- Original Extracted Source: original extracted web-security-wiki source/lfi-php-filter.md
Description:
Use a PHP filter chain for an LFI attack
Prerequisites:
- An LFI vulnerability exists
- A PHP environment
- The filter pseudo-protocol is available
Execution Outline:
1. 1. Read the source code
2. 2. Multiple filters
3. 3. Filter-chain RCE
4. 4. Read config files
## PHP Input Execution
- ID: lfi-php-input
- Difficulty: intermediate
- Subcategory: PHP Input
- Tags: lfi, php, input, rce
- Original Extracted Source: original extracted web-security-wiki source/lfi-php-input.md
Description:
Use php://input to execute PHP code
Prerequisites:
- An LFI vulnerability exists
- allow_url_include=On
- The POST method is available
Execution Outline:
1. 1. Basic execution
2. 2. Command execution
3. 3. File operations
4. 4. Reverse shell
## PHP Data Protocol Attack
- ID: lfi-php-data
- Difficulty: intermediate
- Subcategory: PHP Data
- Tags: lfi, php, data, protocol
- Original Extracted Source: original extracted web-security-wiki source/lfi-php-data.md
Description:
Use the data:// protocol to execute PHP code
Prerequisites:
- An LFI vulnerability exists
- allow_url_include=On
- The data protocol is available
Execution Outline:
1. 1. Basic execution
2. 2. Base64 encoding
3. 3. Command execution
4. 4. Reverse shell
## PHP Zip Protocol Attack
- ID: lfi-php-zip
- Difficulty: intermediate
- Subcategory: PHP Zip
- Tags: lfi, php, zip, archive
- Original Extracted Source: original extracted web-security-wiki source/lfi-php-zip.md
Description:
Use the zip:// protocol for an LFI attack
Prerequisites:
- An LFI vulnerability exists
- Can upload a zip file
- The zip protocol is available
Execution Outline:
1. 1. Create a malicious Zip
2. 2. Upload a Zip file
3. 3. Include the Zip file
4. 4. Image-embedded webshell
## Phar Deserialization Attack
- ID: lfi-phar
- Difficulty: advanced
- Subcategory: Phar deserialization
- Tags: lfi, phar, deserialization, rce
- Original Extracted Source: original extracted web-security-wiki source/lfi-phar.md
Description:
Use Phar deserialization for RCE
Prerequisites:
- An LFI vulnerability exists
- A PHP environment
- The phar extension is available
Execution Outline:
1. 1. Create a Phar file
2. 2. Trigger deserialization
3. 3. Image-embedded-webshell Phar
4. 4. Common gadget chains
## Session File Inclusion
- ID: lfi-session
- Difficulty: intermediate
- Subcategory: Session inclusion
- Tags: lfi, session, file, inclusion
- Original Extracted Source: original extracted web-security-wiki source/lfi-session.md
Description:
Use the session file for an LFI attack
Prerequisites:
- An LFI vulnerability exists
- Can control the session content
- Know the session path
Execution Outline:
1. 1. Probe for the session path
2. 2. Control the session content
3. 3. Include the session file
4. 4. Session race condition
## Proc Filesystem Abuse
- ID: lfi-proc
- Difficulty: intermediate
- Subcategory: Proc filesystem
- Tags: lfi, proc, linux, environ
- Original Extracted Source: original extracted web-security-wiki source/lfi-proc.md
Description:
Use the /proc filesystem for an LFI attack
Prerequisites:
- An LFI vulnerability exists
- A Linux system
- /proc is accessible
Execution Outline:
1. 1. Read process information
2. 2. Read environment variables
3. 3. Read logs via fd
4. 4. Read other processes

