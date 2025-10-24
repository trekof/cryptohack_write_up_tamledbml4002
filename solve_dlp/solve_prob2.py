#!/usr/bin/env python3
"""
Vì sao chọn BSGS:
- Biết rằng private key x chỉ dài 40 bit ⇒ không vượt quá 2^40 ≈ 1 nghìn tỷ.
- Các thuật toán như Pollard-Rho hoặc Pohlig-Hellman chỉ tốt khi order nhỏ hoặc có cấu trúc, 
  trong khi đây là nhóm elliptic curve không có yếu tố đặc biệt.
- BSGS cho phép tìm x trong O(√N) ≈ 2^20 ≈ 1 triệu bước, rất khả thi.
- Đây là cách tối ưu nhất khi ta chỉ biết rằng x nhỏ (giới hạn bit size).
"""

import hashlib, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ---------- parameters ----------
p = 81663996540811672901764249733343363790991183353803305739092974199965546219729
a = 1
b = 7
Gx = 14023374736200111073976017545954000619736741127496973904317708826835398305431
Gy = 23173384182409394365116200040829680541979866476670477159886520495530923549144
Px = 45277951688968912485631557795066607843633896482130484276521452596515645125170
Py = 33416418291776817124002088109454937261688060362650609033690500364258401702752

ciphertext_hex = '44af53c95092c86c04b67358aad3911282347862fec02f8943ea2eb5297780a7098faef27b2d2dbab7cf29bec5e32adcc7be6f4b57370aa2b6f6d1eafc5c3f3a07db1162d00b0037b757450b6fd405e0'
iv_hex = '29d6bba244e66a562969a6dae8e61449'

# ---------- EC helpers ----------
O = (None, None)
def is_O(P): return P[0] is None
def inv_mod(x, m): return pow(x, -1, m)

def point_add(P, Q):
    if is_O(P): return Q
    if is_O(Q): return P
    x1,y1 = P; x2,y2 = Q
    if x1 == x2:
        if (y1 + y2) % p == 0:
            return O
        num = (3 * x1 * x1 + a) % p
        den = (2 * y1) % p
        lam = (num * inv_mod(den, p)) % p
    else:
        num = (y2 - y1) % p
        den = (x2 - x1) % p
        lam = (num * inv_mod(den, p)) % p
    xr = (lam * lam - x1 - x2) % p
    yr = (lam * (x1 - xr) - y1) % p
    return (xr, yr)

def point_mul(P, n):
    if is_O(P) or n == 0: return O
    if n < 0:
        x,y = P
        return (x, (-y) % p)
    R = O
    Q = P
    while n:
        if n & 1:
            R = point_add(R, Q)
        Q = point_add(Q, Q)
        n >>= 1
    return R

# ---------- BSGS ----------
def ec_bsgs_bound(G, P, bound):
    """
    Find x with 0 <= x < bound s.t. x*G = P using BSGS.
    Returns x or None.
    """
    from math import isqrt, ceil
    m = isqrt(bound) + 1
    print(f"[+] BSGS with bound={bound}, m={m}")
    # baby steps: j*G for j in [0..m-1]
    baby = dict()
    R = O
    start = time.time()
    for j in range(m):
        # store by x-coordinate; collisions extremely unlikely for distinct points
        if R[0] not in baby:
            baby[R[0]] = j
        R = point_add(R, G)
        if j and j % 100000 == 0:
            print(f"  built baby steps {j}/{m} (elapsed {time.time()-start:.1f}s)")
    print(f"  done baby steps, time {time.time()-start:.1f}s, entries {len(baby)}")

    # precompute m*G
    mG = point_mul(G, m)
    # giant steps: check P - i*(mG) for i in [0..m]
    cur = P
    for i in range(m+1):
        if cur[0] in baby:
            j = baby[cur[0]]
            x = i * m + j
            if x < bound and point_mul(G, x) == P:
                print(f"[+] Found x = {x} (i={i}, j={j})")
                return x
        # cur = cur - mG  --> i.e. cur = cur + (-mG)
        if mG != O:
            cur = point_add(cur, (mG[0], (-mG[1]) % p))
        if i and i % 100000 == 0:
            print(f"  giant steps {i}/{m} (elapsed {time.time()-start:.1f}s)")
    print("[-] No solution < bound found.")
    return None

# ---------- decrypt helper ----------
def try_decrypt_with_x(x):
    key = hashlib.sha1(str(x).encode('ascii')).digest()[:16]
    iv = bytes.fromhex(iv_hex)
    ct = bytes.fromhex(ciphertext_hex)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    try:
        pt = unpad(cipher.decrypt(ct), 16)
        return pt
    except Exception as e:
        return None

# ---------- main ----------
if __name__ == '__main__':
    G = (Gx, Gy)
    P = (Px, Py)
    # confirm points on curve
    def on_curve(P):
        if is_O(P): return True
        x,y = P
        return (y*y - (x*x*x + a*x + b)) % p == 0
    assert on_curve(G) and on_curve(P), "Points not on curve!"

    B = 1 << 40   # bound
    start_total = time.time()
    x = ec_bsgs_bound(G, P, B)
    if x is None:
        print("No x found up to bound. Consider increasing resources.")
    else:
        print("x =", x)
        pt = try_decrypt_with_x(x)
        if pt is not None:
            print("Decrypted plaintext (flag):")
            print(pt)
        else:
            print("Decryption with found x failed (unexpected).")
    print("Total elapsed:", time.time()-start_total)
