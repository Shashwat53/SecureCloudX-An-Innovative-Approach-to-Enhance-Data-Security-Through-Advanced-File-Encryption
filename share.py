from __future__ import division
from __future__ import print_function
import random
import functools
from random import randrange, getrandbits
_PRIME = int(input("Enter the prime number: ")) #generate_prime_number()
_RINT = functools.partial(random.SystemRandom().randint, 0)
uni = 0
global dsar,dsas

def is_prime(n, k):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n%2 == 0:
        return False
    s = 0
    r=n-1
    while r & 1 == 0:
        s += 1
        r //= 2
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
    if x != 1 and x != n-1:
        j = 1
    while j < s and x != n-1:
        x = pow(x, 2, n)
    if x == 1:
        return False
    j = j+1
    if x != n-1:
        return False
    return True

def generate_prime_candidate(length):
    p=getrandbits(length)
    p |= (1 << length-1) | 1
    return p

def generate_prime_number(length=1024):
    p = 4
    while not is_prime(p, 80):
        p = generate_prime_candidate(length)
    return p

def keygen():
    def _eval_at(poly, x, prime):
        accum = 0
        for coeff in reversed(poly):
            accum *= x
            accum += coeff
            accum %= prime
        return accum

    def make_random_shares(minimum, shares, prime=_PRIME): #Generatesarandomshares.
        if minimum > shares:
            raise ValueError("pool secret would be irrecoverable")
        poly = [_RINT(prime) for i in range(minimum)]
        points = [(i, _eval_at(poly, i, prime)) for i in range(1,shares+1)]
        return poly[0], points

    def _extended_gcd(a,b):
        x = 0
        last_x = 1  
        y = 1
        last_y = 0  
        while b != 0:
            quot = a // b
            a, b = b, a % b
            x, last_x = last_x - quot * x, x
            y, last_y = last_y-quot*y, y
        return last_x, last_y

    def _divmod(num, den, p): # mod division
        inv, _ = _extended_gcd(den, p)
        return num * inv

    def _lagrange_interpolate(x, x_s, y_s, p): # Finding the Y value
        k = len(x_s)
        assert k == len(set(x_s)), "points must be distinct"

        def PI(vals):
            accum =1
            for v in vals:
                accum *= v
            return accum

        nums = []
        dens = []
        for i in range(k):
            others = list(x_s)
            cur = others.pop(i)

        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
        den = PI(dens)
        num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p) for i in range(k)])
        return (_divmod(num, den, p) + p) % p

    def recover_secret(shares, prime=_PRIME): #RecoveringtheKeyswithy,x
        if len(shares) < 2:
            raise ValueError("Need at least two shares.")
        x_s, y_s = zip(*shares)
        return _lagrange_interpolate(0, x_s, y_s, prime)

    def maingen(): # mainfunction
        n = int(input("Enter the minimum keys required: "))
        s=int(input("Enter the no.of shares required: "))
        uni = s
        secret, shares = make_random_shares(minimum=n, shares=s)
        print('Generated secret Code is:', secret)
        print('shares:', shares)
        return secret

    return maingen()

def secgen():
    def _extended_gcd(a, b):
        x = 0
        last_x = 1
        y = 1
        last_y =0
        while b != 0:
            quot = a // b
            a, b = b, a % b
            x, last_x = last_x - quot * x,x
            y, last_y = last_y-quot*y, y
        return last_x, last_y

    def _divmod(num, den, p): # mod division
        inv, _ = _extended_gcd(den, p)
        return num * inv

    def _lagrange_interpolate(x, x_s, y_s, p): # Finding the Y value
        k = len(x_s)
        assert k == len(set(x_s)),"points must be distinct"

        def PI(vals):
            accum = 1
            for v in vals:
                accum *= v
            return accum
        nums = []
        dens = []
        for i in range(k):
            others = list(x_s)
            cur = others.pop(i)
            nums.append(PI(x - o for o in others))
            dens.append(PI(cur - o for o in others))
        den = PI(dens)
        num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p) for i in range(k)])
        return (_divmod(num, den, p) + p) % p

    def recover_secret(shares, prime =_PRIME): #RecoveringtheKeyswithy,x
        if len(shares) < uni:
            print("Need at least two shares.")
        x_s, y_s = zip(*shares)
        return _lagrange_interpolate(0, x_s, y_s, prime)

    def mainsec():
        ns = int(input("Enter the no. of subset share keys u got: "))
        rs = []
        for i in range(ns):
            m = int(input("Enter the i value of the person: "))
            s = int(input("Enter his secret key: \t"))
            p = (m, s)
            rs.append(p)
        recoveredKey = recover_secret(rs[:ns])
        print('Secret recovered from subset of sharekey:',recoveredKey)
        return recoveredKey
    return mainsec()