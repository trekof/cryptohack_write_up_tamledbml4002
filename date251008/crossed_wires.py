#!/usr/bin/env python3
import ast
import sys
import math
from math import prod
from Crypto.Util.number import inverse, long_to_bytes
from factordb.factordb import FactorDB

e = 0x10001

# giải thích toàn bộ scheme:
#   người mã hóa đã dùng 1 bộ rsa cơ bản nhưng thay vì làm cho từng người 1 key thì họ đã mã hóa bằng cả 5 key cùng lúc
#   nghĩa là ciphertext cuối cùng chính là (((((m^e1)^e2)^e3)^e4)^e5) mod N
#   đó cũng chính bằng m^(prod(e_i)) mod N = m^E mod N
#   nên về căn bản là ta chỉ cần tìm phi, tìm E để ra D là đã có thể decrypt thành công


# --------------- FactorDB helper -------------------
def get_factors_from_factordb(N: int):
    f = FactorDB(N)
    f.connect()
    factors = f.get_factor_list()
    if not factors:
        raise RuntimeError("FactorDB returned no factors for N")
    # ensure all are ints
    factors = [int(x) for x in factors]
    return factors

def compute_phi_from_factors(factors):
    """
    Compute phi(N) from a factor list returned by FactorDB.
    Handles multiplicities if FactorDB returns repeated primes.
    phi(N) = product over distinct p: p^(a-1) * (p-1)
    where a is multiplicity.
    """
    # count multiplicities
    counts = {}
    for p in factors:
        counts[p] = counts.get(p, 0) + 1

    phi = 1
    for p, a in counts.items():
        # p^(a-1) * (p-1)
        phi *= pow(p, a-1) * (p - 1)
    return phi

# --------------- parse the file safely -------------------
with open("output_cw.txt", "r") as f:
    data = f.read()

def extract_literal_after(label: str):
    idx = data.find(label)
    if idx < 0:
        raise ValueError(f"Label not found: {label}")
    rest = data[idx + len(label):].strip()
    line = rest.splitlines()[0].strip()
    return line

priv_line = extract_literal_after("My private key:")
pubs_line = extract_literal_after("My Friend's public keys:")
cipher_line = extract_literal_after("Encrypted flag:")

my_key = ast.literal_eval(priv_line)          # (N, d)
friend_keys = ast.literal_eval(pubs_line)     # [(N, e1), (N, e2), ...]
cipher = int(cipher_line)

N, d_from_file = my_key

print("[*] Loaded values from file")
print("    N bit-length:", N.bit_length())
print("    number of friend keys:", len(friend_keys))

# --------------- get factors (FactorDB) -------------------
print("[*] Querying FactorDB for factors of N...")
factors = get_factors_from_factordb(N)
print("[+] FactorDB returned:", factors)

# compute phi robustly from factors (handles multiplicities)
phi = compute_phi_from_factors(factors)
print("[+] Computed phi from factors")

# Optional sanity: verify that e * d ≡ 1 (mod phi)
if (e * d_from_file - 1) % phi != 0:
    print("[!] Warning: provided d does not satisfy e*d ≡ 1 (mod phi). Continuing anyway.")
else:
    print("[+] Verified e*d ≡ 1 (mod phi) for d from file")

# --------------- build combined exponent E -------------------
E = 1
for (n_i, e_i) in friend_keys:
    if int(n_i) != int(N):
        raise ValueError("Different modulus in friend public keys (unexpected)")
    E *= int(e_i)

print("[*] Combined exponent E computed (length bits):", E.bit_length())

# ensure gcd(E, phi) == 1 (invertible)
g = math.gcd(E, phi)
if g != 1:
    raise RuntimeError(f"Combined exponent not invertible mod phi (gcd={g}). Can't compute inverse.")

D_total = inverse(E, phi)  # modular inverse of E mod phi
print("[*] Computed D_total (inverse of combined exponent)")

# --------------- decrypt -------------------
m = pow(cipher, D_total, N)
try:
    plaintext = long_to_bytes(m)
    print("[+] Decrypted plaintext bytes:")
    print(plaintext)
except Exception as exc:
    print("[!] Could not convert to bytes:", exc)
    print("    m (decimal):", m)
