def find_mod(a: int, b: int)->int:
    return a%b

# doing the test on in the challenge

# a = find_mod(3**17,17)
# print(a)

# so we now accept the theory of x^y mod m = x mod m

a = find_mod(273246787654**65536,65537)
print(a)