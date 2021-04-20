from pwn import *
from Cryptodome.Util.number import getPrime, inverse, long_to_bytes, bytes_to_long
import gmpy2
import math

HOST = "localhost"
PORT = 8888
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