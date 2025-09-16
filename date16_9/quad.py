def find_quad(a: int, b: int) -> int:
    x = 1
    while True:
        if (x*x) %b == a:
            return x
        x += 1
        if x > 100:  # no inverse found
            raise ValueError(f"{a} has no inverse modulo {b}")
        
print(find_quad(6, 29))