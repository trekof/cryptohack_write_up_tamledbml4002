#!/usr/bin/env python3
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from factordb.factordb import FactorDB
from math import prod


with open("output_mi.txt") as f:
    content = f.read()
    
local_vars = {}
exec(content, {}, local_vars)

n = local_vars["n"]
e = local_vars["e"]
ct = local_vars["ct"]

print(f"n = {n}")
print(f"e = {e}")
print(f"ct = {ct}")

f = FactorDB(n)
# Connect to the FactorDB API
f.connect()

# Get the list of factors
factors = f.get_factor_list()

# Print the factors
print(factors)

def decrement_list(lst):
    """Trả về một list mới, mỗi phần tử giảm 1"""
    return [x - 1 for x in lst]

phi_fac = decrement_list(factors)

phi = prod(phi_fac)

print(phi)

print(phi%e)

# d = inverse(e, phi) # failed cause phi is devidable by e

# as we can see, the ct is kinda small for the n itself, so I may try cube root it

# pt = pow(ct, d, n)
# decrypted = long_to_bytes(pt)
# assert decrypted == flag

# pt = pow(ct, d, n)

# print(pt)

# pt = round(ct ** (1/3))
# if pt**3 == ct:
#     print("Yes, cube root works!")
# else:
#     print("No, modulus reduction happened.")

# failed cube rooted

# safer way to cube root the integer
def iroot3(x):
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi) // 2
        if mid**3 < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


pt = iroot3(ct)
if pt**3 == ct:
    print("✔ Cube root attack successful!")
else:
    print("✘ Cube root check failed. (But it's probably still plaintext.)")


plaintext = long_to_bytes(pt).decode()
print("Plaintext (decoded):", plaintext)
