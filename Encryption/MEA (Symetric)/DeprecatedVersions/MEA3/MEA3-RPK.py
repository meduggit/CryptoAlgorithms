import binascii
import os
import time

import SBox

start_time = time.time()

version = "MEA3-RPK"

def check():
    return print(f"{version} started")

def derive_subkeys(main_key):
    if len(main_key) != 128:
        raise ValueError("Main key must be 128 hex characters (512 bits) long.")
    subkeys = []
    for i in range(16):
        sk1 = int(main_key[i*8:i*8+2], 16)
        sk2 = int(main_key[i*8+2:i*8+4], 16)    
        sk3 = int(main_key[i*8+4:i*8+6], 16)
        sk4 = int(main_key[i*8+6:i*8+8], 16)
        subkeys.append((sk1, sk2, sk3, sk4))
    return subkeys

def plaintext_to_bytes(plaintext):
    hex_data = binascii.hexlify(plaintext.encode('utf-8')).decode('utf-8')
    return bytearray.fromhex(hex_data)

def generate_iv(length=16):
    return bytearray(os.urandom(length))

def add_iv(data, iv):
    return iv + data

def apply_sbox(data):
    return bytearray(SBox.S_BOX[b] for b in data)

def apply_inverse_sbox(data):
    inv_sbox = {v: k for k, v in enumerate(SBox.S_BOX)}
    return bytearray(inv_sbox[b] for b in data)

def rotate_right(data, count):
    return data[-count:] + data[:-count]

def encryption_round(data, subkeys):
    sk1, sk2, sk3, sk4 = subkeys
    shifted_data = bytearray((b + sk1) % 256 for b in data)
    xor_data1 = bytearray(b ^ sk2 for b in shifted_data)
    rotated_data = rotate_right(xor_data1, sk3)
    xor_data2 = bytearray(b ^ sk4 for b in rotated_data)
    return xor_data2

def decryption_round(data, subkeys):
    sk1, sk2, sk3, sk4 = subkeys
    xor_data1 = bytearray(b ^ sk4 for b in data)
    rotated_data = rotate_right(xor_data1, -sk3)  # Use negative count for decryption
    xor_data2 = bytearray(b ^ sk2 for b in rotated_data)
    shifted_data = bytearray((b - sk1) % 256 for b in xor_data2)
    return shifted_data

def encrypt(plaintext, main_key, rounds=1):
    data = plaintext_to_bytes(plaintext)
    iv = generate_iv()  # Generate a random IV
    data = apply_sbox(data)
    subkeys = derive_subkeys(main_key)
    data_with_iv = add_iv(data, iv)  # Prepend IV to data
    for i in range(rounds):
        round_key = subkeys[i % len(subkeys)]
        data_with_iv = encryption_round(data_with_iv, round_key)
    return iv.hex() + data_with_iv.hex()  # Return IV + encrypted data

def decrypt(ciphertext, main_key, rounds=1):
    iv = bytearray.fromhex(ciphertext[:32])  # Extract IV
    data = bytearray.fromhex(ciphertext[32:])
    subkeys = derive_subkeys(main_key)
    
    for i in range(rounds - 1, -1, -1):
        round_key = subkeys[i % len(subkeys)]
        data = decryption_round(data, round_key)
        
    data = apply_inverse_sbox(data)
    
    decrypted_data = data[16:]
    
    return decrypted_data.decode('utf-8')

def generate_key_hex():
    return os.urandom(64).hex()

#Test setup 
key = "78246aa96a9466aae5756b2495aebaf13fa523166ebf051071faffaeb8edae41327d877757332a144cc6237cc7227b972e2384b8a4ef03b5f86189c84ca5b951"
input_data = "The quick brown fox jumps over the lazy dog // Արագ շագանակագույն աղվեսը ցատկում է ծույլ շան վրայով"
encrypted = encrypt(input_data, key)
decrypted = decrypt(encrypted, key)
print("Key:" ,key)
print("Encrypted" , encrypted)
print("Decrypted", decrypted)

end_time = time.time()
execution_time = end_time - start_time

print(execution_time)


0x8e87f51c75fd5397e37c57e708b9391e#b55960aac759b9b9598fa7ce617b977b4a597b267b977b4a7b977b1b7b977b437b977b4a7bb3ce2d7b8a7b1b597b977b517b3e7bbd7bf17bc459cede7b977b747b437bb3ce2d7b7a597b73597b467bb3ce2d7b8a7bdb597b267b977b1b597b3ece617b977b8a7bb37b3e#8b72e01960f84682d67942d20dbc3c1b3fd44959452c6b95b7595412aa9cd2593baa9659d72c9ee8a459aab449125989d4495964a92f
0x069dd97fdf6550ff591e3a9b2bad7cc0#b55960aac759b9b9598fa7ce617b977b4a597b267b977b4a7b977b1b7b977b437b977b4a7bb3ce2d7b8a7b1b597b977b517b3e7bbd7bf17bc459cede7b977b747b437bb3ce2d7b7a597b73597b467bb3ce2d7b8a7bdb597b267b977b1b597b3ece617b977b8a7bb37b3e#f398dc7ada5045fa5c1b3f9e2ea879b53fd44959452c6b95b7595412aa9cd2593baa9659d72c9ee8a459aab449125989d4495964a92f