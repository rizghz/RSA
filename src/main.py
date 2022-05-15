from math import gcd
from operator import mod
from random import randint
from time import time

def 𝜙(n: int) -> int:
   s = [k for k in range(1, n) if gcd(n, k) == 1]
   return len(s)

def prime(k: int) -> bool:
   if k < 2: return False
   s = [mod(k, i) for i in range(2, k)]
   return 0 not in s

def congruences(a: int, x: int, b: int, m: int) -> int:
   if mod(a * x, m) == b:
      return x
   else: return 0

def generate(n: int, totient: int) -> tuple[int, int]:
   e, d = 0, 0
   while gcd(totient, e) != 1:
      e = randint(13, totient - 1)
   while d == 0:
      k = randint(1, n)
      d = congruences(e, k, 1, totient)
   return e, d

def parameter() -> tuple[int, int]:
   p, q = 0, 0
   while not prime(p) or not prime(q):
      p = randint(700, 3000)
      q = randint(700, 3000)
   return p, q

def key(n: int) -> dict[str, int]:
   e, d = generate(n, 𝜙(n))
   k = {
      'private': {'d': d, 'n': n},
      'public' : {'e': e, 'n': n},
   }
   return k

def digit(text: str, n: int) -> int:
   test, d = text, len(str(n))
   while len(test) != 0:
      if int(test[0:d]) > n:
         test, d = text, d - 1
      else: test = test[d::]
   return d

def block(text: str, d: int) -> list:
   result = []
   while len(text) != 0:
      result.append(text[0:d])
      text = text[d::]
   return result

def encrypt(plain: str, key: dict) -> str:
   d = len(str(key['n']))
   chiper = [ord(m) + 69 for m in plain]
   chiper = [str(m) for m in chiper]
   chiper = ''.join(chiper)
   chiper = block(chiper, 6)
   chiper = [int(m) for m in chiper]
   chiper = [mod(m ** key['e'], key['n']) for m in chiper]
   chiper = [str(m).rjust(d, '0') for m in chiper]
   return ''.join(chiper)

def decrypt(chiper: str, key: dict) -> str:
   d = len(str(key['n']))
   plain = block(chiper, d)
   plain = [int(c) for c in plain]
   plain = [mod(c ** key['d'], key['n']) for c in plain]
   plain = [str(c) for c in plain]
   plain = ''.join(plain)
   plain = block(plain, 3)
   plain = [int(c) - 69 for c in plain]
   plain = [chr(c) for c in plain]
   return ''.join(plain)

if __name__ == "__main__":
   p, q = parameter()
   n = p * q
   message = input('pesan      : ')
   key_start = time()
   k = key(n)
   key_end = time()
   encrypt_start = time()
   chiper = encrypt(message, k['public'])
   encrypt_end = time()
   decrypt_start = time()
   plain = decrypt(chiper, k['private'])
   decrypt_end = time()
   print(f"kunci      : {k} ({key_end - key_start} detik)")
   print(f"chiper     : {chiper} ({encrypt_end - encrypt_start} detik)")
   print(f"plain      : {plain} ({decrypt_end - decrypt_start} detik)")
