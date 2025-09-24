import requests

# print(bytes.fromhex('63727970746f7b626c30636b5f633170683372355f3472335f663435375f217d'))

# r = requests.get("http://aes.cryptohack.org/block_cipher_starter/encrypt_flag")
# print("status:", r.status_code)            # kiểm tra tình trạng api trả về
# print("header:", r.headers.get("Content-Type"))      # kiểm tra header file có phải json không
# data = r.json()                
# print(data)                 # kiểm tra trường dữ liệu có định dạng như nào -> {'ciphertext': '...'}
# cipher_hex1 = data.get("ciphertext")
# print(cipher_hex1)

# r = requests.get(f"http://aes.cryptohack.org/block_cipher_starter/decrypt/{cipher_hex1}/")
# print("status:", r.status_code)
# print("headers:", r.headers.get("Content-Type"))
# data = r.json()                 # 
# print(data)                 # kiểm tra trường dữ liệu có định dạng như nào -> {'plaintext': '...'} 
# flag_hex = data.get('plaintext')
# # nhưng plaintext này ở dạng hex nên ta phải giải nó ra
# print(bytes.fromhex(flag_hex))


# uncomment toàn bộ phần trên để kiểm tra mọi thứ

# ----------------final code:------------------------------------------

r = requests.get("http://aes.cryptohack.org/block_cipher_starter/encrypt_flag")
data = r.json()          
cipher_hex1 = data.get("ciphertext")
r = requests.get(f"http://aes.cryptohack.org/block_cipher_starter/decrypt/{cipher_hex1}/")
data = r.json() 
flag_hex = data.get('plaintext')
print(bytes.fromhex(flag_hex))
