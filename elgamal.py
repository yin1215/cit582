import random

from params import p
from params import g

def keygen():
    q = (p - 1) / 2
    a = random.randint(1, q)
    pk = pow(g, a, p)
    sk = a
    return pk,sk

def encrypt(pk,m):
    q = (p-1)/2
    r = random.randint(1,q)
    c1 = pow(g, r, p)
    c2 = (pow(pk, r, p) * m) % p
    return [c1,c2]

def decrypt(sk,c):
    c1 = c[0]
    c2 = c[1]
    m = ((c2 % p) * pow(c1, -sk, p)) % p
    return m