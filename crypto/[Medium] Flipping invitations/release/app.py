from flask import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta
from secrets import flag
import os

app = Flask(__name__)

BLOCK_SIZE = AES.block_size
KEY = os.urandom(BLOCK_SIZE)

@app.route('/check_invitation/<invitation>/<iv>/')
def check_admin(invitation, iv):
    invitation = bytes.fromhex(invitation)
    iv = bytes.fromhex(iv)
    try:
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(invitation)
        unpadded = unpad(decrypted, BLOCK_SIZE)
        print(unpadded)
    except ValueError as e:
        return {"error": str(e)}
    if "user=INSSec;" in str(unpadded):
        return {"flag": flag}
    else:
        return {"error": "Only INSSec members can read the flag"}


@app.route('/get_invitation/')
def get_cookie():
    expires_at = str(datetime.today() + timedelta(days=1))
    invitation = f"user=Eestec;expiry={expires_at}".encode()
    iv = os.urandom(BLOCK_SIZE)
    print(invitation)
    padded = pad(invitation, BLOCK_SIZE)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded)
    ciphertext = iv.hex() + encrypted.hex()
    print(encrypted)
    print(encrypted.hex())
    return {"invitation": ciphertext}