from totient import *

p = 857504083339712752489993810777
q = 1029224947942998075080348647219

e = 65537

m = totient_find(p,q)

def egcd(a: int, b: int):
    if b == 0: # when the function get to egcd(a,0) then it is egcd(gcd(a,b),0)
        return (a, 1, 0) # then 1*gcd = gcd -> true
    g, x, y = egcd(b, a%b)
    return (g, y , x- (a//b)* y) # so we have that x*a+y*b=g in the step before
# which is b and a%b = a - (a//b)*b in the round comming up
# so it will be:
#   x*b + y*(a-(a//b)*b) = g
#   x*b + y*a - y*(a//b)*b = g
#   a*y + b(a - (a//b)*b) = g
#   and that is how we have the next parameter for x and y

def modinv(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        print("No modular inverse (numbers not coprime)")
        return -1
    return x % m
# modinv(x) of a mod m is an x that fit:
#           a*x = 1 (mod m)

print(modinv(e, m))
for i in range(1, 1000, 50):
    print(f"{i} modinv with 65537 = {modinv(i,e)}")
