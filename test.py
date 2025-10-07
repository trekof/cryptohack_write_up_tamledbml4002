from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from factordb.factordb import FactorDB

f = FactorDB(461733370363)
# Connect to the FactorDB API
f.connect()

# Get the list of factors
factors = f.get_factor_list()

# Print the factors
print(factors)


p = 461733370363

g = 2

ga = 114088419126

gb = 276312808197

a=0
b=0

for i in range(1, p):
    if pow(g, i, p) == ga:
        print("ga = ", i)
        a=i
    if pow(g, i, p) == gb:
        print("gb = ", i)
        b=i
    if (a!=0 or b!=0): break

if a==0:
    print(pow(ga,b,p))
else:
    print(pow(gb,a,p))