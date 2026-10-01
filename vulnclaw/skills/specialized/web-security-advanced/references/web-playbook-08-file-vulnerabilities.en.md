# File Vulnerabilities
English: File Vulnerabilities
- Entry Count: 7
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## File-Upload Bypass
- ID: file-upload-bypass
- Difficulty: intermediate
- Subcategory: File upload
- Tags: upload, bypass, webshell
- Original Extracted Source: original extracted web-security-wiki source/file-upload-bypass.md
Description:
File-upload-restriction bypass techniques
Prerequisites:
- The target has a file-upload feature
- Upload restrictions exist
Execution Outline:
1. Extension bypass
2. Content-Type
3. Image-embedded webshell
4. Space bypass
## Arbitrary File Download
- ID: file-download
- Difficulty: beginner
- Subcategory: Download
- Tags: file-download, lfi, leak
- Original Extracted Source: original extracted web-security-wiki source/file-download.md
Description:
Exploit a path-control flaw in a file-download feature to download arbitrary sensitive files from the server
Prerequisites:
- The target has a file-download feature
- The file-path parameter is attacker-controlled
- The server does not strictly filter the path
Execution Outline:
1. Identify file-download endpoints
2. Path traversal to download sensitive files
3. Download the source and database config
4. Automated bulk sensitive-file probing
## Race Condition
- ID: file-competition
- Difficulty: advanced
- Subcategory: Race Condition
- Tags: race-condition, file-upload
- Original Extracted Source: original extracted web-security-wiki source/file-competition.md
Description:
Exploit a race condition during file upload/processing to perform malicious operations in the time window between the security check and the file's use
Prerequisites:
- The target has a file-upload feature
- The server uploads first and checks afterward
- Can access the uploaded file with high concurrency
- Know the temp-file storage path
Execution Outline:
1. Identify the race-condition window
2. Race-condition exploitation - concurrent upload and access
3. Python concurrent race-condition exploit script
4. .htaccess race-condition write
## Path Traversal
- ID: file-traversal
- Difficulty: beginner
- Subcategory: Traversal
- Tags: traversal, file
- Original Extracted Source: original extracted web-security-wiki source/file-traversal.md
Description:
Use path-traversal (../) sequences to break out of the file-access directory restriction and read or write arbitrary files outside the web root
Prerequisites:
- The target has a file-read/inclusion feature
- The file-path parameter is attacker-controlled
- The server's path filtering is not strict
Execution Outline:
1. Basic path-traversal test
2. Encoding bypass of path filtering
3. Windows-specific path traversal
4. LFI-to-RCE escalation
## Zip Slip
- ID: file-zip-slip
- Difficulty: intermediate
- Subcategory: Zip
- Tags: zip-slip, file, rce
- Original Extracted Source: original extracted web-security-wiki source/file-zip-slip.md
Description:
Use path traversal in a maliciously crafted archive (ZIP/TAR) to write arbitrary files, overwriting critical server files or writing a webshell
Prerequisites:
- The target has a ZIP/TAR upload feature that auto-extracts
- The extraction library does not filter path traversal in file names
- Know the path of the web root or other key directories
Execution Outline:
1. Probe the ZIP-upload and extraction feature
2. Build a Zip Slip malicious archive
3. Upload and verify Zip Slip
4. TAR Zip Slip variant
## MIME-Type Bypass
- ID: file-mime
- Difficulty: beginner
- Subcategory: MIME
- Tags: mime, bypass
- Original Extracted Source: original extracted web-security-wiki source/file-mime.md
Description:
Bypass the file-upload type check by forging the MIME type (Content-Type) to upload a malicious executable file
Prerequisites:
- The target has a file-upload feature
- The server determines file type only by Content-Type
- Know the MIME types the target allows
Execution Outline:
1. Probe the file-type-checking mechanism
2. Upload a webshell by forging the MIME type
3. Magic-bytes forgery
4. Verify the upload result
## Null-Byte Truncation
- ID: file-null-byte
- Difficulty: intermediate
- Subcategory: Null Byte
- Tags: null-byte, bypass
- Original Extracted Source: original extracted web-security-wiki source/file-null-byte.md
Description:
Use a null byte (%00/\x00) to truncate the filename's extension check and bypass the file-upload whitelist
Prerequisites:
- The target uses a whitelist to validate file extensions
- The back-end language or library is affected by null-byte truncation (PHP<5.3.4, old Java versions)
- The server has a truncation point in path concatenation
Execution Outline:
1. Null-byte-truncation principle and environment detection
2. File-upload null-byte truncation
3. File-inclusion null-byte truncation
4. Modern alternative (PHP>=5.3.4)

