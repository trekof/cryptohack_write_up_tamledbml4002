import math

p = 857504083339712752489993810777
q = 1029224947942998075080348647219

def is_prime(a: int)-> bool:
    if a<=1: return False
    for i in range(2, int(math.sqrt(a))+1):
        if a % i == 0:
            return False
    return True
    
def totient_find(a: int, b: int) -> int:
    # if is_prime(a) and is_prime(b):
    return (a-1)*(b-1)

if __name__ == "__main__":
    print(totient_find(p,q))