from binascii import hexlify
import random
import string


t = 12 # Número da turma
g = 2  # Número do grupo


# Returns True if n is probably prime, False if it's composite
def millerRabin(n, k=5):
    # Input #2: k, the number of rounds of testing to perform
    # Input #1: n > 2, an odd integer to be tested for primality
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(s-1):
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != n-1:
                return False
            x = y
        if x != 1:
            return False
    return True

def getRandomPrime(exp):
    candidate = 2**exp
    while not millerRabin(candidate):
        candidate += 1
    return candidate


def extendedEuclidean(a, b):
    print(f"Extended Euclidean Algorithm for {a} and {b}")
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q*r
        old_s, s = s, old_s - q*s
        old_t, t = t, old_t - q*t

    # Ensure gcd is positive
    if old_r < 0:
        old_r = -old_r
        old_s = -old_s
        old_t = -old_t

    return old_r, old_s, old_t

def modInv(a, b):
    print(f"Calculating modular inverse of e mod phi: {a} mod {b}")
    g, x, y = extendedEuclidean(a, b)
    if g != 1:
        print("ERROR!! gcd(e, phi) != 1")

    return x % b # returns d such that (d * e) % v == 1


def getParams(i, j):
    p = getRandomPrime(i) # Large prime number
    q = getRandomPrime(j) # Large prime number
    n = p*q
    phi = (p-1) * (q-1)   # Euler's totient function (phi(n) or v)
    e = 0x10001           # Public exponent
    d = modInv(e, phi)
    return (p, q, n, phi, e, d)

def enc(x, e, n):
    int_x = int.from_bytes(x, "little")
    y = pow(int_x,e,n)
    return y.to_bytes(256, 'little')

def addFlag(s, f):
    return s+"flag{"+f+"}"

def genFlag():
    return "".join([string.ascii_lowercase[random.randint(0,25)] for _ in range(16)])

def gen():
    file_name = f"CTF12_L{str(t).zfill(2)}G{str(g).zfill(2)}.cph"
    f = open(file_name, "w")
    fl = genFlag()
    m = addFlag("", fl)

    offset = ((t - 1) * 10 + g) // 2

    (p, q, n, phi, e, d) = getParams(500+offset, 500+1+offset)
    c = enc(m.encode(), e, n)

    f.write("Public exponent: "+str(e)+"\n")
    f.write("Modulus: "+str(n)+"\n")
    f.write(hexlify(c).decode())
    f.close()