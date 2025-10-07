# 11 ≡ x mod 6
# 8146798528947 ≡ y mod 17
def find_mod(a: int, b: int)->int:
    return a%b

a = find_mod(11,6)
b = find_mod(8146798528947,17)
result = a if a<b else b
print(result)