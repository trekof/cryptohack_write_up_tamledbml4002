def extended_gcd(a: int, b: int):
    """
    Extended Euclidean Algorithm.
    Returns (g, u, v) where g = gcd(a, b) and u, v satisfy a*u + b*v = g.
    """
    # Base case
    if b == 0:
        return a, 1, 0
    # as for example :
    # initial was gcd(4,3)
    # then it will be gcd(3,1) next
    # then it will be gcd(1,0)
    # this will return as: 1,1,0 for it will be understand as 1*1+0*0 = 1
    # then 0*3 + 1*1 = 1
    # then 4*1 + 3*(-1) = 1 
    # Recursive step
    g, x1, y1 = extended_gcd(b, a % b)
    # explain the recursion step:
    # the inherited x1, y1 of the step before would match that x1*b + y1*(a%b) = g
    # Update x, y using results of recursion
    x = y1
    y = x1 - (a // b) * y1
    # now, how will it be = g, for x1*b + y1*(a%b) = g
    # we have : a%b = a-q*b #for q = a//b
    # g = x1*b + y1*(a%b)
    #   = x1*b + y1*(a-qb) 
    #   = x1*b + y1*a - y1*q*b
    #   = a*y1 + b*(x1 - y1*q)
    # reverse:
    # x*a + y*b = y1*a + x1 - (a//b)*y1 *b
    #           = y1*a + x1*b - q*y1*b
    #           = y1(a-q*b) + x1*b
    #           = y1*(a%b) + x1*b = g
    return g, x, y



p = 26513
q = 32321

g, u, v = extended_gcd(p, q)
print("gcd:", g)           
print("u:", u)            
print("v:", v)             
print(p*u + q*v)      # for checking      
