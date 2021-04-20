# [__CuSm1th 🍆__](#)

## Description: 

* We need to find the message that Mr.Smith sends to his employees. Luckily we got access to his encryption oracle. 

## Objective: 

* The same plaintext gets encrypted with the same e, so we can use the chinese remainder theorem and perform hastaads broadcast attack to get the original message

## Flag: 🏁
* `INSSEC{h4stad_Br0adcast_4ttack_iz_pr3tty_c00l}`

### Difficulty:
* Medium

## Writeup

In this challenge we communicate with the encryption oracle of an RSA encryption algorithm. In order to understand how RSA works its good to read this:
https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-045j-automata-computability-and-complexity-spring-2011/lecture-notes/MIT6_045JS11_rsa.pdf

and

https://www.nku.edu/~christensen/the%20mathematics%20of%20the%20RSA%20cryptosystem.pdf

RSA is a public key cryptographic algorithm (assymetric). Looking at the `server.py` code we can see that oracle returns the flag encrypted *C* and the public key *N*. Since the the public key is produced by two 1028 bits primes its impossible to factorize it to find *p* and *q*. We can see though that the **same** ciphertext is being encrypted using the **same** exponent *e* = 37. We can use this information to perform a *Coppersmit's* type of attack called *Hastad's Broadcast Attack* which uses the Chinese Remainder Theorem to recover the plaintext from the ciphertexts.

Sources to read:

http://koclab.cs.ucsb.edu/teaching/cren/project/2017/chennagiri.pdf

https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html


In order to perform the attack we need at least *e=37* ciphertexts.

Let's implement the attack on code:

```python
from pwn import *
from Cryptodome.Util.number import getPrime, inverse, long_to_bytes, bytes_to_long
import gmpy2
import math

HOST = "localhost" # change
PORT = 8888 #change
conn = remote(HOST,PORT)


cts = []
ns = []

for i in range(37):
	conn.recvline()
	conn.recvline()
	conn.send('1')
	ct = conn.recvline()
	N = conn.recvline()
	sleep(1)
	
	ct = bytearray.fromhex(ct.decode())
	ct = bytes_to_long(ct)
	ns.append(int(N.decode()))
	cts.append(int(ct))

# calculating N
N = 1
for n in ns:
	N = N*n
# calculatins Ns
Ns = []
for n in ns:
	Ns.append(N//n)

# calculating us
us = []
for i in range(len(ns)):
	u = gmpy2.invert(Ns[i], ns[i])
	us.append(u)

# calculating mults
mults = []
for i in range(len(ns)):
	mult = cts[i]*us[i]*Ns[i]
	mults.append(mult)
sum = 0
for mu in mults:
	sum = sum + mu
M = sum%N
m = gmpy2.iroot(M,37)[0]
flag = long_to_bytes(m)
print(flag)
```

Nice! The flag is `INSSEC{h4stad_Br0adcast_4ttack_iz_pr3tty_c00l}`