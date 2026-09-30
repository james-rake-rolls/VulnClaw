# AES and Block-Cipher Attacks

## Cipher-Mode Quick-Reference

| Mode | Characteristics | Exploitable weakness |
|------|------|-----------|
| ECB | Same plaintext -> same ciphertext | Pattern recognition, reordering attack |
| CBC | Previous ciphertext block feeds the current encryption | IV flip, Padding Oracle |
| CTR | Stream encryption | nonce reuse -> XOR leak |
| CFB | Stream-cipher-like | IV flip |
| OFB | Stream-cipher-like | nonce reuse |
| GCM | Authenticated encryption | nonce reuse -> keystream recovery |

## ECB Byte-Flipping

```python
from Crypto.Cipher import AES

# In ECB, identical plaintext blocks produce identical ciphertext blocks
# Attack: identify repeated ciphertext blocks -> infer plaintext structure
# Reordering ciphertext blocks changes the plaintext structure

def ecb_detect(ciphertext, block_size=16):
    """Detect ECB mode (look for repeated blocks)"""
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    return len(blocks) != len(set(blocks))
```

## CBC IV-Flip Attack

```python
"""
Principle: in CBC, P[i] = Decrypt(C[i]) XOR C[i-1]
Modifying a byte of C[i-1] -> the corresponding byte of P[i] is also flipped

Use: modifying the IV changes the first plaintext block; modifying C[i-1] changes the i-th block
Cost: the plaintext P[i-1] corresponding to C[i-1] is destroyed
"""

def cbc_iv_flip(ciphertext, known_plain, target_plain, block_size=16):
    """Flip the first CBC plaintext block (modify the IV)"""
    iv = bytearray(ciphertext[:block_size])
    for i in range(block_size):
        iv[i] = iv[i] ^ known_plain[i] ^ target_plain[i]
    return bytes(iv) + ciphertext[block_size:]
```

## Padding Oracle Attack

```python
"""
Principle: during CBC decryption, if the padding is invalid the server returns a different error
Recover the plaintext byte by byte using the error/success difference

Conditions:
1. Uses CBC mode
2. The server returns different responses for padding errors vs. ciphertext errors
3. You can repeatedly submit modified ciphertext
"""

def padding_oracle_attack(oracle, ciphertext, block_size=16):
    """Padding Oracle attack to recover plaintext
    
    oracle: a function taking ciphertext and returning True (padding OK) / False (padding bad)
    """
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    plaintext = b''
    
    for block_idx in range(1, len(blocks)):
        prev_block = bytearray(blocks[block_idx - 1])
        curr_block = blocks[block_idx]
        intermediate = bytearray(block_size)
        
        for byte_pos in range(block_size - 1, -1, -1):
            padding_val = block_size - byte_pos
            
            # Build the test ciphertext
            test_block = bytearray(block_size)
            for k in range(byte_pos + 1, block_size):
                test_block[k] = intermediate[k] ^ padding_val
            
            found = False
            for guess in range(256):
                test_block[byte_pos] = guess
                test_cipher = bytes(test_block) + curr_block
                
                if oracle(test_cipher):
                    intermediate[byte_pos] = guess ^ padding_val
                    found = True
                    break
            
            if not found:
                raise Exception(f"Padding oracle attack failed at byte {byte_pos}")
        
        # Recover the plaintext
        for i in range(block_size):
            plaintext += bytes([intermediate[i] ^ prev_block[i]])
    
    return plaintext
```

## GCM Nonce-Reuse Attack

```python
"""
When the same nonce is used for two encryptions:
- Both encryptions use the same keystream
- C1 = P1 XOR keystream
- C2 = P2 XOR keystream
- C1 XOR C2 = P1 XOR P2

If P1 is known, P2 can be recovered
"""

def gcm_nonce_reuse(c1, c2, p1):
    """Recover plaintext via GCM nonce reuse"""
    return bytes(a ^ b ^ c for a, b, c in zip(c1, c2, p1))
```

## CTR Nonce Reuse

```python
"""
In CTR mode, nonce reuse is equivalent to stream-cipher key reuse
C1 = P1 XOR keystream
C2 = P2 XOR keystream
C1 XOR C2 = P1 XOR P2
"""

def ctr_nonce_reuse(c1, c2, known_p1):
    """Recover plaintext via CTR nonce reuse"""
    return bytes(a ^ b ^ c for a, b, c in zip(c1, c2, known_p1))
```
