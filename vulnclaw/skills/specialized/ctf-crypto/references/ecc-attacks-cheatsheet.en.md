# ECC Attack Cheatsheet

## Elliptic-Curve Basics

```python
# Elliptic curve: y^2 = x^3 + ax + b (mod p)
# Point operations: P + Q, k*P
# ECDLP: given P, Q=k*P, find k
```

## Attack Selection

| Condition | Attack method | Applicable scenario |
|------|---------|---------|
| Order n is smooth | Pohlig-Hellman | All factors of n are small |
| Anomalous curve (p=n) | Smart attack | Anomalous curve |
| Small subgroup order | Small-subgroup attack | Order has a large prime factor |
| Suspicious curve parameters | Invalid-curve attack | Non-standard curve |
| ECDSA nonce reuse | Deterministic attack | Same k used for two signatures |
| Small order | Brute force / Baby-step Giant-step | n < 2^40 |

## Pohlig-Hellman Attack

```python
# Sage implementation
# When all factors of the group order n are small

P = EllipticCurve(GF(p), [a, b])
G = P(P_x, P_y)  # base point
Q = P(Q_x, Q_y)  # target point

n = P.order()  # group order
factors = factor(n)

# Pohlig-Hellman
k = discrete_log(Q, G, operation='+')
# Or specify a method
k = Q.discrete_log(G)
```

## Smart Attack (anomalous curve)

```python
# When the curve order equals the characteristic p (anomalous curve)
# E.lift_x() may fail, but p-adic lifting can be used

# Sage implementation
def smart_attack(P, Q, p, a, b):
    """Smart attack, for anomalous curves where #E = p"""
    E = EllipticCurve(Qp(p), [a, b])
    P_lift = E.lift_x(ZZ(P.xy()[0]))
    Q_lift = E.lift_x(ZZ(Q.xy()[0]))
    
    pP = p * P_lift
    pQ = p * Q_lift
    
    x1 = pP.xy()[0] / pP.xy()[1]
    x2 = pQ.xy()[0] / pQ.xy()[1]
    
    k = ZZ(x2) / ZZ(x1) % p
    return k
```

## Invalid-Curve Attack

```python
# When the server does not verify the point is on the curve
# You can send a point not on the curve; it may lie on another curve
# If that curve's order is smooth, Pohlig-Hellman can be used

# Construction: choose a' so that y^2 = x^3 + a'*x + b has smooth order
```

## ECDSA Nonce-Reuse Attack

```python
"""
If the same nonce k is used for two ECDSA signatures:
s1 = k^(-1) * (h1 + r*d) mod n
s2 = k^(-1) * (h2 + r*d) mod n

s1 - s2 = k^(-1) * (h1 - h2) mod n
k = (h1 - h2) * (s1 - s2)^(-1) mod n
d = (s1 * k - h1) * r^(-1) mod n  (private key)
"""

def ecdsa_nonce_reuse(r1, s1, h1, r2, s2, h2, n):
    """Recover the private key from ECDSA nonce reuse"""
    from gmpy2 import invert
    # Confirm r is the same
    assert r1 == r2
    k = ((h1 - h2) * invert(s1 - s2, n)) % n
    d = ((s1 * k - h1) * invert(r1, n)) % n
    return int(d)
```

## Common ECC CTF Challenge Types

| Challenge type | Characteristics | Attack |
|------|------|------|
| Standard curve + small order | n < 2^40 | Brute force |
| Standard curve + smooth order | n has small factors | Pohlig-Hellman |
| Anomalous curve | #E = p | Smart attack |
| Custom curve | Suspicious a, b | Invalid curve / factor the order |
| ECDSA signatures | Multiple signatures | Nonce reuse |
| Twisted Edwards | x^2 + a*y^2 = 1 + d*x^2*y^2 | Convert to Weierstrass |
