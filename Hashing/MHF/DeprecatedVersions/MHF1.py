def HashingFunction(message, iterations=1000):
    # Define a prime number for mixing
    prime = 1023
    # Initialize the hashed value
    hashed_value = 7
    # Loop through each character in the message
    for char in message:
        # Multiply the hashed value by the prime number and add the value of the character
        hashed_value = hashed_value * prime 
        # Mix the hashed value
        for _ in range(iterations):
            hashed_value = (hashed_value >> 3) ^ (hashed_value << 5)
            hashed_value &= 0xFFFFFFFFFFFFFFFF  # Ensure the value fits into 64 bits
    # Convert the hashed value to hexadecimal representation
    hex_hash = hex(hashed_value)[2:]  # [2:] to remove '0x' prefix
    return hex_hash

print(HashingFunction("010"))