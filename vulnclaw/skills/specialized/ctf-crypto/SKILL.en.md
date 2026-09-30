---
name: ctf-crypto
description: CTF cryptography-attack knowledge base — RSA attacks (small exponent/common modulus/Wiener/Coppersmith), AES attacks (Padding Oracle/ECB byte-flipping/GCM nonce reuse), ECC attacks, LFSR/LCG/PRNG attacks, classical ciphers, LWE lattice attacks
routing:
  target_types: [ctf, crypto]
  task_types: [ctf, crypto]
---

# CTF Cryptography-Attack Knowledge Base

A practical attack knowledge base for CTF Crypto challenges, providing **concrete attack parameters, mathematical formulas, and Python code snippets**.

**Difference from `crypto-toolkit`**:
- `crypto-toolkit` → encode/decode operation tools (base64 decoding, MD5 hashing, AES encrypt/decrypt)
- `ctf-crypto` → cryptographic-attack knowledge (how to do an RSA small-exponent attack, how to exploit a Padding Oracle)

## Core principles

1. **Identify the cryptosystem first** — look at key length, cipher mode, and known quantities to determine the attack direction
2. **Verify with tools** — use `python_execute` to run attack code, and `crypto_decode` for auxiliary encode/decode
3. **Parameter-sensitive** — cryptographic attacks are extremely parameter-sensitive; compute precisely

## Scenario routing

| Scenario | Reference | Core attacks |
|------|---------|---------|
| RSA attacks | `rsa-attacks-cheatsheet.md` | small-e / common-modulus / Wiener / Pollard / Fermat / Coppersmith |
| AES / block-cipher attacks | `aes-and-block-cipher-attacks.md` | ECB flip / Padding Oracle / GCM nonce reuse |
| ECC attacks | `ecc-attacks-cheatsheet.md` | small subgroup / invalid curve / Smart / Pohlig-Hellman |
| PRNG / stream-cipher attacks | `prng-and-stream-cipher-attacks.md` | MT19937 / LCG / LFSR / RC4 |
| Classical ciphers | `classic-cipher-attacks.md` | Vigenere / XOR frequency analysis / OTP reuse |
| Lattice attacks | `lattice-and-lwe-attacks.md` | LLL / BKZ / HNP / LWE embedding |

## Quick triage guide

| Challenge characteristic | Likely attack | Recommended reference |
|---------|---------|---------|
| Given n, e, c | RSA | rsa-attacks-cheatsheet.md |
| e=3 or e very small | RSA small-exponent attack | rsa-attacks-cheatsheet.md |
| Multiple (n, e, c) with the same n | RSA common-modulus attack | rsa-attacks-cheatsheet.md |
| n very large but e very large | Wiener attack | rsa-attacks-cheatsheet.md |
| AES-CBC + decryption oracle | Padding Oracle | aes-and-block-cipher-attacks.md |
| AES-ECB + controllable plaintext | ECB byte-flipping | aes-and-block-cipher-attacks.md |
| Elliptic-curve parameters | ECC attacks | ecc-attacks-cheatsheet.md |
| Given a random-number sequence | PRNG prediction | prng-and-stream-cipher-attacks.md |
| Given ciphertext and partial plaintext | XOR / stream cipher | classic-cipher-attacks.md |
| Matrix / vector operations | Lattice attacks | lattice-and-lwe-attacks.md |
