#!/usr/bin/env python3
"""
auto_recover_endless_emails.py (with plaintext printing)

Tries multiple automated strategies after the CRT candidate root was not exact:
- parse linewise (n,e,c)
- show pairwise gcds
- factor moduli sharing gcds and attempt decryption using the factorization
- try exact integer e-th root on each single c (m^e < n case)
- try CRT on combinations of blocks (sizes e..len(blocks)) and take e-th root
Stops when an exact plaintext is found and prints it.
"""

import sys
import math
import itertools
from Crypto.Util.number import long_to_bytes, inverse
from math import gcd

FNAME = sys.argv[1] if len(sys.argv) > 1 else "output_ee.txt"

# try to use gmpy2 iroot if available (faster & reliable)
try:
    import gmpy2
    have_gmpy2 = True
except Exception:
    have_gmpy2 = False

# ---------- helper to print plaintext cleanly ----------
def print_plaintext(b: bytes):
    """
    Try to decode bytes to utf-8 text and print it cleanly.
    Falls back to printing a repr and hex if decode fails.
    Exits the program after printing.
    """
    try:
        text = b.decode('utf-8')
        print("\n[+] Plaintext (utf-8):\n" + text)
    except Exception:
        # fallback: printable repr + hex (useful for debugging)
        print("\n[+] Plaintext (bytes repr):")
        print(repr(b))
        print("\n[+] Plaintext (hex):")
        print(b.hex())
    sys.exit(0)

# ---------- parsing ----------
def parse_linewise(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f if l.strip()]
    triples = []
    i = 0
    while i < len(lines):
        if lines[i].lower().startswith("n ="):
            try:
                if not (lines[i+1].lower().startswith("e =") and lines[i+2].lower().startswith("c =")):
                    i += 1; continue
                n = int(lines[i].split("=",1)[1].strip())
                e = int(lines[i+1].split("=",1)[1].strip())
                c = int(lines[i+2].split("=",1)[1].strip())
                triples.append((n,e,c))
                i += 3
            except Exception:
                i += 1
        else:
            i += 1
    return triples

# ---------- iterative egcd & modular inverse (safe) ----------
def egcd_iter(a, b):
    """
    Extended Euclidean Algorithm.
    Returns (g, u, v) where g = gcd(a, b) and u, v satisfy a*u + b*v = g.
    """
    # Base case
    if b == 0:
        return a, 1, 0
    
    # Recursive step
    g, x1, y1 = egcd_iter(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def modinv(a, m):
    """Modular invert for big number"""
    a = a % m
    try:
        return pow(a, -1, m)
    except TypeError:
        g, x, _ = egcd_iter(a, m)
        if g != 1:
            raise ValueError("modinv does not exist")
        return x % m

# ---------- integer nth root ----------
def integer_nth_root(a, n):
    if have_gmpy2:
        r, exact = gmpy2.iroot(a, n)
        return int(r), bool(exact)
    # binary search fallback
    if a < 0:
        raise ValueError("a must be >= 0")
    if a == 0:
        return 0, True
    lo = 0
    hi = 1 << ((a.bit_length() + n - 1)//n + 1)
    while lo + 1 < hi:
        mid = (lo + hi)//2
        p = mid**n
        if p == a:
            return mid, True
        if p < a:
            lo = mid
        else:
            hi = mid
    if lo**n == a:
        return lo, True
    return lo, False

# ---------- CRT helpers (pairwise, requires coprime moduli) ----------
def crt_pair(x1, m1, x2, m2):
    g = math.gcd(m1, m2)
    if g != 1:
        raise ValueError(f"Moduli not coprime: gcd={g}")
    inv = modinv(m1, m2)
    t = ((x2 - x1) * inv) % m2
    X = x1 + m1 * t
    M = m1 * m2
    return X % M, M

def crt_list(remainders, moduli):
    X, M = remainders[0], moduli[0]
    for r,m in zip(remainders[1:], moduli[1:]):
        X, M = crt_pair(X, M, r, m)
    return X, M

# ---------- main flow ----------
def main():
    blocks = parse_linewise(FNAME)
    if not blocks:
        print("No blocks found in", FNAME); return
    print(f"Found {len(blocks)} blocks.")
    ns = [b[0] for b in blocks]
    es = [b[1] for b in blocks]
    cs = [b[2] for b in blocks]
    e_set = set(es)
    if len(e_set) != 1:
        print("Warning: different exponents found:", e_set)
    e = es[0]
    print("Using exponent e =", e)

    # 1) Pairwise gcds - look for shared factors
    print("\n[*] Pairwise gcds (only show gcd>1):")
    shared = []
    for i in range(len(ns)):
        for j in range(i+1, len(ns)):
            g = math.gcd(ns[i], ns[j])
            if g != 1:
                print(f"  gcd(n[{i}], n[{j}]) = {g}")
                shared.append((i,j,g))
    if shared:
        print("\n[*] Trying to use shared gcds to factor moduli and decrypt related blocks.")
        for (i,j,g) in shared:
            p = g
            # factor n[i] and n[j]
            qi = ns[i] // p
            qj = ns[j] // p
            print(f"  For pair ({i},{j}): p = {p}, q_i = {qi}, q_j = {qj}")
            # try decrypting block i
            try:
                phi_i = (p-1)*(qi-1)
                d_i = inverse(e, phi_i)
                m_i = pow(cs[i], d_i, ns[i])
                pt_i = long_to_bytes(m_i)
                print_plaintext(pt_i)
            except Exception as exc:
                print(f"  Could not decrypt block {i}: {exc}")
            # try decrypting block j
            try:
                phi_j = (p-1)*(qj-1)
                d_j = inverse(e, phi_j)
                m_j = pow(cs[j], d_j, ns[j])
                pt_j = long_to_bytes(m_j)
                print_plaintext(pt_j)
            except Exception as exc:
                print(f"  Could not decrypt block {j}: {exc}")
    else:
        print("  No shared gcds found.")

    # 2) Try individual exact e-th root on each c (maybe m^e < n for some)
    print("\n[*] Trying exact e-th root on each individual ciphertext:")
    for i,(n_i,e_i,c_i) in enumerate(blocks):
        root, exact = integer_nth_root(c_i, e)
        if exact:
            try:
                pt = long_to_bytes(root)
                print_plaintext(pt)
            except Exception as exc:
                print(f"  Block {i}: root -> bytes failed: {exc} (decimal m={root})")
        else:
            # debug info
            # if root**e % n == c, candidate might be root
            if pow(root, e, n_i) == c_i:
                try:
                    pt = long_to_bytes(root)
                    print_plaintext(pt)
                except Exception:
                    print(f"  Block {i}: candidate integer (decimal): {root}")
            else:
                print(f"  Block {i}: not exact (floor root).")

    # 3) Try CRT on subsets of blocks
    print("\n[*] Trying CRT on combinations of blocks (size e .. {0})".format(len(blocks)))
    found = False
    for size in range(e, len(blocks)+1):
        print(f"  trying combinations of size {size}...")
        for combo in itertools.combinations(range(len(blocks)), size):
            moduli = [ns[i] for i in combo]
            rems = [cs[i] for i in combo]
            # basic coprime check
            ok = True
            for (a,b) in itertools.combinations(moduli,2):
                if math.gcd(a,b) != 1:
                    ok = False; break
            if not ok:
                continue
            try:
                X, M = crt_list(rems, moduli)
            except Exception:
                continue
            # try root
            root, exact = integer_nth_root(X, e)
            if exact:
                try:
                    pt = long_to_bytes(root)
                    print(f"\n[+] Success with combo {combo} (size {size})!")
                    print_plaintext(pt)
                    found = True
                    break
                except Exception:
                    print(f"\n[+] Found exact root but long_to_bytes failed. m={root}")
                    found = True
                    break
        if found:
            break
    if not found:
        print("\n[-] No exact recovery via CRT on tested combinations.")

    # 4) If still nothing, provide candidate floor root for full CRT (report what you saw)
    print("\n[*] As a last diagnostic, try the full-CRT floor root candidate (what you saw).")
    try:
        allX, allM = crt_list(cs, ns)
        r, exact = integer_nth_root(allX, e)
        print("full CRT combined modulus bits:", allM.bit_length())
        print("floor root length (bytes):", (r.bit_length()+7)//8)
        try:
            print("floor candidate (bytes):", long_to_bytes(r))
        except Exception:
            print("floor candidate (decimal):", r)
        if exact:
            print("[!] Unexpectedly exact for full CRT (should have been caught earlier).")
    except Exception as exc:
        print("Full CRT failed:", exc)

    print("\nDone. If none of the above found the plaintext, possible reasons:\n"
          " - combined m^e >= product(n_i) for all tested subsets (CRT gave only floor root)\n"
          " - some n_i share factors that break simple CRT (we tried to detect shared gcds)\n"
          " - message may be padded/structured differently (Coppersmith or other advanced methods needed)\n\n"
          "Next steps you can try:\n"
          " - try more combinations (or all subsets) if you have more blocks\n"
          " - attempt factoring the moduli (e.g. via FactorDB) and decrypt single blocks\n"
          " - if you want, paste any decrypted intermediate outputs here and I can help analyze them.")

if __name__ == "__main__":
    main()
