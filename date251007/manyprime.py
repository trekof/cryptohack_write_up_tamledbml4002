#!/usr/bin/env python3
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from factordb.factordb import FactorDB
from math import prod


with open("output_manyprime.txt") as f:
    content = f.read()
    
local_vars = {}
exec(content, {}, local_vars)

n = local_vars["n"]
e = local_vars["e"]
ct = local_vars["ct"]

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
    
d = inverse(e, phi)

# FLAG = b"crypto{???????????????}"
# pt = bytes_to_long(FLAG)
# ct = pow(pt, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"ct = {ct}")

pt = pow(ct, d, n)

print(pt)

plaintext = long_to_bytes(pt).decode()
print("Plaintext (decoded):", plaintext)
