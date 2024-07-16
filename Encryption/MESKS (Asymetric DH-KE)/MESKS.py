import params

def modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus

    while exponent > 0:
        if (exponent % 2) == 1:
            result = (result * base) % modulus

        exponent = exponent >> 1
        base = (base * base) % modulus

    return result

def enhanced_hash(input_str, process_rounds=1, mixing_rounds=2):
    rotation_amount = len(input_str) ** 2 % 32

    def input_whitening(data):
        return ''.join(format(ord(char), '08b') for char in data)

    def mixing(binary_data, rotation_amount, rounds):
        original = binary_data
        for _ in range(rounds):
            rotated = ((original << rotation_amount) | (original >> (32 - rotation_amount))) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            original ^= rotated
        return original

    def process_data(data):
        state = [0x87033a211350c9a5682e25cc2fafb24a, 0x3eda649a22357ed19ba54dea2f73d94c, 0x7edd261d1afd9717422c61f275ec2cb8, 0x37e81ad125b939805a672be0039c902e, 0x87aa2973de76e28905c6e181d6f0b8f2, 0x2d65153481ad91425f27f25899716593]

        for _ in range(process_rounds):
            for char in data:
                bit = int(char)
                mixed_data = mixing(bit, rotation_amount, mixing_rounds)
                state[0] = (state[0] + mixed_data + (state[1] ^ state[2] ^ state[3])) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                state[1] ^= (bit + state[0])
                state[2] = (state[1] << 7 | state[1] >> (32 - 7)) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                state[3] = (state[2] + (mixed_data * state[0]) + (state[5] ^ (bit >> 5) ^ (state[1] >> 3))) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                state[4] ^= (state[2] + bit)
                state[5] = (state[4] << 11 | state[3] >> (32 - 11)) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


        if rotation_amount < 16:    
            state[0], state[1], state[2], state[3], state[4], state[5] = state[3], state[2], state[1], state[0], state[5], state[4]
        else:
            state[0], state[1], state[2], state[3], state[4], state[5] = state[1], state[3], state[5], state[0], state[2], state[4]

        return state

    def combine_state_variables(state):
        state_integers = state
        result = (state_integers[0] ^ state_integers[1] ^ state_integers[2] ^ state_integers[3] ^ state_integers[5] ^ state_integers[4]) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        return hex(result)[2:].zfill(128)

    binary_data = input_whitening(input_str)
    processed_data = process_data(binary_data)
    combined_states = combine_state_variables(processed_data)

    return combined_states

private_key = params.private_key
print("---BEGIN PRIVATE KEY---\n",private_key,"\n---END PRIVATE KEY---\n")
public_mod = params.mod # Change the prime inside the 'params.py' file
print("---BEGIN PUBLIC MOD---\n",public_mod,"\n---END PUBLIC MOD---\n")
public_base = params.base # Change the base inside the 'params.py' file
print("---BEGIN PUBLIC BASE---\n",public_base,"\n---END PUBLIC BASE---\n")
public_key = modular_exponentiation(public_base, private_key, public_mod)
print("---BEGIN PUBLIC KEY---\n",public_key,"\n---END PUBLIC KEY---\n")
external_pub_key = int(input("Enter other person's key: "))
shared_key = modular_exponentiation(external_pub_key, private_key, public_mod)
print("---BEGIN SHARED KEY---\n",enhanced_hash(str(shared_key)),"\n---END SHARED KEY---\n")