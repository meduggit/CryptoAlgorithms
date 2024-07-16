import random

# Define the S-box
S_BOX = bytearray(random.getrandbits(8) for _ in range(32))

def generate_subkeys(key_hex, num_rounds):
    key = bytearray.fromhex(key_hex)  # Convert to bytearray
    subkeys = []

    # Generate subkeys for each round
    for _ in range(num_rounds):
        subkey = key[:16]  # Each subkey is of fixed length 16 bytes
        key = key[1:] + key[:1]  # Circular left shift the key by 1 byte
        subkeys.append(bytearray(subkey))  # Store subkey as a bytearray

    return subkeys

def encrypt(plaintext, key_hex):
    num_rounds = 10  # Example: Using 10 rounds
    subkeys = generate_subkeys(key_hex, num_rounds)

    iv = bytearray(random.getrandbits(8) for _ in range(16))
    encrypted_bytes = bytearray(iv)

    # Additive mixing done only once
    for j in range(len(subkeys)):
        subkey = subkeys[j]
        for i in range(len(subkey)):
            subkey[i] = (subkey[i] + S_BOX[(i + j) % len(S_BOX)]) % 256
        subkeys[j] = subkey

    for i, char in enumerate(plaintext.encode()):
        round_key = subkeys[i % num_rounds]
        encrypted_char = char
        for byte in round_key:
            encrypted_char ^= byte
        encrypted_bytes.append(encrypted_char)

    return encrypted_bytes.hex()

def decrypt(encrypted_hex, key_hex):
    num_rounds = 10  # Example: Using 10 rounds
    subkeys = generate_subkeys(key_hex, num_rounds)

    encrypted_bytes = bytes.fromhex(encrypted_hex)
    iv = encrypted_bytes[:16]
    encrypted_bytes = encrypted_bytes[16:]
    decrypted_bytes = bytearray()

    # Additive mixing done only once
    for j in range(len(subkeys)):
        subkey = subkeys[j]
        for i in range(len(subkey)):
            subkey[i] = (subkey[i] + S_BOX[(i + j) % len(S_BOX)]) % 256
        subkeys[j] = subkey

    for i, char in enumerate(encrypted_bytes):
        round_key = subkeys[i % num_rounds]
        decrypted_char = char
        for byte in round_key:
            decrypted_char ^= byte
        decrypted_bytes.append(decrypted_char)

    return decrypted_bytes.decode('utf-8')

def generate_key_hex():
    key = ''.join(random.choice('0123456789ABCDEF') for _ in range(128))
    return key



key = generate_key_hex()
input_data = "cu"
output = encrypt(input_data, key)
decrypted = decrypt(output, key)
print(key)
print(output)
print(decrypted)