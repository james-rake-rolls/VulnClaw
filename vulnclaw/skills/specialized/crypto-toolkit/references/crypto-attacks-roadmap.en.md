# Cryptographic-Attack Classification Routing

From the information the challenge gives, quickly decide which attack method to use.

## Decision Tree

```
Known information
├── Know plaintext + ciphertext?
│   ├── Same key used multiple times? -> XOR / stream-cipher analysis
│   └── Single encryption? -> analyze the cipher mode
├── Know ciphertext + key?
│   ├── Symmetric encryption -> decrypt directly
│   └── Asymmetric encryption -> RSA/ECC attack
├── Known n, e, c (RSA)?
│   ├── small e -> small-exponent attack
│   ├── Multiple sharing n -> common-modulus attack
│   ├── small d -> Wiener attack
│   ├── p-1 smooth -> Pollard p-1
│   └── Try online factorization (factordb)
├── Elliptic-curve parameters?
│   ├── Smooth order -> Pohlig-Hellman
│   ├── Anomalous curve -> Smart attack
│   └── ECDSA nonce reuse -> private-key recovery
├── Known PRNG output sequence?
│   ├── MT19937 -> state recovery
│   ├── LCG -> parameter recovery
│   └── LFSR → Berlekamp-Massey
└── Classical cipher?
    ├── Caesar/ROT13 -> brute force
    ├── Vigenere -> Kasiski + frequency
    └── One-Time Pad reuse -> statistical attack
```

## RSA Attack Quick-Selection

| Known | Attack |
|------|------|
| n, e, c, e=3 | Small-exponent root |
| Multiple (n, c), same e, same plaintext | Hastad broadcast |
| Multiple (n, c), same n, different e | Common-modulus attack |
| n, e, d very small | Wiener attack |
| n factorable, p~q | Fermat factorization |
| n factorable, p-1 smooth | Pollard p-1 |
| Partial plaintext known | Coppersmith |
| Found in factordb | Online factorization |

## AES / Block-Cipher Attack Quick-Selection

| Scenario | Attack |
|------|------|
| ECB mode | Pattern analysis + block reordering |
| CBC mode, controllable IV | IV-flip attack |
| CBC mode, Padding Oracle | Padding Oracle attack |
| CTR/GCM, nonce reuse | Keystream recovery |
| Partial plaintext known | XOR to recover the keystream |

## PRNG Attack Quick-Selection

| Scenario | Attack |
|------|------|
| Python random(), 624 outputs | MT19937 state recovery |
| 3 consecutive LCG outputs | Parameter recovery |
| LFSR output sequence | Berlekamp-Massey |
| RC4 (after dropping the first 3072 bytes) | RC4 Drop attack |

## Classical-Cipher Quick-Selection

| Ciphertext trait | Attack |
|---------|------|
| Single-character substitution | Frequency analysis |
| Multi-character shift | Caesar brute force |
| Polyalphabetic substitution | Vigenere Kasiski |
| Binary multi-byte XOR | Frequency analysis + key-length estimation |
| One-time-pad reuse | XOR-comparison attack |
