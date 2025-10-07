# from random import randint
import ast

with open("output_as.txt", "r") as f:
    data = f.read().strip()

# dùng ast.literal_eval để chuyển chuỗi list thành Python list an toàn
ciphertext = ast.literal_eval(data)

a = 288260533169915
p = 1007621497415251

def legendre_check(a: int, b: int) -> int:
    result = pow(a, (b-1)//2, b)  # fast modular exponentiation
    # print(f"{a} {b} {result}")
    if result == 1:
        return result
    return -1

leg_a = legendre_check(a, p)
leg_minus1 = legendre_check(p-1, p)
leg_minus_a = (leg_a * leg_minus1)
print(leg_a,leg_minus1,leg_minus_a)
# từ đây bài dễ hơn vì a là residue nên mọi a^e sẽ là residue và khi nhân -1 sẽ không là residue

def legendre_bit(c, p):
    r = legendre_check(c,p)
    if r == 1:
        return '1'   # residue -> a^e -> b=1
    elif r == - 1:
        return '0'   # non-residue -> -a^e -> b=0
    else:
        raise ValueError("Unexpected Legendre result")

bits = ''.join(legendre_bit(c, p) for c in ciphertext)

# --- Bước 5: Gom thành byte ---
plaintext_bytes = []
for i in range(0, len(bits), 8):
    byte = bits[i:i+8]
    plaintext_bytes.append(int(byte, 2))

# --- Bước 6: In ra flag ---
flag = bytes(plaintext_bytes).decode()

print(flag)