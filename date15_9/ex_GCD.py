def extended_gcd(a: int, b: int):
    """
    Extended Euclidean Algorithm.
    Returns (g, u, v) where g = gcd(a, b) and u, v satisfy a*u + b*v = g.
    """
    # Base case
    if b == 0:
        return a, 1, 0
    # Recursive step
    g, x1, y1 = extended_gcd(b, a % b)
    # Update x, y using results of recursion
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y



p = 26513
q = 32321

g, u, v = extended_gcd(p, q)
print("gcd:", g)           
print("u:", u)             
print("v:", v)             
print(p*u + q*v)      # for checking      
