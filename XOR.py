def xor_with_13(text):
    result = ""
    for c in text:
        # XOR Unicode code point with 13
        xored = ord(c) ^ 13
        result += chr(xored)
    return result

# given string
label = "label"

# apply XOR
new_string = xor_with_13(label)

# print the flag
print("crypto{" + new_string + "}")
