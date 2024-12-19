from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

import time
from binascii import unhexlify

KEYLEN = 16

def gen():
  offset = 3 # Hotfix to make Crypto blazing fast!!
  key = bytearray(b'\x00'*(KEYLEN-offset))
  key.extend(os.urandom(offset))
  return bytes(key)

def enc(k, m, nonce):
  cipher = Cipher(algorithms.AES(k), modes.CTR(nonce))
  encryptor = cipher.encryptor()
  cph = b""
  cph += encryptor.update(m)
  cph += encryptor.finalize()
  return cph

def dec(k, c, nonce):
  cipher = Cipher(algorithms.AES(k), modes.CTR(nonce))
  decryptor = cipher.decryptor()
  msg = b""
  msg += decryptor.update(c)
  msg += decryptor.finalize()
  return msg


# ==== Code to find the flag ====
# By brute-forcing the key
def find_flag():
  nonce = unhexlify("7fd84ef196cd4c9cb16560524326a325")
  ciphertext = unhexlify("8d4f1b53b6ec30d878a2a368653202b035cf764d1ad0")
  start_time = time.time()

  offset = 3
  for i in range(256**offset):  # 256^3 possible combinations for the 3 bytes
    key = bytearray(b'\x00'*(KEYLEN-offset))
    key.extend(i.to_bytes(offset, 'big'))  # Fill the rest of the key with the 3 bytes

    decrypted = dec(bytes(key), ciphertext, nonce)
    try:
      decoded_msg = decrypted.decode('utf-8')
      if decoded_msg.startswith("flag{") and decoded_msg.endswith("}"):
        print(f"Found flag: {decoded_msg}")
        print(f"Number of iterations: {i+1}")

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")

        return decoded_msg
    except UnicodeDecodeError:
      # To not crash when bytes are not decodable to UTF-8
      pass
  return None

find_flag()
