import math
#from primes import primes
###############################################################################
# Chapter 3 - Primes
###############################################################################
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
          61, 67, 71, 73, 79, 83, 89, 97]

def check_primelist(n):
    if n > primes[-1]:
        return False

    for p in primes:
        if n == p:
            return True
        if n < p:
            return False
    return False

def is_prime(n):
    # Short circuits to try and optimize a bit based on dynamic computing
    if check_primelist(n):
        return True

    if n < primes[-1]:
        return False

    for ii in range(2, math.ceil(math.sqrt(n))+1):
        if n % ii == 0:
            return False

    return True

def all_primes(n):
    _primes = primes[:]
    for ii in range(_primes[-1], n):
        if is_prime(ii):
            _primes.append(ii)
    return _primes

def p_factors(n):
    for ii in range(1, n):
        if n % ii == 0:
            print(ii)

factors = lambda n: [ii for ii in range(1, n) if (n % ii) == 0]

def prime_power(n, p):
    """ returns a tuple of (p|n, if p|n -> k)
    """
    divides = (n % p) == 0
    if not divides:
        return (False, None)
    k = 1
    while (n % p**k) == 0:
        k += 1
    return (True, k-1)

def prime_factors(n, _primes=None):
    if not _primes:
        _primes = primes

    factors = []
    for p in _primes:
        if p > n:
            break

        r = prime_power(n, p)
        if r[0]:
            factors.append((p, r[1]))
    return factors

def pprime_factors(n, _primes=None):
    factors = prime_factors(n, _primes=_primes)
    return " * ".join(["{}^{}".format(p, k) for (p, k) in factors])


###############################################################################
#   Chapter 6 - Fermat's Litte Theorem
###############################################################################
def phi(n, P=100000):
    """
    This implementation is using this function:
    φ(n) = φ(p1 ^ a1) ··· φ(pk ^ ak) = (p1 ^ (a1-1))(p1-1)) ··· (pk ^ (ak-1))(pk-1))
    """
    _primes = all_primes(P)
    factors = prime_factors(n, _primes=_primes)
    product = 1
    for p, k in factors:
        product *= (p**(k-1)) * (p - 1)

    return product


###############################################################################
#   Chapter 7 - Number-Theoretic Functions
###############################################################################

def tau(n):
    pass

def sigma(n, _print=False):
    s1 = lambda n, k: ( (n**(k+1) - 1) / (n-1))
    product = 1
    ppp = ""
    for prime, power in prime_factors(n, _primes=all_primes(n)):
        product *= s1(prime, power) 
        ppp += "(({}^{} - 1) / {})".format(prime, power+1, prime-1)

    if _print:
        print(ppp)

    return product

###############################################################################
#   Chapter 8 - Introduction to Cryptography
###############################################################################
import string
mapping = {l:str(i).rjust(2, '0') for i, l in enumerate(string.ascii_uppercase)}
reverse_mapping = {str(i).rjust(2, '0'):l for i, l in enumerate(string.ascii_uppercase)}

def encode(word):
    out = []
    for l in word.upper():
        out.append(mapping[l] if l != ' ' else ' ')
    return out

def decode(encoded):
    out = []
    for l in encoded:
        out.append(reverse_mapping[l] if l != ' ' else ' ')
    return out

def caesar_cipher(encoded, encrypt=True):
    out = []
    mod = +3 if encrypt else -3

    for c in encoded:
        if not c.strip():
            out.append(' ')
        else:
            out.append(str((int(c) + mod) % 26).rjust(2, '0'))

    return out

def affine_cipher(encoded, a, b, encrypt=True):
    out = []

    for c in encoded:
        if not c.strip():
            out.append(' ')
        else:
            out.append(str((a * int(c) + b) % 26).rjust(2, '0'))

    return out


def RSA(encoded, e, n, N, encrypt=True):
    out = ""
    encoded = [char for string in encoded for char in string]

    block = ""
    for c in encoded:
        if not c.strip():
            out+= ' '
            continue

        elif len(block) == N:
            out += (str((int(block)**e) % n).rjust(2, '0'))
            block = ""

        block += c

    if block:
        out += (str((int(block)**e) % n).rjust(2, '0'))

    _out = []
    s = ""
    for c in out:
        if not c.strip():
            _out.append(' ')
            continue
        if int(s + c) >= 26 or len(s + c) > 2:
            _out.append(s.rjust(2, '0'))
            s = ""
        s += c
    if s:
        _out.append(s.rjust(2, '0'))


    return _out
