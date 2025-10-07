from factordb.factordb import FactorDB

# Create a FactorDB object for the number 16
f = FactorDB(16)

# Connect to the FactorDB API
f.connect()

# Get the list of factors
factors = f.get_factor_list()

# Print the factors
print(factors)