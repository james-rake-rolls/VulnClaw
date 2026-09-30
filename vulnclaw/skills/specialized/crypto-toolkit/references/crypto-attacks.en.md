# Cryptographic-Attack Techniques

## 1. Hash Attacks

### Rainbow-Table Lookup
- crackstation.net — free, supports MD5/SHA1/SHA256
- cmd5.com — Chinese, wide coverage
- hashes.org — community-maintained

### Hash Length-Extension Attack
- Applies to: MD5, SHA1, SHA256 and other Merkle-Damgard hashes
- Condition: you know `H(message)` and `len(message)` but not the message itself
- Tools: hashpump, hash_extender
- Scenario: API signature-verification bypass

### Hash Collision
- MD5：fastcoll, HashClash
- SHA1: SHAttered (theoretically feasible)
- Scenario: file-integrity bypass, certificate forgery

## 2. Symmetric-Encryption Attacks

### ECB-Mode Attack
- Same plaintext block -> same ciphertext block
- Can reorder the plaintext by reordering ciphertext blocks
- Can identify repeated patterns (e.g. a user-role field)

### CBC Byte-Flipping Attack
- Modifying the IV or previous ciphertext block flips the corresponding byte of the next plaintext block
- Formula: `P[i] = D(C[i]) XOR C[i-1]`
- Modifying `C[i-1][j]` -> flips `P[i][j]`
- Scenario: modify an encrypted user ID or role field

### Padding Oracle Attack
- Condition: the server reveals whether the padding is correct
- Recover the plaintext byte by byte, no key needed
- Tools: padbuster, padding-oracle-attacker
- Scenario: ASP.NET / Java serialized tokens

### IV-Reuse Attack
- In CBC, same IV + same key -> information leakage
- Can infer whether plaintexts are the same

## 3. RSA Attacks

### Small-Public-Exponent Attack
- When e=3, if m^3 < n, recover directly with a cube root
- Low-exponent broadcast attack: same plaintext encrypted with the same e under different n

### Common-Modulus Attack
- Same plaintext encrypted with the same n and different e
- Recover the plaintext via the extended Euclidean algorithm

### Wiener Attack
- n can be factored when d < n^0.25
- Applies when the private exponent is small

### Fermat Factorization
- n can be factored quickly when p and q are close
- Applies to weak key generation

### Known Key File
- Extract parameters from a .pem/.der file
- openssl rsa -text -noout -in key.pem

## 4. Classical-Cipher Attacks

### Caesar Brute Force
- Only 25 possibilities; iterate directly
- Use letter-frequency analysis to pick the most likely result

### Vigenere Analysis
- Kasiski test to determine the key length
- Use the index of coincidence to verify the key length
- After determining the length, Caesar-crack each column

### Rail-Fence Cipher
- Common rail counts: 2-8
- Try every possible rail count
- Check whether the result is meaningful

### Bacon Cipher
- Two fonts/styles -> A/B encoding
- Decode one letter per 5 characters

## 5. JWT Attacks

### none-Algorithm Bypass
```json
{"alg": "none", "typ": "JWT"}
```
- Change the algorithm to none
- Remove the signature part
- Some implementations accept an unsigned token

### RS256 -> HS256 Algorithm Confusion
- Change the algorithm from RS256 to HS256
- Sign using the public key as the HMAC secret
- If the server verifies an HS256 signature with the public key -> bypass

### Weak-Key Brute Force
- jwt-tool, jwt-cracker
- Common weak keys: secret, password, 123456, etc.

### JWK / jku Injection
- Embed a public key in the header (jwk field)
- Or point to an attacker-controlled jku URL
- If the server trusts the key in the header -> forge

## 6. Encoding-Chain Attack Patterns

### WAF-Bypass Encoding
- Double URL encoding: `%2527` -> `%27` -> `'`
- Unicode normalization: `％27` -> `'` (full-width to half-width)
- HTML entity: `&#39;` -> `'`
- Base64-encoded injection parameters

### Encoding in Deserialization
- PHP: base64-encoded serialized object
- Java: base64-encoded serialized byte stream
- Python: base64 pickle payloads

## 7. Tool Quick-Reference

| Scenario | Tool |
|------|------|
| General encode/decode | CyberChef |
| Hash cracking | hashcat, john |
| RSA analysis | RsaCtfTool |
| JWT analysis | jwt-tool |
| Padding Oracle | padbuster |
| Hash extension | hashpump |
| Online decoding | base64decode.org, cyberchef.org |
