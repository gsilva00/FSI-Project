from binascii import hexlify, unhexlify
import random
import string


t = 12 # Número da turma
g = 2  # Número do grupo
offset = ((t - 1) * 10 + g) // 2
print(f"t: {t}, g: {g}, offset: {offset}")

# Miller-Rabin primality test
# Returns True if n is probably prime, False if it's composite
def isPrime(n, k=30):
    # Input #2: k, the number of rounds of testing to perform
    # Input #1: n, > 2, an odd integer to be tested for primality
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(s):
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != n-1:
                return False
            x = y
        if y != 1:
            return False
    return True

def getRandomPrime(exp):
    candidate = 2**exp

    while not isPrime(candidate):
        candidate += 1

    return candidate


def modInv(a, b):
    g, x, y = extendedEuclidean(a, b)
    if g != 1:
        print("ERROR!! gcd(e, phi) != 1")

    print(f"d is {x % b}")
    return x % b # returns d such that (d * e) % v == 1

def extendedEuclidean(a, b):
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

    print(f"old_r: {old_r}, old_s: {old_s}, old_t: {old_t}")
    return old_r, old_s, old_t


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

    (p, q, n, phi, e, d) = getParams(500+offset, 500+offset+1)
    c = enc(m.encode(), e, n)

    f.write("Public exponent: "+str(e)+"\n")
    f.write("Modulus: "+str(n)+"\n")
    f.write(hexlify(c).decode())
    f.close()


def decryptCipher():
    file_name = f"CTF12_L{str(t).zfill(2)}G{str(g).zfill(2)}.cph"
    with open(file_name, "r") as f:
        lines = f.readlines()
        e = int(lines[0].split(": ")[1])
        n = int(lines[1].split(": ")[1])
        ciphertext_hex = lines[2].strip()

    print("Public exponent:", e)
    print("Modulus:", n)

    ciphertext = unhexlify(ciphertext_hex)
    p, q = find_primes(n)
    phi = (p-1)*(q-1)
    d = modInv(e, phi)

    plaintext_bytes = decrypt_rsa(ciphertext, d, n)
    plaintext = plaintext_bytes.decode()
    print("Decrypted plaintext:", plaintext)

    flag_start = plaintext.find('{')
    flag_end = plaintext.find('}') + 1
    if flag_start != -1 and flag_end != -1:
        flag = plaintext[flag_start:flag_end]
        print("Decrypted flag:", flag)
    else:
        print("Flag not found in decrypted plaintext")

    print("Decrypted plaintext:", plaintext)

def find_primes(n):
    p_start = 2**(500 + offset)

    for candidate_p in range(p_start, p_start+100000):
        if isPrime(candidate_p) and n % candidate_p == 0:
            candidate_q = n // candidate_p
            if isPrime(candidate_q):
                print(f"Found p: {candidate_p}, q: {candidate_q}")
                return candidate_p, candidate_q
    print(f"Primes not found for n: {n}")
    return None, None

def decrypt_rsa(ciphertext, d, n):
    ciphertext_int = int.from_bytes(ciphertext, "little")
    p_int = pow(ciphertext_int, d, n)
    return p_int.to_bytes((p_int.bit_length() + 7) // 8, 'little')

decryptCipher()