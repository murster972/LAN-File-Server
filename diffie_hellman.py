#!/usr/bin/env python3
import secrets
import hashlib
import primes
import os

"""
An implemantion of the Diffie-Hellman key exchange protocol
used to establish a key to use in AES encryption.

works as follows: a large prime p is used for the multiplicative
group mod p, g is a primtive value of said group. The server
the picks a value x from the multiplicative group mod p
and client picks value y from the multiplicative group mod p
server send client g**x and client sends server g**y
key = (g**x)**y == (g**y)**x

K should be hashed before being used by any other system, e.g. as a key in AES
"""
class DiffieHellman:
    def __init__(self, sock):
        self.sock = sock

    def gen_values(self):
        #sock - socket to send and recv over
        q, n, p = primes.generate_large_prime("test")

        while True:
            a = secrets.randbelow(p - 2) + 1
            g = pow(a, n, p)
            if g != 1 and pow(g, q, p) == 1:
                break

        #TODO: send generated values to sock

    def send_values(self):
        pass

    def receive_values(self):
        pass

    def _check_values(self):
        'checks that values receieved are valid'
        pass

if __name__ == '__main__':
    DiffieHellman()
