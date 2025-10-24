import math
import random
import time
from sympy import factorint, isprime
from sympy.ntheory.modular import crt
from sympy.ntheory import n_order

# ---------- BSGS (được sử dụng chung) ----------
def baby_step_giant_step_for_order(g, a, p, order_bound):
    n = int(math.sqrt(order_bound)) + 1
    table = {}
    val = 1
    for j in range(n):
        if val not in table:
            table[val] = j
        val = (val * g) % p

    try:
        g_n_inv = pow(pow(g, n, p), -1, p)
    except ValueError:
        return None

    gamma = a
    for i in range(n + 1):
        if gamma in table:
            x = i * n + table[gamma]
            if x < order_bound and pow(g, x, p) == a % p:
                return x
        gamma = (gamma * g_n_inv) % p
    return None

# ---------- Pohlig–Hellman ----------
def pohlig_hellman(g, a, p):
    try:
        order = p - 1 if isprime(p) else n_order(g, p)
    except:
        order = p - 1

    factors = factorint(order)
    if not factors:
        return None

    residues = []
    moduli = []

    for q, e in factors.items():
        pe = q ** e
        gamma = pow(g, order // pe, p)
        h = pow(a, order // pe, p)

        x_pe = baby_step_giant_step_for_order(gamma, h, p, pe)
        if x_pe is None:
            return None

        residues.append(x_pe)
        moduli.append(pe)

    result = crt(moduli, residues)[0]
    if pow(g, result, p) == a % p:
        return result
    return None

# ---------- Pollard’s Rho ----------
def pollard_rho_dlog(g, a, p, max_tries=200, iter_mul=20):
    order = p - 1 if isprime(p) else n_order(g, p)

    def f(X, A, B):
        r = X % 3
        if r == 0:
            X = (X * g) % p
            A = (A + 1) % order
        elif r == 1:
            X = (X * a) % p
            B = (B + 1) % order
        else:
            X = (X * X) % p
            A = (2 * A) % order
            B = (2 * B) % order
        return X, A, B

    for attempt in range(max_tries):
        A = random.randrange(order)
        B = random.randrange(order)
        X = (pow(g, A, p) * pow(a, B, p)) % p

        X2, A2, B2 = X, A, B
        max_iter = iter_mul * int(math.sqrt(order)) + 10

        for _ in range(1, max_iter + 1):
            X, A, B = f(X, A, B)
            X2, A2, B2 = f(*f(X2, A2, B2))

            if X == X2:
                r = (A - A2) % order
                s = (B2 - B) % order
                if s == 0:
                    break
                g0 = math.gcd(s, order)
                if g0 == 1:
                    try:
                        s_inv = pow(s, -1, order)
                        x = (r * s_inv) % order
                        if pow(g, x, p) == a % p:
                            return x
                    except ValueError:
                        break
                else:
                    if r % g0 != 0:
                        break
                    r_red = r // g0
                    s_red = s // g0
                    order_red = order // g0
                    try:
                        s_inv = pow(s_red, -1, order_red)
                        x_base = (r_red * s_inv) % order_red
                        for k in range(g0):
                            x_cand = x_base + k * order_red
                            if pow(g, x_cand, p) == a % p:
                                return x_cand
                    except ValueError:
                        break
                break
    return None

# ---------- Dispatcher ----------
def discrete_log_solver(g, a, b, alg="bsgs"):
    g = g % b
    a = a % b

    if a == 1:
        return 0
    if g == 0:
        return None if a != 0 else 0
    if g == 1:
        return None if a != 1 else 0

    alg = alg.lower()
    start_time = time.perf_counter()

    if alg == "bsgs":
        print(f"→ Đang chạy Baby-step Giant-step")
        try:
            order = b - 1 if isprime(b) else n_order(g, b)
        except:
            order = b - 1
        result = baby_step_giant_step_for_order(g, a, b, order)
    elif alg == "p-hellman":
        print(f"→ Đang chạy Pohlig–Hellman")
        result = pohlig_hellman(g, a, b)
    elif alg == "pollard-rho":
        print(f"→ Đang chạy Pollard’s Rho")
        result = pollard_rho_dlog(g, a, b)
    else:
        raise ValueError("Unknown algorithm")

    elapsed = time.perf_counter() - start_time
    print(f"   ⏱️ Thời gian chạy ({alg}): {elapsed:.6f}s")
    return result

# ---------- 10 bộ test ----------
def run_tests():
    print("\n================= KIỂM THỬ 10 BỘ MẪU =================\n")
    test_cases = [
        (5, 3, 11),
        (2, 8, 13),
        (7, 15, 23),
        (3, 10, 17),
        (5, 9, 19),
        (6, 9, 31),
        (7, 13, 37),
        (10, 4, 41),
        (11, 17, 43),
        (2, 7, 29),
    ]

    for i, (g, a, p) in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: g={g}, a={a}, p={p} ---")

        res1 = discrete_log_solver(g, a, p, "bsgs")
        res2 = discrete_log_solver(g, a, p, "p-hellman")
        res3 = discrete_log_solver(g, a, p, "pollard-rho")

        print(f"✅ BSGS: {res1}")
        print(f"✅ Pohlig–Hellman: {res2}")
        print(f"✅ Pollard–Rho: {res3}")

        # Kiểm tra đồng nhất
        correct = all(r is not None and r == res1 for r in [res2, res3])
        print("   ➤ Kết luận:", "Tất cả khớp ✅" if correct else "Không khớp ⚠️")

# ---------- main ----------
if __name__ == "__main__":
    g, a, p = 91, 15, 17
    print(f"Ví dụ ban đầu: g={g}, a={a}, p={p}\n")

    for alg in ["bsgs", "p-hellman", "pollard-rho"]:
        res = discrete_log_solver(g, a, p, alg)
        print(f"{alg} -> {res}")

    run_tests()

# Trong các phần ở trên thì hiện tại mới chỉ có thể hiểu được cách hoạt động của bsgs 1 cách hoàn toàn nên mong anh thông cảm việc em dùng AI để hỗ trợ 2 thuật toán còn lại ạ

