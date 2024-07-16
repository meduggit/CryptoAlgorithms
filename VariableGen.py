import os

def generate_iv():
    return os.urandom(64)
    
# Generate 4 IVs
iv1 = generate_iv()
iv2 = generate_iv()
iv3 = generate_iv()
iv4 = generate_iv()

# Convert byte arrays to comma-separated string format
iv1_str = ', '.join(map(str, iv1))
iv2_str = ', '.join(map(str, iv2))
iv3_str = ', '.join(map(str, iv3))
iv4_str = ', '.join(map(str, iv4))

# Print the IVs in the required format
print(f"IV1: {iv1_str}")
print(f"IV2: {iv2_str}")
print(f"IV3: {iv3_str}")
print(f"IV4: {iv4_str}")
