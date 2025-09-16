def GCD(a: int, b: int) -> int:
    if a<b:
        a,b = b, a
    if a%b == 0:
        return b
    else: return GCD(b,a-b)
    
a=66528
b=52920

print(GCD(a,b))