# run.py — pure-Python ECC + AES (không cần tinyec/sage)
from Crypto.Util.number import getRandomNBitInteger
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import urandom
from secret import flag

# curve params (from bạn)
p = 81663996540811672901764249733343363790991183353803305739092974199965546219729
a = 1
b = 7
Gx = 14023374736200111073976017545954000619736741127496973904317708826835398305431
Gy = 23173384182409394365116200040829680541979866476670477159886520495530923549144

# helpers: modular inverse (p là prime, nên dùng pow)
def modinv(x, p):
    return pow(x, p-2, p)

# point at infinity represented by None
O = None

def is_on_curve(P):
    if P is None:
        return True
    x, y = P
    return (y * y - (x * x * x + a * x + b)) % p == 0

def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return O
    if P == Q:
        # doubling
        if y1 == 0:
            return O
        num = (3 * x1 * x1 + a) % p
        den = (2 * y1) % p
        lam = (num * modinv(den, p)) % p
    else:
        if x1 == x2:
            return O
        num = (y2 - y1) % p
        den = (x2 - x1) % p
        lam = (num * modinv(den, p)) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mult(k, P):
    # double-and-add, k >= 0
    if k % p == 0 or P is None:
        return O
    if k < 0:
        # use -P
        return scalar_mult(-k, (P[0], (-P[1]) % p))
    R = O
    Q = P
    while k:
        if k & 1:
            R = point_add(R, Q)
        Q = point_add(Q, Q)
        k >>= 1
    return R

# check generator on curve
G = (Gx, Gy)
assert is_on_curve(G), "G không nằm trên curve!"

# secret random 40-bit
x = getRandomNBitInteger(40)
P = scalar_mult(x, G)

# AES key from sha1(x)
sha1 = hashlib.sha1()
sha1.update(str(x).encode('ascii'))
key = sha1.digest()[:16]
iv = urandom(16)

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
ciphertext = cipher.encrypt(pad(flag, 16))

print(f"a = {a}")
print(f"b = {b}")
print(f"p = {p}")
print(f"G = ({G[0]}, {G[1]})")
print(f"P = ({P[0]}, {P[1]})")
print(f"ciphertext = '{ciphertext.hex()}'")
print(f"iv = '{iv.hex()}'")
