---
name: crypto-toolkit
description: Encoding/decoding and encryption/decryption tools — base64/URL/Hex/HTML-entity encode-decode, MD5/SHA hashing, AES/DES/RSA encrypt-decrypt, JWT parsing, Caesar/ROT13 ciphers, rail-fence/Vigenere ciphers, Unicode escaping, Morse code, and more
---

# Encoding/Decoding and Encryption/Decryption Skill

Provides comprehensive encode/decode and encrypt/decrypt capabilities for the encoding, encryption, and obfuscation scenarios common in penetration testing.
**Important**: whenever you encounter an encoded/encrypted string, use the `crypto_decode` tool to decode it rather than guessing by intuition.

## Core principles

1. **Tool first** — for base64, hex, URL-encoded, and similar strings, call the `crypto_decode` tool to decode; do not guess in your head
2. **Try multiple formats** — if one decoding produces an implausible result, try other encoding formats
3. **Chained decoding** — CTFs often use multi-layer encoding (e.g. base64→hex→ROT13); after decoding, check whether the result needs decoding again
4. **Validate the result** — after decoding, check whether the result is plausible (readable text? looks like a path/URL/flag?)

## 1. Encoding identification and decoding

### Recognizing common encodings

| Encoding | Characteristics | Example |
|---------|------|------|
| Base64 | `A-Za-z0-9+/=`, often ends with `=` padding | `TnNTY1RmLnBocA==` |
| Base32 | `A-Z2-7=` | `OBZHK5DFN2A====` |
| Hex | `0-9a-f`, even length | `4e73536354662e706870` |
| URL encoding | `%XX` format | `%2F%61%64%6D%69%6E` |
| HTML entities | `&#xNN;` or `&#NNN;` | `&#x3C;script&#x3E;` |
| Unicode escape | `\uXXXX` or `\UXXXXXXXX` | `<sc` |
| JWT | three `.`-separated base64 segments | `eyJhbG...` |

### Decoding strategy

1. Identify the encoding → call the `crypto_decode` tool with the matching operation
2. Check whether the decoded result is readable/plausible
3. If implausible, try other encoding formats
4. If the result still looks encoded, repeat steps 1-3

## 2. Hashes and digests

### Common hash types

| Type | Output length | Characteristics |
|------|---------|------|
| MD5 | 32 hex | `e10adc3949ba59abbe56e057f20f883e` |
| SHA1 | 40 hex | `aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d` |
| SHA256 | 64 hex | `2c26b46b68ffc68ff99b453c1d30413413422d7064...` |
| SHA512 | 128 hex | a longer hex string |
| NTLM | 32 hex | Windows hash |
| MySQL5 | 41 chars | `*E6CC90B878B948C35E92B003C792C46758BF4` |

### Hash-handling strategy

- Identify the hash type (by length and character set)
- Try online rainbow-table lookups (via the fetch tool, e.g. crackstation)
- For hashes with a known salt, try salted brute force

## 3. Symmetric encryption

### AES/DES/3DES

- Needs a key and a mode (ECB/CBC/CTR, etc.)
- CBC mode needs an IV
- Common padding: PKCS7 / ZeroPadding
- Hardcoded keys are common in pentests; prefer extracting them from the source

## 4. Asymmetric encryption

### RSA

- Extract parameters from public/private-key files
- RSA with a too-small modulus can be factored
- A known private key decrypts directly

## 5. Classical ciphers

| Type | Characteristics | Cracking method |
|------|------|---------|
| Caesar/ROT13 | Letter shift | Brute-force 25 shifts |
| Vigenere | Polyalphabetic substitution | Kasiski / frequency analysis |
| Rail-fence | Character regrouping | Try common rail counts |
| Bacon | AB quintuples | Table lookup |
| Morse | `.-` dots and dashes | Table lookup |

## 6. JWT handling

- Decode Header + Payload (base64url)
- Check the algorithm: `none`-algorithm bypass, RS256→HS256 algorithm confusion
- Try weak-key signature forgery
- Check time claims such as exp/nbf

## Tool usage

### The `crypto_decode` tool

Call this tool whenever you need to encode / decode / encrypt / decrypt:

```
crypto_decode(operation="base64_decode", input="TnNTY1RmLnBocA==")
```

Supported operations:
- **Encode**: `base64_encode`, `base32_encode`, `hex_encode`, `url_encode`, `html_encode`, `unicode_encode`, `rot13_encode`, `morse_encode`, `caesar_encode`, `base58_encode`
- **Decode**: `base64_decode`, `base32_decode`, `hex_decode`, `url_decode`, `html_decode`, `unicode_decode`, `rot13_decode`, `morse_decode`, `caesar_decode`, `base58_decode`
- **Hash**: `md5_hash`, `sha1_hash`, `sha256_hash`, `sha512_hash`
- **Encrypt/decrypt**: `aes_encrypt`, `aes_decrypt`, `des_encrypt`, `des_decrypt`, `rsa_encrypt`, `rsa_decrypt`
- **JWT**: `jwt_decode`, `jwt_encode`
- **Auto-detect**: `auto_decode` (auto-identifies the encoding type and decodes)

## CTF cryptography-attack routing

> When you encounter a cryptographic-attack scenario (the algorithm is known and you need to recover plaintext or the key), prefer the `ctf-crypto` skill:

| Attack scenario | Route to ctf-crypto | Reference |
|---------|-----------------|---------|
| RSA small exponent / common modulus / Wiener | `ctf-crypto` | `references/rsa-attacks-cheatsheet.md` |
| AES Padding Oracle / ECB flipping | `ctf-crypto` | `references/aes-and-block-cipher-attacks.md` |
| ECC small subgroup / discrete log | `ctf-crypto` | `references/ecc-attacks-cheatsheet.md` |
| PRNG / MT19937 prediction | `ctf-crypto` | `references/prng-and-stream-cipher-attacks.md` |
| Classical ciphers (Vigenere/XOR) | `ctf-crypto` | `references/classic-cipher-attacks.md` |
| Lattice attacks / LWE | `ctf-crypto` | `references/lattice-and-lwe-attacks.md` |

**This skill focuses on encode/decode operation tools**; for concrete cryptographic-attack methods and parameters, see `ctf-crypto`.

## References

- `references/encoding-cheatsheet.md` — encoding-identification quick-reference
- `references/crypto-attacks.md` — cryptographic-attack techniques
- `references/crypto-attacks-roadmap.md` — cryptographic-attack routing (choose the attack method by challenge characteristics)
