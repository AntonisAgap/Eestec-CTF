from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import bcrypt
from Crypto.Cipher import AES
from sage.all import *

p = 4566065691823285126725148967010801309220233002802904153241
a = 227907375881651903584877890985545706866573389150228308104
b = 3998659116920584825807479363516922827218502560448779364782
E = EllipticCurve(GF(p),[a,b])
P = E(4206491747417187590068684446696003266570427558241621500310,3575035391285926130153819912348189517782214432782863401724)

Qb = E(1791949839791122190546233750753244260851112033084523925678,3580275061590791028794415451416286977588041153017396781835)
nonce = "d56fa88d4dc685a4e89f1ff2feab99ad"
ct = "260f931ce9418a4f7441551f7f6004dc7c14d21f23d44795a034b17859b8fccffea6a62aee3929e6f9ccc2c9da0bb1"
Qa = E(1182868381060519044572066866474873241673096724988337116814,154571546801027591725651933541756554893669723825951645884)

def SmartAttack(P,Q,p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])

    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break

    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break

    p_times_P = p*P_Qp
    p_times_Q = p*Q_Qp

    x_P,y_P = p_times_P.xy()
    x_Q,y_Q = p_times_Q.xy()

    phi_P = -(x_P/y_P)
    phi_Q = -(x_Q/y_Q)
    k = phi_Q/phi_P
    return ZZ(k)


na = SmartAttack(P, Qa, p)


def create_key(S):
    key = str.encode(str(S))
    h = SHA256.new()
    h.update(key)
    key = h.hexdigest()
    return key
S = na*Qb
key = create_key(int(S[0]))

def decrypt_message(ciphertext,key,nonce):
    key = bytearray.fromhex(key)
    nonce = bytearray.fromhex(nonce)
    ciphertext = bytearray.fromhex(ciphertext)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

plaintext = decrypt_message(ct,key,nonce)
print(plaintext)