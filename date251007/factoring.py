from factordb.factordb import FactorDB

n = 510143758735509025530880200653196460532653147

f = FactorDB(n)

# Connect to the FactorDB API
f.connect()

# Get the list of factors
factors = f.get_factor_list()

# Print the factors
print(factors)