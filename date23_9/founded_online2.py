from Crypto.Cipher import AES
import hashlib

import requests
url1 = "http://aes.cryptohack.org/passwords_as_keys/"
r = requests.get(f"{url1}/encrypt_flag")
data = r.json()
c = data["ciphertext"]
ciphertext = bytes.fromhex(c)
with open("wordlist.txt") as f:
    words = [w.strip() for w in f.readlines()]
for i in words:
    key = hashlib.md5(i.encode()).digest()
    cipher = AES.new(key,AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    if b'crypto' in decrypted:
        print(i) # khóa được tìm thấy là
        print(decrypted)
