from totient import (is_prime, totient_find)
from private_key import (modinv, egcd)

# Read the file
with open("output.txt", "r") as f:
    content = f.read()

# Execute the content safely
local_vars = {}
exec(content, {}, local_vars)

# Extract variables
p = local_vars["p"]
a = local_vars["a"]

def legendre_check(a: int, b: int) -> int:
    """check the legendre of a mod p"""
    result = pow(a, (b-1)//2, b)  # fast modular exponentiation
    # print(f"{a} {b} {result}")
    return result

# hàm kiểm tra theo tonelli-shanks - toàn bộ được tham khảo trên chat gpt sau khi đã tìm hiểu về thuận toán
def tonelli_shanks(a, p):
    """Tìm x sao cho x^2 ≡ a mod p, với p lẻ và a là quadratic residue"""
    # Kiểm tra a có phải residue không
    if legendre_check(a, p) != 1:
        raise ValueError(f"{a} không phải quadratic residue modulo {p}")

    # Trường hợp đặc biệt p ≡ 3 mod 4
    if p % 4 == 3:
        x = pow(a, (p+1)//4, p)
        return x, p-x

    # Bước chuẩn bị: viết p-1 = Q * 2^S
    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1

    # Tìm một non-residue z
    z = 2
    while legendre_check(z, p) != p-1:
        z += 1

    # Khởi tạo
    M = S
    c = pow(z, Q, p)
    t = pow(a, Q, p)
    R = pow(a, (Q+1)//2, p)

    while t != 1:
        # Tìm i nhỏ nhất sao cho t^{2^i} ≡ 1
        i = 0
        temp = t
        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1
            if i == M:
                print("Không tìm thấy i thỏa mãn")
        # Cập nhật
        b = pow(c, 2**(M-i-1), p)
        R = (R * b) % p
        t = (t * pow(b, 2, p)) % p
        c = pow(b, 2, p)
        M = i

    return R, p-R

x1, x2 = tonelli_shanks(a, p)
print(min(x1,x2))