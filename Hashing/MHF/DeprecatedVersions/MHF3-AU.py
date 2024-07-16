import threading
import random
import string

def MHF3_AU(plaintext):

    state_a = 0x67452301
    state_b = 0xEFCDAB89
    state_c = 0x98BADCFE
    state_d = 0x10325476

    def left_rotate(x, amount):
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFFF

    for byte in plaintext.encode():
        
        state_a = (state_a + byte + (state_b ^ state_c ^ state_d)) & 0xFFFFFFFFF
        
        state_b = left_rotate((state_b ^ (byte + state_a)), 7)
        
        state_c = (state_c + (byte * state_a) + (state_d ^ (state_b >> 3))) & 0xFFFFFFFFF
        
        state_d = left_rotate((state_d ^ (state_c >> 2) + byte), 11)

        state_a = left_rotate(state_a, 3)

        state_b = (state_b + state_a - state_c) & 0xFFFFFFFFF

        state_c = left_rotate(state_c, 5)

        state_d = (state_d + state_b ^ state_a) & 0xFFFFFFFFF

        state_a, state_b, state_c, state_d = state_d, state_c, state_b, state_a

    final_value = (state_a ^ state_b ^ state_c ^ state_d) & 0xFFFFFFFFF

    final_hex = hex(final_value)[2:].zfill(9)

    return final_hex

def kdf(input_data, key_length=64):
    derived_key = ''
    counter = 0

    while len(derived_key) < key_length * 2:
        counter_str = str(counter)
        counter += 1
        hash_input = input_data + counter_str
        derived_key += MHF3_AU(hash_input)
    
    return derived_key[:key_length * 2]
    
    
print(MHF3_AU("hello"))
