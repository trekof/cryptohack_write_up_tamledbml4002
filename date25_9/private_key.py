from totient import *

p = 857504083339712752489993810777
q = 1029224947942998075080348647219

e = 65537

m = totient_find(p,q)

def egcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    g, x, y = egcd(b, a%b)
    return (g, y , x- (a//b)* y)

def modinv(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        print("No modular inverse (numbers not coprime)")
        return -1
    return x % m

print(modinv(e, m))
for i in range(1, 1000, 50):
    print(f"{i} modinv with 65537 = {modinv(i,e)}")
