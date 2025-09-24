from Crypto.Cipher import AES
from flask import Flask
import os

chal = Flask(__name__)


# KEY = ?
# FLAG = ?

KEY = os.environ.get("AES_KEY", "THIS_IS_16_BYTES").encode()
FLAG = os.environ.get("FLAG", "CTF{example_flag}")

ciphertext = 'c11949a4a2ecf929dfce48b39daedd9e6d90c67d2f550b79259bdda835348a48'

@chal.route('/block_cipher_starter/decrypt/<ciphertext>/')
def decrypt(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)

    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}


@chal.route('/block_cipher_starter/encrypt_flag/')
def encrypt_flag():
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(FLAG.encode())

    return {"ciphertext": encrypted.hex()}

if __name__ == "__main__":
    chal.run(port=5000, debug=True)