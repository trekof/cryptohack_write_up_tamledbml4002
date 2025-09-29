# Read the file
with open("output.txt", "r") as f:
    content = f.read()

# Execute the content safely
local_vars = {}
exec(content, {}, local_vars)  # run code in isolated dict

# Extract variables
p = local_vars["p"]
a = local_vars["a"]

print(a,p)