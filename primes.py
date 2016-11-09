#!/usr/bin/env python3
from random import randint
import secrets
import time
import math

"""
A collection of functions used to generate primes involved in the
Diffie-Hellman key exchange protocol.
"""

"""
generate very large - 1000s of bits - prime numbers
:param l: lower bound
:param u: upper bound
:output p: random prime in range l...u
"""
def generate_large_prime(l, u):
    assert l > 2 and l <= u

    #max number of attemtps
    r = 100 * math.floor(math.log2(u) + 1)

    while True:
        r -= 1
        #change so an error is raised explaining what happend
        assert r > 0
        n = secrets.randbelow(u - l) + l
        if is_prime(n): break
    return n

"""
Uses the sieve of eratosthenes to generate a small list of primes, which
are used in the rabin miller test.
:param n: Limit on primes to generate, must satisfy 2 <= n <= 2**20
:output p: list of primes <= n
"""
#TOADD: optimize sieve of eratosthenes
def sieve_of_eratosthenes(n):
    assert n >=2 and n <= 2**20

    #generate and set flags for all numbers 2 to n to one
    flags = {x:1 for x in range(3, n + 1, 2) if x % 3 != 0}
    flags[2] = 1

    i = 3
    while i**2 <= n:
        #mark all multiples of i as composites, i.e set flags to zero
        for j in range(2, math.floor(n / i) + 1):
            flags[j * i] = 0

        i += 2
        while flags[i] != 1:
            i += 2

    primes = []
    for i in flags:
        if flags[i] == 1: primes.append(i)

    return primes

def is_prime(n):
    primes = sieve_of_eratosthenes(2**20)
    for i in primes:
        if n % i == 0:
            return i == n
    return rabin_miller(n)

"""
Uses rabin miller prime test to determine if a number
if prime or composite
:params n: number to check, n >= 3
:output p: boolean indicating whether prime or not
"""
def rabin_miller(n):
    assert n >= 3 and n % 2 != 0
    s = n - 1
    t = 0
    while s % 2 == 0:
        s //= 2
        t += 1

    k = 0
    while k < 128:
        #TODO: DONT USE PSEUDO-RANDOM NUMBER GENERATOR FOR CRYPTO!!!
        a = secrets.randbelow(n - 3) + 2
        v = pow(a, s, n)

        if v != 1:
            i = 0
            while v != n - 1:
                if i == t - 1:
                    return False
                else:
                    v = v**2 % n
                    i += 1
        k += 2
    return True

if __name__ == "__main__":
    x = time.time()
    print(generate_large_prime(2**9999, 2**10000))
    print(time.time() - x)
    #print(is_prime())
