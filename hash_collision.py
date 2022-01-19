import hashlib
import os


def hash_collision(k):
    if not isinstance(k, int):
        print("hash_collision expects an integer")
        return (b'\x00', b'\x00')
    if k < 0:
        print("Specify a positive number of bits")
        return (b'\x00', b'\x00')

    # Collision finding code goes here
    x = os.urandom(64)
    y = os.urandom(64)

    if k == 0:
        return (x, y)

    sha_x = hashlib.sha256(x).hexdigest()
    bit_x = format(int(sha_x, 16), "0256b")
    sha_y = hashlib.sha256(y).hexdigest()
    bit_y = format(int(sha_y, 16), "0256b")

    while bit_x[-k:] != bit_y[-k:]:
        y = os.urandom(64)
        sha_y = hashlib.sha256(y).hexdigest()
        bit_y = format(int(sha_y, 16), "0256b")

    print(bit_x)
    print(bit_y)
    return (x, y)


hash_collision(4)

