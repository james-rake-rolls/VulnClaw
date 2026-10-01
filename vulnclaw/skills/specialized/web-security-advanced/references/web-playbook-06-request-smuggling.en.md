# Request smuggling
English: Request Smuggling
- Entry Count: 4
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## CL-TE Request Smuggling
- ID: smuggling-cl-te
- Difficulty: advanced
- Subcategory: CL-TE
- Tags: smuggling, request, http
- Original Extracted Source: original extracted web-security-wiki source/smuggling-cl-te.md
Description:
Content-Length vs Transfer-Encoding smuggling
Prerequisites:
- The target uses multiple proxy layers
- Front-end/back-end handling differences
Execution Outline:
1. CL-TE basics
2. TE-CL basics
3. TE-TE
## CL-CL Smuggling
- ID: smuggling-cl-cl
- Difficulty: advanced
- Subcategory: CL-CL
- Tags: smuggling, cl-cl, http
- Original Extracted Source: original extracted web-security-wiki source/smuggling-cl-cl.md
Description:
Exploit differences in how the front-end proxy and back-end server handle multiple Content-Length headers to perform HTTP request smuggling
Prerequisites:
- A front-end-proxy (e.g. HAProxy/Nginx) + back-end-server architecture exists
- The two ends parse the Content-Length header differently
- Understand HTTP request-smuggling principles
Execution Outline:
1. Detect CL-CL-smuggling conditions
2. CL-CL request-smuggling PoC
3. Use CL-CL smuggling to bypass front-end access control
## TE-CL Smuggling
- ID: smuggling-te-cl
- Difficulty: expert
- Subcategory: TE-CL
- Tags: smuggling, te-cl, http
- Original Extracted Source: original extracted web-security-wiki source/smuggling-te-cl.md
Description:
Exploit the difference where the front end uses Transfer-Encoding and the back end uses Content-Length to perform HTTP request smuggling
Prerequisites:
- The front-end proxy prioritizes Transfer-Encoding
- The back-end server prioritizes Content-Length
- Understand the chunked-encoding format
Execution Outline:
1. Detect TE-CL differences
2. TE-CL smuggling PoC
3. TE-CL smuggling to hijack a request
## TE-TE Smuggling
- ID: smuggling-te-te
- Difficulty: expert
- Subcategory: TE-TE
- Tags: smuggling, te-te, http
- Original Extracted Source: original extracted web-security-wiki source/smuggling-te-te.md
Description:
Exploit differences in how the front end and back end handle various Transfer-Encoding obfuscation variants to perform request smuggling
Prerequisites:
- Both front end and back end support Transfer-Encoding
- Can obfuscate the TE header so one end ignores TE
- Understand chunked encoding and HTTP-smuggling principles
Execution Outline:
1. TE-obfuscation-variant probing
2. TE-TE smuggling exploitation (the front end ignores the obfuscated TE)
3. TE-TE cache-poisoning attack

