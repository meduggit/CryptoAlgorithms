import threading
import random
import string

######################################################
################### CODE HERE ########################
######################################################

def enhanced_hash(data, process_rounds=4, mixing_rounds=2):
    state = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]

    rotation_amount = len(data)

    def mixing(binary_data, rotation_amount, rounds):
        for _ in range(rounds):
            binary_data = binary_data[-rotation_amount:] + binary_data[:-rotation_amount]
            binary_data = ''.join('1' if a != b else '0' for a, b in zip(binary_data, binary_data))
        return int(binary_data, 2)

    def rotation(x, amount):
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFFF

    def process_data(data):
        nonlocal state

        for _ in range(process_rounds):
            for byte in data.encode():
                state[0] = (state[0] + byte + (state[1] ^ state[2] ^ state[3])) & 0xFFFFFFFFF
                state[1] = rotation((state[1] ^ (byte + state[0])), 7)
                state[2] = (state[2] + (byte * state[0]) + (state[3] ^ (state[1] >> 3))) & 0xFFFFFFFFF
                state[3] = rotation((state[3] ^ (state[2] >> 2) + byte), 11)

                binary_data = int(''.join(format(byte, '08b') for byte in data.encode()), 2)
                binary_data = mixing(bin(binary_data)[2:], rotation_amount, mixing_rounds)

                state[0], state[1], state[2], state[3] = state[3], state[2], state[1], state[0]

    def combine_state_variables():
        return hex((state[0] ^ state[1] ^ state[2] ^ state[3]) & 0xFFFFFFFFF)[2:].zfill(9)

    process_data(data)

    return combine_state_variables()

######################################################
################### COLLISION HERE ###################
######################################################



class CollisionFinder:
    def __init__(self):
        self.seen_hashes = {}
        self.lock = threading.Lock()
        self.collision_found = False

    def find_collision(self):
        # First, try all numbers from 1 to 10000
        for number in range(1, 10001):
            if self.collision_found:
                return
            input_data = str(number)
            hashed_hex = enhanced_hash(input_data)
            if self.check_collision(input_data, hashed_hex):
                return

        # After that, continue with random strings and numbers
        while not self.collision_found:
            input_data = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 20)))
            hashed_hex = enhanced_hash(input_data)
            if self.check_collision(input_data, hashed_hex):
                return

    def check_collision(self, input_data, hashed_hex):
        with self.lock:
            if hashed_hex in self.seen_hashes:
                if self.seen_hashes[hashed_hex] != input_data:
                    print("Collision found for hash:", hashed_hex)
                    print("Inputs:")
                    print(self.seen_hashes[hashed_hex])
                    print(input_data)
                    self.collision_found = True
                    return True
            else:
                self.seen_hashes[hashed_hex] = input_data
                print("Tried:", input_data, "Hash:", hashed_hex)
        return False

def main(num_threads=2):
    finder = CollisionFinder()
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=finder.find_collision)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
