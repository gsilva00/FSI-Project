# CTF 9 - Week 12 - RSA

## Introduction

In this CTF challenge, we were given a [Python script](/files/CTF12/gen_example.py) (with some missing functions) generates the [cryptogram given to us](CTF12_L12G02.cph), This cryptogram contains the public exponent, the modulus, and an encrypted excerpt that contains the flag. The goal is to extract the flag from the cryptogram.

The missing functions for the RSA encryption of a message, we need to implement:

- `getRandomPrime()` - to find `p` and `q` starting on the given value (given the ambiguity of the guidelines, it might be necessary to search for numbers before the given value). Also according to the guidelines: "p is a prime around `2^(500+offset)` and q is a prime around `2^(501+offset)`", where the `offset` is `(((t-1)*10 + g) // 2)`, with `t` being our class number `12`, and `g` being our group number `2`. For each prime candidate, we check its validity using the `isPrime` function, which is analyzed in the next section.

```python
def getRandomPrime(exp):
  candidate = 2**exp

  while not isPrime(candidate):
    candidate += 1

  return candidate
```

- `extendedEuclidean()` - to find the modular inverse of `e` and `phi`. Given that the Extended Euclidean Algorithm is used to find the greatest common divisor of two numbers, as well as the coefficients of Bézout's identity, and in our opinion that responsibility is separate from the modular inverse calculation, we will implement a separate function for the modular inverse `modInv()`, which calls the `extendedEuclidean()` function:

```python
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
```

## Task 1 - Implementing a Primality Test

As per the guidelines, to test the primality of a number, we can use the Miller-Rabin primality test. The implementation of this function is based on the pseudocode in the [Wikipedia page](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Miller%E2%80%93Rabin_test):

```python
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
    for _ in range(s):
      y = pow(x, 2, n)
      if y == 1 and x != 1 and x != n-1:
        return False
      x = y
      if y != 1:
        return False
  return True
```

> Note 1: 3 is included as a base case because it is adjacent to 2 and also a prime, so there is no need to perform the whole algorithm to find such a simple prime. Beyond that, the primes stop being adjacent, and listing more would be unnecessary work. The same goes for the even numbers, as they are not prime by definition, so we can return False. Exhaustively listing all the divisors of a number does not make sense for the same reason (numbers are infinite). In the same vein, as a work around, using a `for` loop to check all the numbers up to the square root of `n' would be extremely inefficient, due to the large size of the primes used in this context (RSA).
>
> Note 2: As this is a probabilistic algorithm, the larger the number of rounds `k`, the more accurate the result. The default value of `k` is set to 30, which is a good balance between accuracy and performance, as a higher value would also increase the number of iterations in the loop.

## Task 2 - Implementing RSA

In the given [gen_example.py](/files/CTF12/gen_example.py) script, the implementation of the encryption of the plaintext, including all the necessary parameters associated with it is present, but the decryption function is missing. Therefore, we need to implement it - `decryptCipher()`:

```python
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
```

## Task 3

**Question 1:** How can I use the information I have to infer the values used in the RSA that encrypted the flag?

**Answer 1:** Given the public exponent `e` and the modulus `n`, we can try and infer the values of `p` and `q` by finding the prime factors of `n`. With the goal of discovering the value of `phi`, which is calculated using these primes, the difficulty lies in finding the correct values of these 2 primes, and that's why RSA is considered secure. As we're given the range of the primes for each number, there are way less computations that we need to perform to find the correct values. In fact, the brute-forcing of the primes in this CTF was made to be relatively easy, as we only needed to start from the given values and search 1105 numbers to find the correct values of `p` and `q`.

Once we have the primes, we can calculate the private exponent `d` using the modular inverse of `e` and `phi`, where `phi = (p-1)*(q-1)`. Finally, we can decrypt the ciphertext using the private exponent `d` and the modulus `n`, simply by using the `pow()` function, given how the RSA encryption and decryption work.

**Question 2:** How can I find out if my inference is correct?

**Answer 2:** We can verify if our inference is correct by decrypting the ciphertext using the calculated private exponent `d` and the modulus `n`. If the decryption is successful, we should be able to see the flag in the decrypted plaintext.

**Question 3:** Finally, how can I extract my key from the cryptogram I received?

**Answer 3:** By finding the substring that starts with `{` and ends with `}`. In this case, the whole decrypted plaintext is the flag - `flag{mubdidsmsqrllmkk}` - which we submitted in the CTF platform and completed the challenge:

![flag_after_bruteforce](/images/CTF12/brute_force_result.png)
