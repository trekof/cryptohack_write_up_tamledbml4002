def find_quad(a: int, b: int):
    x = 1
    while True:
        if (x*x) %b == a%b:
            return x
        x += 1
        if x > 100:  # no inverse found
            print(f"{a} has no inverse modulo {b}")
            return -1
            # raise ValueError(f"{a} has no inverse modulo {b}")
        
# Find the quadratic residue and then calculate its square root. Of the two possible roots, submit the smaller one as the flag.
# p=29  ints=[14,6,11]
print(find_quad(14, 29))
print(find_quad(11, 29))
print(find_quad(6, 29))