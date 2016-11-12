#!/usr/bin/env python3
from random import randint
import cProfile
import secrets
import time
import math

"""
A collection of functions used to generate primes involved in the
Diffie-Hellman key exchange protocol.
"""

"""
generate very large - 1000s of bits - prime numbers
:param l: lower bound in bits
:param u: upper bound in bits
:output p: random prime in range l...u

TOFIX: taking between 11s-15s to gen 2*2048 bit prime, find a way
       reduce the time to.
"""
#TODO: only generate safe primes which satisfy certain condtions,
#      so that the generator for Diffie Hellman can be secure and
#      2.
def generate_safe_prime(l, u):
    assert l > 1 and l <= u

    #generate 1 256-bit to be used for q
    #p = Nq + 1
    q = 0

    r = 100 * math.floor(math.log2(2**256) + 1)

    while True:
        assert r > 0
        r -= 1
        n = secrets.randbits(256)
        if is_prime(n):
            q = n
            break

    #generate prime p, p = Nq + 1
    p = 0
    while True:
        #TODO: CHANGE TO "CRYPTO SECURE" random number generator
        #TODO: Figure out how to calc n to get N-bit prime
        #currently returns a 2048-bit prime p.
        n = randint(2**1791, 2**1792)
        p = (n * q) + 1
        if is_prime(p): break
    return p
    #print(p)
    #print(math.floor(math.log2(p) + 1))

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
    flags = {x:1 for x in range(3, n + 1, 2)}
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
    #primes = sieve_of_eratosthenes(2**20)

    """x = 1000
    flags = {x:1 for x in range(3, x + 1, 2)}
    flags[2] = 1

    i = 3
    while i**2 <= x:
        #mark all multiples of i as composites, i.e set flags to zero
        for j in range(2, math.floor(x / i) + 1):
            flags[j * i] = 0

        i += 2
        while flags[i] != 1:
            i += 2

    for i in flags:
        if flags[i] == 1 and n % i == 0:
            return i == n"""
    primes = sieve_of_eratosthenes(1000)

    for i in primes:
        if n % i == 0:
            return i == n
    return rabin_miller(n)

"""
Uses rabin miller prime test to determine if a number
if prime or composite
:params n: number to check, n >= 3 and n mod n != 0
:output p: boolean indicating whether prime or not
"""
def rabin_miller(n):
    assert n >= 3 and n % 2 != 0
    s = n - 1
    t = 0
    while s % 2 == 0:
        s //= 2
        t += 1

    #K is the number of times that n is tested
    #the higher K is the less probalitity n has of
    #producing a false result as the prob of n
    #failing is 2**-k
    #crypto engin. book recommends k = 128
    k = 0
    while k < 128:
        a = secrets.randbelow(n - 3) + 2
        v = pow(a, s, n)

        if v != 1:
            i = 0
            while v != n - 1:
                if i == t - 1:
                    return False
                else:
                    v = v**2 % n
                    #v = pow(v, 2, n)
                    i += 1
        k += 2
    return True

if __name__ == "__main__":
    x = time.time()
    #print(sieve_of_eratosthenes(1000))
    print(generate_safe_prime(2**2047, 2**2048))
    print(time.time() - x)
