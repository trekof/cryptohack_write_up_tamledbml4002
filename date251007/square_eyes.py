from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from factordb.factordb import FactorDB

with open("output_square_eyes.txt") as f:
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

p = factors[0]
q = factors[1]

print(n-p*q)

phi = (p - 1) * q
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