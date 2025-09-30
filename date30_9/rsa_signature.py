import hashlib
from Crypto.Util.number import bytes_to_long, long_to_bytes
import base64

# đọc N,d từ private.key dạng key=value
def read_private_key(path):
    dct = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            k,v = line.split("=", 1)
            dct[k.strip()] = int(v.strip())
    return dct["N"], dct["d"]

N, d = read_private_key("private.key")
e = 65537  # public exponent thường dùng

message = b"crypto{Immut4ble_m3ssag1ng}"
h_int  = bytes_to_long(hashlib.sha256(message).digest())


# ký: S = H(m)^d mod N
S = pow(h_int, d, N)

print(S)

# xuất signature ra file:
sig_bytes = long_to_bytes(S, (N.bit_length()+7)//8)  # padded to modulus size

with open("signature.bin","wb") as f:
    f.write(sig_bytes)

# lưu dạng hex / base64 nếu cần:
with open("signature.hex","w") as f:
    f.write(hex(S)[2:])

with open("signature.b64","w") as f:
    f.write(base64.b64encode(sig_bytes).decode())

# verify: pow(S,e,N) == h_int % N
S_read = int(open("signature.hex").read().strip(), 16)
print(pow(S_read, e, N) == h_int % N)
