from PIL import Image

lemur = Image.open("lemur.png").convert("RGB")
flag  = Image.open("flag.png").convert("RGB")

# Make sure the sizes match
assert lemur.size == flag.size

out = Image.new("RGB", lemur.size)
pixels_out = out.load()
pixels_l   = lemur.load()
pixels_f   = flag.load()

width, height = lemur.size
for y in range(height):
    for x in range(width):
        r1, g1, b1 = pixels_l[x, y]
        r2, g2, b2 = pixels_f[x, y]
        pixels_out[x, y] = (r1 ^ r2, g1 ^ g2, b1 ^ b2)

out.save("solution.png")
out.show()
