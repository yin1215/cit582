import hashlib
import os

def hash_preimage(target_string):
    if not all( [x in '01' for x in target_string ] ):
        print( "Input should be a string of bits" )
        return
    #nonce = b'\x00'
    l = len(target_string)
    if l>256:
        print("Input is too long")
        return

    nonce = os.urandom(64)
    if l == 0:
        return nonce

    sha_x = hashlib.sha256(nonce).hexdigest()
    bit_x = format(int(sha_x, 16), "0256b")

    while bit_x[-l:] != target_string:
        nonce = os.urandom(64)
        sha_x = hashlib.sha256(nonce).hexdigest()
        bit_x = format(int(sha_x, 16), "0256b")

    return( nonce )