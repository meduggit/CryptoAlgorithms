import os
import time
import Hash as h
import subprocess

usb_path = "/media/medug/MAIN/sign.txt"

sk = "0x937731"
ci = "123456789"
sn_c = "E0D55EA57425F7B0185A08DF"

def gsn(d):
    result = subprocess.run(
        ['lsblk', '-no', 'SERIAL', d],
        stdout=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()

def verify():
    with open(usb_path, 'r') as file_r:
        data = file_r.read().strip()

    sn = gsn("/dev/sdb")
    print(sn)

    hash_c = h.enhanced_hash(sk + ci + sn_c, salting=False, salt_param=None, process_rounds=1, mixing_rounds=2)
    hash_v = h.enhanced_hash(sk + data[:-33] + sn, salting=False, salt_param=None, process_rounds=1, mixing_rounds=2)
    if hash_c == hash_v:
        print("Authorized")

while True: 
    if os.path.exists(usb_path):
        verify()
        break
    time.sleep(1)