import time
import random
import string

######################################################
################### CODE HERE ########################
######################################################

def enhanced_hash(input_str, process_rounds=1, mixing_rounds=4):
    rotation_amount = len(input_str) ** 2 % 32

    def input_whitening(data):
        return ''.join(format(ord(char), '08b') for char in data)

    def mixing(binary_data, rotation_amount, rounds):
        original = binary_data
        for _ in range(rounds):
            rotated = ((original << rotation_amount) | (original >> (32 - rotation_amount))) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            original ^= rotated
        return original

    def process_data(data):
        state = [0x87033a211350c9a5682e25cc2fafb24a, 0x3eda649a22357ed19ba54dea2f73d94c, 0x7edd261d1afd9717422c61f275ec2cb8, 0x37e81ad125b939805a672be0039c902e, 0x87aa2973de76e28905c6e181d6f0b8f2, 0x2d65153481ad91425f27f25899716593]

        for _ in range(process_rounds):
            for char in data:
                bit = int(char)
                mixed_data = mixing(bit, rotation_amount, mixing_rounds)
                state[0] = (state[0] + mixed_data + (state[1] ^ state[2] ^ state[3])) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                state[1] ^= (bit + state[0])
                state[2] = (state[1] << 7 | state[1] >> (32 - 7)) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                state[3] = (state[2] + (mixed_data * state[0]) + (state[5] ^ (bit >> 5) ^ (state[1] >> 3))) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                state[4] ^= (state[2] + bit)
                state[5] = (state[4] << 11 | state[3] >> (32 - 11)) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


        if rotation_amount < 16:
            state[0], state[1], state[2], state[3], state[4], state[5] = state[3], state[2], state[1], state[0], state[5], state[4]
        else:
            state[0], state[1], state[2], state[3], state[4], state[5] = state[1], state[3], state[5], state[0], state[2], state[4]

        return state

    def combine_state_variables(state):
        state_integers = state
        result = (state_integers[0] ^ state_integers[1] ^ state_integers[2] ^ state_integers[3] ^ state_integers[5] ^ state_integers[4]) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        return hex(result)[2:].zfill(18)

    binary_data = input_whitening(input_str)
    processed_data = process_data(binary_data)
    combined_states = combine_state_variables(processed_data)

    return combined_states

#######################################################
################### PERFOMANCE HERE ###################
#######################################################

def test_hash_performance(hash_function, data_sizes, num_trials):
    results = {}
    
    for size in data_sizes:
        total_time = 0
        for _ in range(num_trials):
            data = ''.join(random.choices(string.ascii_letters + string.digits, k=size))
            start_time = time.time()
            hash_function(data)
            end_time = time.time()
            total_time += end_time - start_time
        
        avg_time = total_time / num_trials
        results[size] = avg_time

    return results

# Example usage:
data_sizes = [10, 100, 1000]  # Varying sizes of data to test
num_trials = 1  # Number of trials for each data size
performance_results = test_hash_performance(enhanced_hash, data_sizes, num_trials)
print(f"Performance Results: ")
for size, avg_time in performance_results.items():
    print(f"Data Size: {size}, Average Time: {avg_time} seconds")