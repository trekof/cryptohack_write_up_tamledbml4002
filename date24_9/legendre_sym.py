# a = input("a")
# a = int(a)
# b = input("b")
# b = int(b)
# # Fermat Theorem check
# def fermat(a: int, b: int):
#     x = 1
#     return (a**(b-1))%b

# print(f"from {a} quad {b} {fermat(a,b)}")

# Read the file
with open("output.txt", "r") as f:
    content = f.read()

# Execute the content safely
local_vars = {}
exec(content, {}, local_vars)  # run code in isolated dict

# Extract variables
p = local_vars["p"]
ints_array = local_vars["ints"]

# Check
# print("p =", p)
# print("First 3 integers in array:", ints_array[:3])

# def legendre_check(a: int, b: int) -> bool:
#     print(f"{a} {b} {((a**((b-1)//2))%b) }")
#     return (((a**((b-1)/2))%b)==1) 

# for i in ints_array:
#     if legendre_check(i, p) == True:
#         print(p)
#         print(i)


def mod_sqrt(a, p):
    # works only if p % 4 == 3 and a is a quadratic residue
    x = pow(a, (p+1)//4, p)
    return max(x, p - x)

def legendre_check(a: int, b: int) -> int:
    result = pow(a, (b-1)//2, b)  # fast modular exponentiation
    # print(f"{a} {b} {result}")
    return result

for i in ints_array:
    if legendre_check(i, p)==1:
        print("the quad of:")
        print(i)
        print("and:")
        print(p)
        print("was:")
        print(mod_sqrt(i, p))
