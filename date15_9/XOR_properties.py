key1 = 'a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313'
keyxor12 = '37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e'
keyxor23 = 'c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1'
keyxor123flag = '04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf'

k1 = bytes.fromhex(key1)
k12 = bytes.fromhex(keyxor12)
k23 = bytes.fromhex(keyxor23)
k = bytes.fromhex(keyxor123flag)

def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(b1, b2))

#since key^(k1^k2^k3) so we find k1^k1^k3
key = xor_bytes(k1, k23)
result = xor_bytes(k, key)

flag = result.decode()

print(flag)
