from math import gcd

a = [588,665,216,113,642,4,836,114,851,492,819,237] #remainders
# this will be x^k...x^(k+11)
print("max remainder found is: ", max(a))
print("total remainder: ", len(a))
# as the highest remainder is 851
# we will have a set for all prime stand between 851 and 999

prime = [853, 857, 859, 863,
877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
947, 953, 967, 971, 977, 983, 991, 997]

# there is a clue online that give: x = x mod p -> ai.aj.x = ai.aj.x mod p -> ai+1.aj = ai.aj+1 mod p
# so ai+1.aj - ai.aj+1 is devidable by p and that will work for every tuple founded

D = []
n = len(a)
for i in range(n-1):
    for j in range(i+1, n-1):
        val = a[i+1]*a[j] - a[i]*a[j+1]
        D.append(abs(val))

g = 0
for d in D:
    if d != 0:
        g = gcd(g, d)
print(g)
        
p=g
# so we find out that p = 919
# it is time to find x

# same above as we have: x = x mod p = x.ai.ai^-1 = ai+1.ai^-1

def find_invert(a: int, b: int) -> int:
    a = a % b  # lower the number without changing the outcome
    x = 1
    while True:
        if (a * x) % b == 1:
            return x
        x += 1
        if x == b:  # no inverse found
            print(f"{a} has no inverse modulo {b}")
            
inv = find_invert(a[1], p)
x=(a[2]*inv)%p

# tìm số mũ khởi điểm - không yêu cầu
for k in range(p):  # thử từ 0 đến p-1
    if pow(x, k, p) == a[0]:
        print("k =", k)
        break

print (f"crypto{{{p},{x}}}")