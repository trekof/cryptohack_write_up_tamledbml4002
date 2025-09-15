hex_str = '73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d'

cap1 = bytes.fromhex(hex_str)

key = 0x10

flag = bytes(key ^ c for c in cap1).decode()

print(flag)

