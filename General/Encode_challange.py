from pwn import remote  # pwntools
import json
import base64
import codecs
from Crypto.Util.number import long_to_bytes

# connect to CryptoHack server
r = remote('socket.cryptohack.org', 13377)

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

while True:
    received = json_recv()
    print("Received:", received)

    # stop when flag is received
    if "flag" in received:
        print("FLAG:", received["flag"])
        break

    enc_type = received["type"]
    enc_value = received["encoded"]

    # decode based on type
    if enc_type == "base64":
        decoded = base64.b64decode(enc_value).decode()
    elif enc_type == "hex":
        decoded = bytes.fromhex(enc_value).decode()
    elif enc_type == "rot13":
        decoded = codecs.decode(enc_value, 'rot_13')
    elif enc_type == "bigint":
        decoded = long_to_bytes(int(enc_value, 16)).decode()
    elif enc_type == "utf-8":
        decoded = "".join(chr(c) for c in enc_value)
    else:
        raise Exception("Unknown encoding: " + enc_type)

    print("Decoded:", decoded)

    # send back the decoded result
    to_send = {
        "decoded": decoded
    }
    json_send(to_send)

# flag is crypto{3nc0d3_d3c0d3_3nc0d3}