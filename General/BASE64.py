import base64

hex_str = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"

a = bytes.fromhex(hex_str)

b = base64.b64encode(a)

print(b.decode())