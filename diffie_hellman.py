#!/usr/bin/env python3
import secrets
import hashlib
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
"""
class DiffieHellman:
    def __init__(self, sock):
        #sock - socket to send and recv over
        p = get_prime()
        multi_group = [x for x in range(1, p)]

        #find primitive value g

    def _get_prime(self):
        pass

def main():
    print(secrets.randbits(512))

if __name__ == '__main__':
    main()
