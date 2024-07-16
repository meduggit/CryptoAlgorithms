import os

def gen():
    return os.urandom(512)

def main():
    for i in range(1024):
        data = gen()
        with open('/home/medug/Documents/CryptoAlgorithms/Hashing/MHF/kks.txt', 'ab') as file:
            file.write(data)

main()