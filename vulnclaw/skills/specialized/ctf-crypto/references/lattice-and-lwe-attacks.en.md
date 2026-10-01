# Lattice Attacks and LWE

## Basic Concepts

```
Lattice: a discrete additive subgroup of Z^n
Basis: a set of linearly independent vectors generating the lattice
LLL algorithm: approximate the shortest lattice vector (approximate SVP)
CVP (Closest Vector Problem): find the nearest vector
SVP (Shortest Vector Problem): find the shortest vector
```

## LLL Algorithm

```python
# SageMath implementation
"""
A = matrix(ZZ, [[...], [...], ...])  # lattice-basis matrix
B = A.LLL()  # LLL-reduced basis
# The columns of B are near-shortest lattice vectors
```

## Hidden Number Problem (HNP)

```python
"""
Given: (d_i, (t_i * a + k_i * d_i) mod p), partial bits
Recover: a (private key)
Use Coppersmith to solve for k_i
"""
# SageMath
def hnp_attack(d, t, bits, p):
    F.<x> = PolynomialRing(Zmod(p))
    # Build the polynomial...
```

## Coppersmith-Related

```python
"""
Coppersmith to find small polynomial roots:
f(x) = 0 mod n, |x| < n^(1/d)
where d is the polynomial degree
"""

# SageMath
def coppersmith_small_root(f, n, d, m):
    """f(x) = 0 mod n, find small roots x, |x| < n^(1/(d*omega))"""
    # Build the lattice and run LLL
```

## LWE (Learning With Errors)

```python
"""
The LWE problem:
Given: (A, b = As + e) mod q
Recover: s (private key)
where e is the small error vector

Common attacks:
1. Enumerate the small error (when e is small)
2. BKW algorithm
3. Reduce to SVP/CVP
"""
```

## HNP Attack Template

```python
# SageMath: recover the RSA private key from a partial private key
"""
DCP (Diffie-Hellman Claw Problem) variant
Solve via lattice reduction
"""

# Basic template
"""
F = GF(p)
P.<x> = PolynomialRing(F)

# Build the lattice-basis matrix
# Apply LLL
# Extract the private key from the reduced basis
"""
```

## General Lattice-Attack Template

```python
# Consider a lattice attack in the following scenarios:
# 1. Several equations with unknowns and "small errors"
# 2. Partial private-key / partial-plaintext recovery
# 3. Reduce to the closest-vector problem in a lattice

# Steps:
# 1. Model the problem as a CVP/SVP in a lattice
# 2. Build the lattice-basis matrix
# 3. Reduce with LLL/BKZ
# 4. Extract the solution from the reduced basis
```
