from binascii import hexlify
import random
import string


def getParams(i, j):
    p = getRandomPrime(i)
    q = getRandomPrime(j)
    n = p*q
    phi = (p-1) * (q-1)
    e = 0x10001
    d = extendedEuclidean(e, phi)
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
	f = open("LEICXGY.cph", "w")
	fl = genFlag()
	m = addFlag("", fl)

	(p, q, n, phi, e, d) = getParams(500+offset, 500+offset+1)
	c = enc(m.encode(), e, n)

	f.write("Public exponent: "+str(e)+"\n")
	f.write("Modulus: "+str(n)+"\n")
	f.write(hexlify(c).decode())
	f.close()