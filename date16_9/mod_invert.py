def find_invert(a: int, b: int) -> int:
    a = a % b  # lower the number without changing the outcome
    x = 1
    while True:
        if (a * x) % b == 1:
            return x
        x += 1
        if x == b:  # no inverse found
            raise ValueError(f"{a} has no inverse modulo {b}")
        
print(find_invert(3,13))