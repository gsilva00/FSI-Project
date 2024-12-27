from binascii import hexlify
import random
import string


t = 12 # Número da turma
g = 2  # Número do grupo


def extendedEuclidean(a, b):
    print(f"Extended Euclidean Algorithm for {a} and {b}")
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        print("------------------------------------------------")
        print(f"Iteration: {old_r}, {r}")
        print(f">> old_r: {old_r}, old_s: {old_s}, old_t: {old_t}")
        print(f">> r: {r}, s: {s}, t: {t}")
        q = old_r // r
        print(f">> Quotient: {q}")
        old_r, r = r, old_r - q*r
        old_s, s = s, old_s - q*s
        old_t, t = t, old_t - q*t
        print(f">> old_r: {old_r}, old_s: {old_s}, old_t: {old_t}")
        print(f">> r: {r}, s: {s}, t: {t}")

    # Ensure gcd is positive
    if old_r < 0:
        old_r = -old_r
        old_s = -old_s
        old_t = -old_t

    print()
    print(f"Bézout coefficients: {old_s}, {old_t}. That is: x,y such that a*x + b*y == g == gcd(a,b)")
    print(f"Greatest common divisor of {a} and {b}: {old_r}")
    print(f"Quotients: diving {a} by gcd == {t}; dividing {b} by gcd == {s}")
    print(f"Equation: {a} * {old_s} + {b} * {old_t} == {old_r}")
    print()
    print(f"The returns are: {old_r}, {old_s}, {old_t}")
    return old_r, old_s, old_t

def modInv(a, b):
    print(f"Calculating modular inverse of e mod phi: {a} mod {b}")
    g, x, y = extendedEuclidean(a, b)
    if g != 1:
        print("ERROR!! gcd(e, phi) != 1")

    print(f"Modular inverse of {a} mod {b} is {x % b}")
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