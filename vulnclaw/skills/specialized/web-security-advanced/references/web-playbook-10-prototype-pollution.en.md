# Prototype-chain pollution
English: Prototype Pollution
- Entry Count: 3
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Server-Side Prototype-Chain Pollution to RCE
- ID: proto-server-rce
- Difficulty: advanced
- Subcategory: Server-side exploitation
- Tags: prototype chain, Prototype Pollution, RCE, Node.js, __proto__
- Original Extracted Source: original extracted web-security-wiki source/proto-server-rce.md
Description:
Inject malicious properties by polluting the JavaScript object prototype chain (__proto__/constructor.prototype), achieving remote code execution on a Node.js server via gadget chains in child_process or template engines such as EJS/Pug.
Prerequisites:
- The target uses Node.js
- A JSON-merge / deep-copy operation exists
- Controllable JSON input
Execution Outline:
1. 1. Detect prototype-chain-pollution points
2. 2. EJS template-engine RCE gadget
3. 3. Pug template-engine RCE gadget
4. 4. Generic DoS / information-disclosure gadget
## Client-Side Prototype-Chain Pollution to XSS
- ID: proto-client-xss
- Difficulty: advanced
- Subcategory: Client-side exploitation
- Tags: prototype chain, XSS, client-side, jQuery, DOM, Prototype Pollution
- Original Extracted Source: original extracted web-security-wiki source/proto-client-xss.md
Description:
Pollute the front-end JavaScript prototype chain via a URL parameter, postMessage, or DOM operations, using gadgets in jQuery / DOM libraries to achieve client-side XSS. An attacker can lure the victim into triggering the vulnerability with a crafted URL.
Prerequisites:
- The target front end uses a vulnerable JS library
- There is logic that converts a URL parameter into an object
Execution Outline:
1. 1. Identify client-side pollution sources
2. 2. jQuery html() Gadget
3. 3. DOMPurify-bypass gadget
4. 4. Automated detection script
## Prototype-Chain Pollution Combined with NoSQL Injection
- ID: proto-nosql-injection
- Difficulty: expert
- Subcategory: Combined exploitation
- Tags: prototype chain, NoSQL, MongoDB, authentication bypass, combined attack
- Original Extracted Source: original extracted web-security-wiki source/proto-nosql-injection.md
Description:
Combine prototype-chain pollution with MongoDB/NoSQL injection. By polluting the query object's prototype-chain properties, bypass authentication logic or craft malicious query conditions, achieving authentication bypass and data leakage.
Prerequisites:
- The target uses MongoDB
- A prototype-chain-pollution point exists
- Query-construction logic exists
Execution Outline:
1. 1. Identify MongoDB query-injection points
2. 2. Prototype-chain pollution to bypass query validation
3. 3. Boolean-blind-injection data extraction
4. 4. Database enumeration and export

