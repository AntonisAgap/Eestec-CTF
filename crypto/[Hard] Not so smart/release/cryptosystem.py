from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import bcrypt
from Crypto.Cipher import AES
from sage.all import *
from secrets import na,flag

def create_shared_secret(Qb,na):
    p = 4566065691823285126725148967010801309220233002802904153241
    a = 227907375881651903584877890985545706866573389150228308104
    b = 3998659116920584825807479363516922827218502560448779364782
    E = EllipticCurve(GF(p),[a,b])
    Qb = E(Qb[0],Qb[1])
    S = na*Qb
    return S

def create_key(S):
    key = str.encode(str(S))
    h = SHA256.new()
    h.update(key)
    key = h.hexdigest()
    return key

def encrypt_message(plaintext,key,nonce):
    key = bytearray.fromhex(key)
    nonce = bytearray.fromhex(nonce)
    plaintext = str.encode(plaintext)

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return ciphertext.hex()


def decrypt_message(ciphertext,key,nonce):
    key = bytearray.fromhex(key)
    nonce = bytearray.fromhex(nonce)
    ciphertext = bytearray.fromhex(ciphertext)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


Qb = [1791949839791122190546233750753244260851112033084523925678,3580275061590791028794415451416286977588041153017396781835]
nonce = "d56fa88d4dc685a4e89f1ff2feab99ad"

S = create_shared_secret(Qb,na)
key = create_key(int(S[0]))
ct = encrypt_message(flag,key,nonce)