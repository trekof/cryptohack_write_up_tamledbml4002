from Crypto.Util.number import getPrime
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import urandom
from secret import flag

p = getPrime(256)
x = getPrime(64)
a, b = 1, 4
E = EllipticCurve(GF(p), [a, b])
G = E.random([0])
P = x*G

sha1 = hashlib.sha1()
sha1.update(str(P).encode('ascii'))
key = sha1.digest()[:16]
iv = urandom(16)

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
ciphertext = cipher.encrypt(pad(flag, 16))

print(f"a = {a}\nb = {b}\np = {p}\nP = {P}\nciphertext = {ciphertext.hex()}\niv = {iv.hex()}")
