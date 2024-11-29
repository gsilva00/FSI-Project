# SEED Labs Tasks for _Secret Key Encryption_

## (Work done in Week #9)

## Task 1: Frequency Analysis

In this week's first task, we will perform frequency analysis on a ciphertext to decipher it. The ciphertext was generated using a monoalphabetic substitution cipher, which is a type of substitution cipher where each letter in an alphabet is mapped to a single letter in the ciphertext alphabet.

First, we need to analyze the frequency of the n-grams in the [ciphertext](/files/LOGBOOK9/TASK1/ciphertext.txt). We will use the [freq.py](/files/LOGBOOK9/TASK1/freq.py) script to do this. It was slightly altered to include the percentages after the frequency of each n-gram, to make it easier to analyze the results and compare them to the English language (altered/added lines are marked with a comment starting with `# !`).

```bash
./freq.py
# Output:
-------------------------------------
1-gram (top 20):
n: 488 (12.41%)
y: 373 (9.49%)
v: 348 (8.85%)
x: 291 (7.40%)
u: 280 (7.12%)
q: 276 (7.02%)
m: 264 (6.72%)
h: 235 (5.98%)
t: 183 (4.66%)
i: 166 (4.22%)
p: 156 (3.97%)
a: 116 (2.95%)
c: 104 (2.65%)
z: 95 (2.42%)
l: 90 (2.29%)
g: 83 (2.11%)
b: 83 (2.11%)
r: 82 (2.09%)
e: 76 (1.93%)
d: 59 (1.50%)
-------------------------------------
2-gram (top 20):
yt: 115 (3.67%)
tn: 89 (2.84%)
mu: 74 (2.36%)
nh: 58 (1.85%)
vh: 57 (1.82%)
hn: 57 (1.82%)
vu: 56 (1.79%)
nq: 53 (1.69%)
xu: 52 (1.66%)
up: 46 (1.47%)
xh: 45 (1.44%)
yn: 44 (1.41%)
np: 44 (1.41%)
vy: 44 (1.41%)
nu: 42 (1.34%)
qy: 39 (1.25%)
vq: 33 (1.05%)
vi: 32 (1.02%)
gn: 32 (1.02%)
av: 31 (0.99%)
-------------------------------------
3-gram (top 20):
ytn: 78 (3.32%)
vup: 30 (1.28%)
mur: 20 (0.85%)
ynh: 18 (0.77%)
xzy: 16 (0.68%)
mxu: 14 (0.60%)
gnq: 14 (0.60%)
ytv: 13 (0.55%)
nqy: 13 (0.55%)
vii: 13 (0.55%)
bxh: 13 (0.55%)
lvq: 12 (0.51%)
nuy: 12 (0.51%)
vyn: 12 (0.51%)
uvy: 11 (0.47%)
lmu: 11 (0.47%)
nvh: 11 (0.47%)
cmu: 11 (0.47%)
tmq: 10 (0.43%)
vhp: 10 (0.43%)
```

### Analysis

To decipher the ciphertext, we'll exploit the vulnerability of monoalphabetic substitution ciphers to frequency analysis. We will compare the frequency of the n-grams in the ciphertext to the frequency of n-grams in the English language, and try to decipher the most common n-grams in the ciphertext.

#### English plaintext frequencies

##### Single letters

| Plaintext | Frequency |
| --------- | --------- |
| e         | 11.1607%  |
| a         | 8.4966%   |
| r         | 7.5809%   |
| i         | 7.5448%   |
| o         | 7.1635%   |
| t         | 6.9509%   |
| n         | 6.6544%   |
| s         | 5.7351%   |
| l         | 5.4893%   |
| c         | 4.5388%   |
| u         | 3.6308%   |
| d         | 3.3844%   |
| p         | 3.1671%   |
| m         | 3.0129%   |
| h         | 3.0034%   |
| g         | 2.4705%   |
| b         | 2.0720%   |
| f         | 1.8121%   |
| y         | 1.7779%   |
| w         | 1.2899%   |
| k         | 1.1016%   |
| v         | 1.0074%   |
| x         | 0.2902%   |
| z         | 0.2722%   |
| j         | 0.1965%   |
| q         | 0.1962%   |

[Source](https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html)

##### Bigrams

| Bigram | Frequency |
| ------ | --------- |
| th     | 3.56%     |
| he     | 3.07%     |
| in     | 2.43%     |
| er     | 2.05%     |
| an     | 1.99%     |
| re     | 1.85%     |
| on     | 1.76%     |
| at     | 1.49%     |
| en     | 1.45%     |
| nd     | 1.35%     |
| ti     | 1.34%     |
| es     | 1.34%     |
| or     | 1.28%     |
| te     | 1.20%     |
| of     | 1.17%     |
| ed     | 1.17%     |
| is     | 1.13%     |
| it     | 1.12%     |
| al     | 1.09%     |
| ar     | 1.07%     |
| st     | 1.05%     |
| to     | 1.05%     |
| nt     | 1.04%     |
| ng     | 0.95%     |
| se     | 0.93%     |
| ha     | 0.93%     |
| as     | 0.87%     |
| ou     | 0.87%     |
| io     | 0.83%     |
| le     | 0.83%     |
| ve     | 0.83%     |
| co     | 0.79%     |
| me     | 0.79%     |
| de     | 0.76%     |
| hi     | 0.76%     |
| ri     | 0.73%     |
| ro     | 0.73%     |
| ic     | 0.70%     |
| ne     | 0.69%     |
| ea     | 0.69%     |
| ra     | 0.69%     |
| ce     | 0.65%     |

[Source](https://en.wikipedia.org/wiki/Bigram)

##### Trigrams

| Trigram | Frequency |
| ------- | --------- |
| the     | 1.81%     |
| and     | 0.73%     |
| tha     | 0.33%     |
| ent     | 0.42%     |
| ing     | 0.72%     |
| ion     | 0.42%     |
| tio     | 0.31%     |
| for     | 0.34%     |
| nde     | 0.34%     |
| has     | 0.34%     |
| nce     | 0.34%     |
| edt     | 0.34%     |
| tis     | 0.34%     |
| oft     | 0.22%     |
| sth     | 0.21%     |
| men     | 0.21%     |

[Source](https://en.wikipedia.org/wiki/Trigram)

### Decryption

#### Try 1

- Highest frequency 1,2,3-grams in English:

  - `The` is the most common trigram by far
  - `Th` and `he` are the most common bigrams
  - `e` is the most common letter

- By analyzing the frequency of the ciphertext:
  - `ytn` is the most common trigram
  - `yt` and `tn` are the most common bigrams
  - `n` is the most common letter

The relationship between these `n-grams` is evident, as `the` word makes it easy to point out that `ytn` in the ciphertext is most likely `the` in the plaintext:

| Ciphertext | Plaintext |
| ---------- | --------- |
| ytn        | the       |
| yt         | th        |
| tn         | he        |
| n          | e         |

So, we executed the following command to decipher the first 3 letters of the ciphertext (the converted letters are in uppercase to make it easier to read):

```bash
tr ’ytn’ ’THE’ < ciphertext.txt > plaintext.txt
```

And our analysis seems to be correct, due to `THE` being at the start of most sentences in the ciphertext.

Therefore we deciphered the first 3 letters of the ciphertext:

| Ciphertext | Plaintext |
| ---------- | --------- |
| y          | T         |
| t          | H         |
| n          | E         |

The result can be seen [here](/files/LOGBOOK9/TASK1/plaintext_try1.txt).

#### Try 2

`and` is the second most common trigram in English.

From the most used letters not yet deciphered in the ciphertext:

- `v` is the most common letter
- `vu` and `up` are common bigrams (even though not the most common, because `mu` is the most common bigram)
- `vup` is the most common trigram.

These facts correlate to the frequency of `an` and `and` (the next most common bigram and trigram in English). The fact that `a` and `i` are vowels - as well as very common letters - that pair with `n` in common words, makes it likely that `u` in the ciphertext is `n` in the plaintext, if we assume that `v` is `a` and `m` is `i`.

So we tried:

```bash
tr ’ytnvup’ ’THEAND’ < ciphertext.txt > plaintext.txt
```

> Note: The already deciphered letters need to be added to the command, so that the file maintains the previous deciphered letters.

This seems to be correct, as the deciphered `AND` appears to be correctly placed in the plaintext, sometimes being followed by `THE` or the indefinite article `A`.

The result can be seen [here](/files/LOGBOOK9/TASK1/plaintext_try2_vupAND.txt).

---

Then we tried:

```bash
tr ’ytnvupm’ ’THEANDI’ < ciphertext.txt > plaintext.txt
```

Which also seems to be correct, due to all full words in uppercase making sense when together and in their position in the plaintext.

The result can be seen [here](/files/LOGBOOK9/TASK1/plaintext_try2_mI.txt).

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| y          | T         |
| t          | H         |
| n          | E         |
| v          | A         |
| u          | N         |
| p          | D         |
| m          | I         |

#### Try 3

Given that vowels make reading the plaintext easier, we can try to decipher the remaining vowels in the ciphertext - `o` and `u` - though `u` is not as common as `o` in English. So, by reading the plaintext deciphered so far, and relating it to the ciphertext's frequencies, let us try converting `x` to `o`.

```bash
tr ’ytnvupmx’ ’THEANDIO’ < ciphertext.txt > plaintext.txt
```

No `O` seems out of place in the plaintext, so we will assume this is correct.

The result can be seen [here](/files/LOGBOOK9/TASK1/plaintext_try3.txt).

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| y          | T         |
| t          | H         |
| n          | E         |
| v          | A         |
| u          | N         |
| p          | D         |
| m          | I         |
| x          | O         |

### Try 4

Considering the words `THIq` and `ATTENDEEq` in the ciphertext, the likelihood of `q` being `S` is high, so let us make this conversion as well.

```bash
tr ’ytnvupmxq’ ’THEANDIOS’ < ciphertext.txt > plaintext.txt
```

The words in plaintext containing `S` seem to be correctly deciphered, so we will assume this is correct.

The result can be seen [here](/files/LOGBOOK9/TASK1/plaintext_try4.txt).

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| y          | T         |
| t          | H         |
| n          | E         |
| v          | A         |
| u          | N         |
| p          | D         |
| m          | I         |
| x          | O         |
| q          | S         |

### Try 5

With this amount of letters deciphered, it becomes easier to decipher the ciphertext by reading it and finding words that are almost fully deciphered (as we did in the previous conversion), and that are related to each other. Consider the groups of words:

- `DIfIDED`, `fOTES`, `fOTEhS`, `INITIATIfES`, `cOfIE`, `cOfIES`, `DIfISIfE` and `HAfE`
- `lAS`, `lHETHEh`, `lHO`, `HOl`, `AlAhDS`, `lONT`, `lITH`, `lIN`, `NATIONAi` and `gEHIND`

... where the undeciphered letters are the same and have very few possibilities. This makes these letters safe guesses to decipher.

These groups, together with some other words that are almost fully deciphered, give context to the plaintext, making it easier to decipher the remaining letters:

- `aONfEhSATION`, `hOSTEh`, `DIhEaTOhS` (with the last one being preceded by `NOcINATED`),
- `lEINSTEIN`, which is a special case, having a termination of a very specific group of nouns; as well as the first letter being missing, and the fact that it is preceded by `HAhfEd`, makes it a safe guess.
- The presence of the words `cOfIE` and `cOfIES` several times, as well as `HOiidlOOD`

We can follow these hunches and decipher all these words as a group with the context of movies in mind (which include actors, directors, award ceremonies, votes, and nominations):

- `f` to `V`
- `c` to `M`
- `a` to `C`
- `h` to `R`
- `l` to `W`
- `d` to `Y`
- `i` to `L`
- `g` to `B`

```bash
tr ’ytnvupmxqfcahldig’ ’THEANDIOSVMCRWYLB’ < ciphertext.txt > plaintext.txt
```

All the substitutions seem to be correct, as some parts of the plaintext start making sense and the words seem to be correctly placed.

The result can be seen [here](/files/LOGBOOK9/TASK1/plaintext_try5.txt).

Letters deciphered so far:

| Ciphertext | Plaintext |
| ---------- | --------- |
| y          | T         |
| t          | H         |
| n          | E         |
| v          | A         |
| u          | N         |
| p          | D         |
| m          | I         |
| x          | O         |
| q          | S         |
| f          | V         |
| c          | M         |
| a          | C         |
| h          | R         |
| l          | W         |
| i          | L         |
| g          | B         |

#### Result

The more letters are deciphered in the monoalphabetic substitution cipher, the easier it becomes to decipher the remaining letters, as more words are complete and the context of the plaintext becomes clearer. So, the complete cipher is:

| Ciphertext | Plaintext |
| ---------- | --------- |
| y          | T         |
| t          | H         |
| n          | E         |
| v          | A         |
| u          | N         |
| p          | D         |
| m          | I         |
| x          | O         |
| q          | S         |
| f          | V         |
| c          | M         |
| a          | C         |
| h          | R         |
| l          | W         |
| d          | Y         |
| i          | L         |
| g          | B         |
| e          | P         |
| r          | G         |
| k          | X         |
| z          | U         |
| s          | K         |
| b          | F         |
| j          | Q         |
| o          | J         |
| w          | Z         |

And the whole ciphertext can be deciphered with the following command:

```bash
tr ’ytnvupmxqfcahldigerkzsbjow’ ’THEANDIOSVMCRWYLBPGXUKFQJZ’ < ciphertext.txt > plaintext.txt
```

The final result can be seen [here](/files/LOGBOOK9/TASK1/plaintext_final.txt).

## Task 2: Encryption (and Decryption) using Different Ciphers

As requested by the guidelines (plaintext with at least 1000 bytes), the [plaintext](/files/LOGBOOK9/TASK2/plaintext.txt) generated by ChatGPT has 1527 characters, including spaces, punctuation, and newlines. This results in a total of 1527 bytes (1.527kB).

### Encryption: using aes-128-ecb, aes-128-cbc and aes-128-ctr

**Question 1A:** When encrypting, which flags did you have to specify?

**Answer 1A:** The flags that were specified when encrypting the plaintext with the different ciphers were the following:

#### aes-128-ecb

```bash
-aes-128-ecb                        # the cipher type
-e                                  # operation (encrypt the input data (default))
-in plaintext.txt                   # input filename
-out cipher_ecb.bin                 # output filename
-K 00112233445566778889aabbccddeeff # the key to use for encryption as a string of hexadecimal digits (when only the key is defined, IV must be specified)
-iv 0102030405060708                # the initialization vector as a string of hexadecimal digits
```

```bash
openssl enc -aes-128-ecb -e -in plaintext.txt -out cipher_ecb.bin -K 00112233445566778889aabbccddeeff -iv 0102030405060708
# Output: warning: iv not used by this cipher
```

> Note: The warning message is due to the fact that the `IV` is not used in the ECB mode, and therefore not required.

The encrypted output can be found [here](/files/LOGBOOK9/TASK2/cipher_ecb.bin)

#### aes-128-cbc

```bash
-aes-128-cbc                        # the cipher type
-e                                  # operation (encrypt the input data (default))
-in plaintext.txt                   # input filename
-out cipher_cbc.bin                 # output filename
-K 00112233445566778889aabbccddeeff # the key to use for encryption as a string of hexadecimal digits (when only the key is defined, IV must be specified)
-iv 0102030405060708                # the initialization vector as a string of hexadecimal digits
```

```bash
openssl enc -aes-128-cbc -e -in plaintext.txt -out cipher_cbc.bin -K 00112233445566778889aabbccddeeff -iv 0102030405060708
# Output: hex string is too short, padding with zero bytes to length
```

> Note: The warning message is due to the fact that the `IV` doesn't have the full length required for the AES algorithm, 16 bytes (128 bits), so it is padded with zeros and the encryption is completed without an error.

The encrypted output can be found [here](/files/LOGBOOK9/TASK2/cipher_cbc.bin)

#### aes-128-ctr

```bash
-aes-128-ctr                        # the cipher type
-e                                  # operation (encrypt the input data (default))
-in plaintext.txt                   # input filename
-out cipher_ctr.bin                 # output filename
-K 00112233445566778889aabbccddeeff # the key to use for encryption as a string of hexadecimal digits (when only the key is defined, IV must be specified)
-iv 0102030405060708                # the initialization vector as a string of hexadecimal digits
```

```bash
openssl enc -aes-128-ctr -e -in plaintext.txt -out cipher_ctr.bin -K 00112233445566778889aabbccddeeff -iv 0102030405060708
# Output: hex string is too short, padding with zero bytes to length
```

The encrypted output can be found [here](/files/LOGBOOK9/TASK2/cipher_ctr.bin)

**Question 1B:** What's the difference between these different modes?

**Answer 1B:** Given that the algorithm in these 3 cipher types is the same (AES), as well as the key size (128-bit), the main difference is their mode of operation (how they handle the encryption process). The three modes used in this task are:

- **Electronic Codebook (ECB)**: one of the simplest encryption modes. It breaks the message into plaintext blocks. Each block is encrypted independently with the same key. This means that identical plaintext blocks will result in identical ciphertext blocks, which can lead to patterns in the encrypted data being revealed. This aspect makes it insecure, proven by the ECB penguin image example (the image's data is different (color), but you can still see the penguin). Additionally, padding is required for CBC mode, as the plaintext can be a multiple of the block size.

- **Cipher Block Chaining (CBC)**: a more secure mode than ECB. It uses an initialization vector (IV) to XOR with the first plaintext block before encryption. After encryption, the result is XOR'ed with the next plaintext block before the next encryption. This means that each ciphertext block depends on all the previous plaintext blocks, making it more secure than ECB. Like the ECB mode, padding is required for CBC mode, as the plaintext can be a multiple of the block size.

- **Counter Block Mode (CTR)**: It generates a key stream by encrypting a nonce concatenated with a counter value with the key. This key stream is then XOR'ed with the plaintext to produce the ciphertext. This mode is very efficient because:
  - the key stream can be pre-processed, due to the block cipher not being applied directly to the message
  - any part of the data can be accessed efficiently, including read/write access. A
  - both encryption and decryption can be parallelized, meaning that the encryption of each block can be done independently, and therefore faster.

Furthermore, padding is not required for CTR mode, because the plaintext is XOR'ed with the key stream, and the key stream is generated for the entire plaintext (by incrementing the counter as many times as needed to go through the entire plaintext).

### Decryption: using aes-128-ecb, aes-128-cbc and aes-128-ctr

**Question 2A:** When decrypting, which flags did you have to specify?

**Answer 2A:** The flags that were specified when decrypting the ciphertext with the different ciphers were the following:

#### aes-128-ecb

```bash
-aes-128-ecb                        # the cipher type
-d                                  # operation (decrypt the input data)
-in cipher_ecb.bin                  # input filename
-out decrypted_ecb.txt              # output filename
-K 00112233445566778889aabbccddeeff # the key to use for encryption as a string of hexadecimal digits (when only the key is defined, IV must be specified)
-iv 0102030405060708                # the initialization vector as a string of hexadecimal digits
```

```bash
openssl enc -aes-128-ecb -d -in cipher_ecb.bin -out decrypted_ecb.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708
# Output: warning: iv not used by this cipher
diff -s plaintext.txt decrypted_ecb.txt
# Output: Files plaintext.txt and decrypted_ecb.txt are identical
```

> Note: The warning message is due to the fact that the `IV` is not used in the ECB mode, and therefore not required.
> Note 2: The `diff` command is used to compare the plaintext and the decrypted plaintext, and the output shows that they are identical.

The decrypted output can be found [here](/files/LOGBOOK9/TASK2/decrypted_ecb.txt)

#### aes-128-cbc

```bash
-aes-128-cbc                        # the cipher type
-d                                  # operation (decrypt the input data)
-in cipher_cbc.bin                  # input filename
-out decrypted_cbc.txt              # output filename
-K 00112233445566778889aabbccddeeff # the key to use for encryption as a string of hexadecimal digits (when only the key is defined, IV must be specified)
-iv 0102030405060708                # the initialization vector as a string of hexadecimal digits
```

```bash
openssl enc -aes-128-cbc -d -in cipher_cbc.bin -out decrypted_cbc.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708
# Output: hex string is too short, padding with zero bytes to length
diff -s plaintext.txt decrypted_cbc.txt
# Output: Files plaintext.txt and decrypted_cbc.txt are identical
```

> Note: The warning message is due to the fact that the `IV` doesn't have the full length required for the AES algorithm, 16 bytes (128 bits), so it is padded with zeros and the encryption is completed without an error.

The decrypted output can be found [here](/files/LOGBOOK9/TASK2/decrypted_cbc.txt)

#### aes-128-ctr

```bash
-aes-128-ctr                        # the cipher type
-d                                  # operation (decrypt the input data)
-in cipher_ctr.bin                  # input filename
-out decrypted_ctr.txt              # output filename
-K 00112233445566778889aabbccddeeff # the key to use for encryption as a string of hexadecimal digits (when only the key is defined, IV must be specified)
-iv 0102030405060708                # the initialization vector as a string of hexadecimal digits
```

```bash
openssl enc -aes-128-ctr -d -in cipher_ctr.bin -out decrypted_ctr.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708
# Output: hex string is too short, padding with zero bytes to length
diff -s plaintext.txt decrypted_ctr.txt
# Files plaintext.txt and decrypted_ctr.txt are identical
```

The decrypted output can be found [here](/files/LOGBOOK9/TASK2/decrypted_cbc.txt)

**Question 2B:** What's the main difference between the aes-128-ctr and the other modes?

**Answer 2B:** The answer to question 1B has already detailed the different ways the ECB, CBC, and CTR modes work. The main difference between the CTR mode and the other modes is that, during encryption, the plaintext does not go through the encryption algorithm, the keystream does. Conversely, during decryption, the ciphertext does not go through the decryption algorithm, the keystream does. In each case, the desired output (plaintext/ciphertext) is obtained by XORing the keystream with the ciphertext/plaintext, respectively (which is the only operation done on them). This is contrary to the ECB and CBC modes, where the plaintext/ciphertext are directly encrypted/decrypted using the AES algorithm.

## Task 5: Error Propagation - Corrupted Cipher Text

Given that our group number 2, the byte to change in each ciphertext is byte number 50\*2 = 100 (0x64), assuming the first byte is the 0th. The 100th byte corresponds to the letter `t` in `... to explore the world beyond ...`. Given that the AES algorithm uses 128-bit blocks (16-bytes), the byte to change is in the 7th block (byte 96 to byte 111).

We will make this change in the encrypted binary file using the `Bless Hex Editor` and set it to `0x50` (arbitrary value - different from the 100th byte in each respective file).

### aes-128-ecb

By analyzing the [ECB decryption scheme](/images/LOGBOOK9/scheme_ECB_decryption.png), we can see that the corrupted ciphertext byte will only affect the block in which it is located, and the rest of the blocks will remain unchanged, because the ECB mode encrypts each block independently.

![Uncorrupted ECB ciphertext in bless](/images/LOGBOOK9/cipher_ecb_before.png)

Image 1: Excerpt of the uncorrupted ECB ciphertext in `Bless`

![Corrupted ECB ciphertext in bless](/images/LOGBOOK9/cipher_ecb_after.png)

Image 2: Excerpt of the corrupted ECB ciphertext in `Bless`

```bash
openssl enc -aes-128-ecb -d -in corrupted_cipher_ecb.bin -out corrupted_decrypted_ecb.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708
# Output:
# warning: iv not used by this cipher
```

The corrupted ciphertext can be found [here](/files/LOGBOOK9/TASK5/corrupted_cipher_ecb.bin).
The corrupted decrypted output can be found [here](/files/LOGBOOK9/TASK5/corrupted_decrypted_ecb.txt).

Given the output, we can confirm that our analysis was correct (only the 7th block is corrupted):

![Corrupted ECB decrypted output](/images/LOGBOOK9/corrupted_decrypted_ecb.png)

Image 3: Excerpt of the corrupted ECB decrypted plaintext

```plaintext
�[����}
�/Q�J
```

> 16 bytes are corrupted (including a newline character)

### aes-128-cbc

By analyzing the [CBC decryption scheme](/images/LOGBOOK9/scheme_CBC_decryption.png), we can see that the corrupted ciphertext byte will affect the block in which it is located (7th), as well as the next block (8th). This is because the current ciphertext block is decrypted and then XOR'ed with the previous ciphertext block to obtain the plaintext block.
The blocks after that (starting from the 9th) will remain unchanged, because even though the 8th plaintext block is corrupted (due to the corrupted 7th ciphertext block), the 9th block is decrypted using the (uncorrupted) 8th ciphertext block.

![Uncorrupted CBC ciphertext in bless](/images/LOGBOOK9/cipher_cbc_before.png)

Image 4: Excerpt of the uncorrupted CBC ciphertext in `Bless`

![Corrupted CBC ciphertext in bless](/images/LOGBOOK9/cipher_cbc_after.png)

Image 5: Excerpt of the corrupted CBC ciphertext in `Bless`

```bash
openssl enc -aes-128-cbc -d -in corrupted_cipher_cbc.bin -out corrupted_decrypted_cbc.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708
# Output:
# hex string is too short, padding with zero bytes to length
```

The corrupted ciphertext can be found [here](/files/LOGBOOK9/TASK5/corrupted_cipher_cbc.bin).
The corrupted decrypted output can be found [here](/files/LOGBOOK9/TASK5/corrupted_decrypted_cbc.txt).

Given the output, we can confirm that our analysis was correct (the 7th and 8th blocks are corrupted, and the further blocks are not):

![Corrupted CBC decrypted output](/images/LOGBOOK9/corrupted_decrypted_cbc.png)

Image 6: Excerpt of the corrupted CBC decrypted plaintext

```plaintext
�4$�ez�[�]��j��he wgrld beyond
```

> The first 16 bytes (7th block) are corrupted and some of the following 16 bytes (8th block) are corrupted as well

### aes-128-ctr

By analyzing the [CTR decryption scheme](/images/LOGBOOK9/scheme_CTR_decryption.png), we can see that the corrupted ciphertext byte will only affect the (single) respective byte in the plaintext, because the CTR mode decrypts the ciphertext block by XORing it with the keystream (this keystream is generated by encrypting a nonce concatenated with a counter, using the key). This means that the ciphertext block does not go through the decryption process - the keystream does - and is instead XOR'ed (which is naturally done byte-by-byte, giving it the byte-independent characteristic, which results in the corrupted byte not propagating to the rest of the plaintext block), with the keystream to obtain the plaintext block.

![Uncorrupted CTR ciphertext in bless](/images/LOGBOOK9/cipher_ctr_before.png)

Image 7: Excerpt of the uncorrupted CTR ciphertext in `Bless`

![Corrupted CTR ciphertext in bless](/images/LOGBOOK9/cipher_ctr_after.png)

Image 8: Excerpt of the corrupted CTR ciphertext in `Bless`

```bash
openssl enc -aes-128-ctr -d -in corrupted_cipher_ctr.bin -out corrupted_decrypted_ctr.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708
# hex string is too short, padding with zero bytes to length
```

The corrupted ciphertext can be found [here](/files/LOGBOOK9/TASK5/corrupted_cipher_ctr.bin).
The corrupted decrypted output can be found [here](/files/LOGBOOK9/TASK5/corrupted_decrypted_ctr.txt).

Given the output, we can confirm that our analysis was correct (only the 100th byte, `t`, is corrupted):

![Corrupted CTR decrypted output](/images/LOGBOOK9/corrupted_decrypted_ctr.png)

Image 9: Excerpt of the corrupted CTR decrypted plaintext

```plaintext
ger :o explore t
```

> The whole 7th block is shown above.
