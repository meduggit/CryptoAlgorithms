#Hashing Function Version 5
#Copyright (C) 2024 meduggit

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import time

start_time = time.time()

version = "MHF5-SF"

def enhanced_hash(input_str, salting=False, salt_param=None, process_rounds=1, mixing_rounds=1):
        
    rotation_amount = len(input_str) ** 2 % 32

    def generate_salt():
        salt = os.urandom(16).hex()
        return salt

    def input_whitening(data):
        return ''.join(format(ord(char), '08b') for char in data)

    def output_whitening(output, salt):
        hash_output = f"#{version}#h={output}#s={salt}#"
        return hash_output

    def mixing(binary_data, rotation_amount, rounds):
        original = binary_data
        for _ in range(rounds):
            rotated = ((original << rotation_amount) | (original >> (32 - rotation_amount))) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            original ^= rotated

        return original

    def process_data(data):
        state = [0x87033a211350c9a5682e25cc2fafb24a, 0x3eda649a22357ed19ba54dea2f73d94c,
                 0x7edd261d1afd9717422c61f275ec2cb8, 0x37e81ad125b939805a672be0039c902e,
                 0x87aa2973de76e28905c6e181d6f0b8f2, 0x2d65153481ad91425f27f25899716593]

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

    if salting == True and salt_param == None:
        salt_param = generate_salt()
    
    if salting == True:
        binary_data = input_whitening(input_str + salt_param)
    else:
        binary_data = input_whitening(input_str)

    processed_data = process_data(binary_data)
    combined_states = combine_state_variables(processed_data)

    output = output_whitening(combined_states, salt_param)
    
    return output

# Test Setup
print(enhanced_hash("91231331232131", salting=False, salt_param=None, process_rounds=1, mixing_rounds=2)) #1:2 or 120:350

end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")