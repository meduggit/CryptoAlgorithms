import os

def expo_gen():
    expo = os.urandom(512).hex()
    return int(expo, 16)

print(expo_gen())