from math import isqrt
from Crypto.Util.number import GCD, inverse
from factordb.factordb import FactorDB

# Khởi tạo
p = 461733370363
g = 2
ga = 114088419126  # g^a mod p
gb = 276312808197  # g^b mod p

# ---------------------------
# 1️⃣ Hàm Baby-Step Giant-Step để tìm log_g(h) mod p
# ---------------------------
def baby_step_giant_step(g, h, p):
    """
    Giải phương trình g^x = h (mod p)
    Trả về x nếu tìm thấy, None nếu không.
    """
    m = isqrt(p - 1) + 1  # m = ceil(sqrt(p-1))
    
    # Baby steps: lưu g^j mod p vào bảng
    table = {} # đây là dictionary: được lưu dưới dạng table{"key0"=v1, "key2"=v2, ...} 
    # nên khi ta dò thì là ta đang dò các key có trong table chứ không phải giá trị
    # cấu trúc này là lý do mà tốc độ của việc tìm kiếm trở nên nhanh hơn bruteforce
    e = 1
    for j in range(m):
        if e not in table:
            table[e] = j
        e = (e * g) % p

    # Tiền tính g^(-m) gộp với g^(-m) mod p
    g_inv_m = pow(inverse(g, p), m, p)
    
    # Giant steps: duyệt i, kiểm tra h * (g^-m)^i
    gamma = h
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma] # tìm tại key gamma -> value = j
        gamma = (gamma * g_inv_m) % p
    
    return None  # Không tìm thấy

# ---------------------------
# 2️⃣ Tìm a bằng BSGS
# ---------------------------
a = baby_step_giant_step(g, ga, p)
print("a =", a)

# ---------------------------
# 3️⃣ Tính shared key
# ---------------------------
shared_key = pow(gb, a, p)
print("Shared key =", shared_key)
