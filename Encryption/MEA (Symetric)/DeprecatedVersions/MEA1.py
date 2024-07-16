import random
import base64

# Function to generate a random key of specified length
def KeyGenerationFunction(length):
    return base64.b64encode(bytes(random.randint(0, 255) for _ in range(length))).decode('utf-8')

# Function to encrypt a message using a key
def EncryptionFunction(message, key):
    key_bytes = base64.b64decode(key.encode('utf-8'))
    encrypted_message = b''
    key_length = len(key_bytes)
    block_size = 2  # Dividing message into blocks of size 2
    blocks = [message[i:i+block_size] for i in range(0, len(message), block_size)]
    for block in blocks:
        block_encrypted = b''
        for i in range(len(block)):
            key_index = i % key_length
            encrypted_char = (ord(block[i]) + key_bytes[key_index]) % 256
            block_encrypted += bytes([encrypted_char])
        encrypted_message += block_encrypted
    return base64.b64encode(encrypted_message).decode('utf-8')

# Function to decrypt a message using the same key
def DecryptionFunction(encrypted_message, key):
    key_bytes = base64.b64decode(key.encode('utf-8'))
    decrypted_message = b''
    key_length = len(key_bytes)
    encrypted_message_bytes = base64.b64decode(encrypted_message.encode('utf-8'))
    block_size = 2  # Dividing message into blocks of size 2
    blocks = [encrypted_message_bytes[i:i+block_size] for i in range(0, len(encrypted_message_bytes), block_size)]
    for block in blocks:
        block_decrypted = b''
        for i in range(len(block)):
            key_index = i % key_length
            decrypted_char = (block[i] - key_bytes[key_index]) % 256
            block_decrypted += bytes([decrypted_char])
        decrypted_message += block_decrypted
    return decrypted_message.decode('utf-8')

#Generates a key
key = KeyGenerationFunction(64)
test_str = "Hello!"
encrypted = EncryptionFunction(test_str, "7BgiW3H0Qfjnb+4akuYTl7yHt+rIi4/SZixpQfk4RBPOChX/Nv6rYa2+5Fahy+qG2vj2D1b0RXlUtDOxyxGXNA==")
decrypted = DecryptionFunction(encrypted, "7BgiW3H0Qfjnb+4akuYTl7yHt+rIi4/SZixpQfk4RBPOChX/Nv6rYa2+5Fahy+qG2vj2D1b0RXlUtDOxyxGXNA==")
print(key)
print(encrypted)
print(decrypted)

