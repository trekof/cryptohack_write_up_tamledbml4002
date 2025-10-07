from itertools import cycle

hex_str = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'

text = 'crypto{'

te = text.encode()

cap1 = bytes.fromhex(hex_str)

key_check = bytes(t ^ c for t, c in zip(te, cap1)).decode()

# print(key_check)
# it return myXORke
# so I add an y to complete the key and try again

key = 'myXORkey'

cyp_key = key.encode()

flag = bytes(k ^ c for k, c in zip(cycle(cyp_key) , cap1)).decode() # checked AI on how to use cycle 

print(flag)
