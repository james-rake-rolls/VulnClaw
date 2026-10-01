# PRNG and Stream-Cipher Attacks

## MT19937 (Mersenne Twister) Attack

```python
# MT19937 state recovery (given 624 outputs)
from ctypes import *

def untemper(y):
    y ^= y >> 18
    y ^= (y << 15) & 0xefc60000
    y ^= (y << 7) & 0x9d2c5680
    y ^= (y << 14) & 0x9d2c5680
    y ^= (y << 13) & 0x9d2c5680
    y ^= (y << 11) & 0x9d2c5680
    y ^= y >> 18
    return y

def recover_mt(outputs):
    """Recover the internal state from 624 consecutive MT19937 outputs"""
    state = [untemper(y) for y in outputs[:624]]
    MT = c_ulong * 624
    mt = MT(*state)
    index = 624
    def twist():
        global index, mt
        for i in range(227):
            y = (mt[i] & 0x80000000) + (mt[(i+1)%624] & 0x7fffffff)
            mt[i] = mt[(i+397) % 624] ^ (y >> 1)
            if y & 1:
                mt[i] ^= 0x9908b0df
        index = 0
    return mt, twist, index
```

## LCG (Linear Congruential Generator) Attack

```python
"""
LCG: s_{n+1} = a * s_n + c (mod m)
When the parameters are known: iterate directly
When parameters are unknown: 3 pairs (s, s_next) suffice to solve a, c, m
"""

def lcg_attack(states):
    """Recover LCG parameters (a, c, m) from 3 consecutive states"""
    s0, s1, s2 = states[0], states[1], states[2]
    # s1 = a*s0 + c (mod m)
    # s2 = a*s1 + c (mod m)
    # s2 - s1 = a*(s1 - s0) (mod m)
    # Extended Euclid to find a, m
```

## LFSR (Linear-Feedback Shift Register) Attack

```python
"""
Berlekamp-Massey algorithm: recover the LFSR feedback polynomial from the output sequence
"""

def berlekamp_massey(s):
    """Recover the shortest LFSR feedback polynomial from a binary sequence"""
    # Sage implementation
    # F.<x> = GF(2)[]
    # s_seq = sequence(s)
    # return list(lfsr_sequence(f, [1]+[0]*15, len(s)))
```

## Known-Plaintext Attack (XOR stream cipher)

```python
"""
Stream cipher: C = P XOR keystream
If part of the plaintext P is known, recover keystream = C XOR P
the keystream can decrypt other ciphertexts
"""

def xor_attack(ciphertext, known_plaintext):
    """Known-plaintext attack on an XOR stream cipher"""
    key = bytes(a ^ b for a, b in zip(ciphertext, known_plaintext))
    return key

def xor_decrypt(key, ciphertext):
    """Decrypt with the recovered keystream"""
    return bytes(a ^ b for a, b in zip(key, ciphertext))
```

## RC4 Attack

```python
"""
Known RC4 weaknesses:
1. RC4 Drop (after dropping the first N bytes, the keystream is near-random)
2. Some key initializations are biased
"""

def rc4_drop(ciphertext, drop=3072):
    """Decrypt after dropping N bytes of RC4"""
```

## Python random-module Prediction

```python
import random

# If you can access Python's random state, you can predict future values
# The state is 624 * 4 = 2496 bytes
state = random.getstate()
# Advance the PRNG
random.setstate(state)
next_val = random.randint(0, 2**31)
```
