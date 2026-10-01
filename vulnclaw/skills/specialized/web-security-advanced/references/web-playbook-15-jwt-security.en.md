# JWT Security
English: JWT Security
- Entry Count: 4
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## JWT None-Algorithm Attack
- ID: jwt-none-attack
- Difficulty: beginner
- Subcategory: Algorithm attack
- Tags: JWT, none algorithm, authentication bypass, token forgery, CVE-2015-2951
- Original Extracted Source: original extracted web-security-wiki source/jwt-none-attack.md
Description:
Exploit a JWT library's flawed support for the "none" algorithm: change the header's signing algorithm to none and remove the signature to forge a token that passes verification without a key. This is one of the most classic JWT vulnerabilities.
Prerequisites:
- The target uses JWT for identity authentication
- jwt_tool or the Python PyJWT library
Execution Outline:
1. 1. Decode an existing JWT
2. 2. Build a None-algorithm JWT
3. 3. Automated attack with jwt_tool
4. 4. Verify the forged token
## JWT Key-Confusion Attack (RS→HS)
- ID: jwt-key-confusion
- Difficulty: advanced
- Subcategory: Algorithm attack
- Tags: JWT, key confusion, RS256, HS256, algorithm tampering
- Original Extracted Source: original extracted web-security-wiki source/jwt-key-confusion.md
Description:
When the server verifies a JWT with an RSA public key, the attacker changes the algorithm from RS256 to HS256; the server then mistakenly uses the RSA public key as the HMAC key for verification. Since the RSA public key is public, the attacker can sign any JWT with it.
Prerequisites:
- The target JWT uses an RS256/RS384/RS512 algorithm
- The RSA public key has been obtained
- jwt_tool or Python
Execution Outline:
1. 1. Obtain the RSA public key
2. 2. Key-confusion attack
3. 3. Automated attack with jwt_tool
4. 4. JWKS-endpoint injection
## JWT Key Brute-Forcing
- ID: jwt-secret-bruteforce
- Difficulty: intermediate
- Subcategory: Key cracking
- Tags: JWT, key brute-forcing, HS256, weak key, hashcat
- Original Extracted Source: original extracted web-security-wiki source/jwt-secret-bruteforce.md
Description:
When a JWT uses an HMAC symmetric algorithm (HS256/HS384/HS512) with a weak key, the signing key can be recovered by dictionary or brute-force cracking, allowing forgery of any JWT.
Prerequisites:
- The target JWT uses an HMAC algorithm (HS256, etc.)
- A valid JWT sample has been obtained
- hashcat or jwt_tool
Execution Outline:
1. 1. Confirm the algorithm and structure
2. 2. hashcat GPU-accelerated cracking
3. 3. jwt_tool dictionary cracking
4. 4. Forge a JWT with the cracked key
## JWT JKU/X5U Header Injection
- ID: jwt-jku-x5u-injection
- Difficulty: advanced
- Subcategory: Header injection
- Tags: JWT, JKU, X5U, header injection, JWKS, key hijacking
- Original Extracted Source: original extracted web-security-wiki source/jwt-jku-x5u-injection.md
Description:
Use the jku (JWK Set URL) or x5u (X.509 URL) parameter in the JWT header to point the key source at an attacker-controlled server, so the server verifies the JWT with the attacker's public key, enabling token forgery.
Prerequisites:
- The target JWT supports the jku/x5u header parameters
- The attacker has a public-facing server
- A Python environment
Execution Outline:
1. 1. Probe for JKU/X5U support
2. 2. Generate the attacker's key pair
3. 3. Host a JWKS and sign the JWT
4. 4. Verify the attack

