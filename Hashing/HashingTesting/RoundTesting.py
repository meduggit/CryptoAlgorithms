import time
import statistics
from collections import Counter
import math

def enhanced_hash(input_str, process_rounds=1, mixing_rounds=2):
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

def test_hash_function():
    input_str = "test_input"
    max_rounds = 10
    performance_results = []

    for process_rounds in range(1, max_rounds + 1):
        for mixing_rounds in range(1, max_rounds + 1):
            # Performance test
            start_time = time.time()
            for _ in range(100):  # Repeat to get a more stable time measurement
                enhanced_hash(input_str, process_rounds, mixing_rounds)
            end_time = time.time()
            avg_time = (end_time - start_time) / 100

            # Strength test
            hash_results = [enhanced_hash(input_str + str(i), process_rounds, mixing_rounds) for i in range(100)]
            unique_hashes = len(set(hash_results))
            stdev_hash_counts = statistics.stdev(Counter(hash_results).values())
            entropy = -sum(freq/100 * math.log2(freq/100) for freq in Counter(hash_results).values())

            performance_results.append((process_rounds, mixing_rounds, avg_time, unique_hashes, stdev_hash_counts, entropy))

    # Print performance and strength results
    print("Results (process_rounds, mixing_rounds, avg_time, unique_hashes, stdev_hash_counts, entropy):")
    for result in performance_results:
        print(result)

    # Find the optimal configuration for performance
    optimal_performance_config = min(performance_results, key=lambda x: x[2])
    print("\nOptimal Configuration for Performance:")
    print(optimal_performance_config)

    # Find the optimal configuration for strength (max unique_hashes and min stdev_hash_counts and max entropy)
    optimal_strength_config = max(performance_results, key=lambda x: (x[3], -x[4], x[5]))
    print("\nOptimal Configuration for Strength:")
    print(optimal_strength_config)

# Run the test
test_hash_function()
