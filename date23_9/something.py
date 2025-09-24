import requests
# import base64

BASE_URL = "https://aes.cryptohack.org/block_cipher_starter"

# Step 1: Test encryption with repeating blocks
plaintext = b"A" * 16 * 4  # 4 blocks of 16 bytes

r = requests.get(f"{BASE_URL}/encrypt/{plaintext.hex()}/")
data = r.json()

ciphertext_hex = data['ciphertext']
print("Ciphertext:", ciphertext_hex)

# Step 2: Check for repeating blocks (ECB detection)
blocks = [ciphertext_hex[i:i+32] for i in range(0, len(ciphertext_hex), 32)]
if len(blocks) != len(set(blocks)):
    print("ECB mode detected!")

# Step 3: Get the flag
# Usually, there is a /get_flag endpoint for starter challenges
flag_req = requests.get(f"{BASE_URL}/get_flag/")
flag_data = flag_req.json()
print("FLAG:", flag_data['flag'])
