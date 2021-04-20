# [__Flipping invitations 🍆__](#)

## Description: 

* The most anticipated  after-covid party will take place soon, but only INSSec members are allowed. Can you find a way to get in?

## Objective: 

* Perform a bit-flipping attack on the AES CBC algorithm and change `user=Eestec` to `user=INSSec`

## Flag: 🏁
* `INSSEC{fl1pping_b1ts_like_a_pr0}`

### Difficulty:
* Medium

## Writeup
By looking at the source code `app.py` we can see that we can communicate with an encryption-decryption flask app. In order to get the flag we must send a ciphertext which when decrypted must contain the string `"user=INSSec"`. Since we can't recover the key that is used to decrypt the ciphertext we must find another way. We can see that the app has two endpoints. One is for getting a chiphertext which was produced by a plaintext that contains the string `"user=Eestec"` and the other is to send an IV (initialized vector) and a ciphertext for the oracle to decrypt. In order to understand the attack it's good to have a basic understanding of the AES encryption algorithm and it's modes of encryption (especially CBC).

Sources to read:

https://en.wikipedia.org/wiki/Advanced_Encryption_Standard

https://www.highgo.ca/2019/08/08/the-difference-in-five-modes-in-the-aes-encryption-algorithm/

In order to manipulate the ciphertext which we are given in order to decrypt to the plaintext we want we must perform what is called a `Bit flipping attack`.

Sources to read:

https://crypto.stackexchange.com/questions/66085/bit-flipping-attack-on-cbc-mode

https://resources.infosecinstitute.com/topic/cbc-byte-flipping-attack-101-approach/

Now that we have a basic understanding of the attack, we can see that we must change the 6th-11th byte of the IV using the following function:
```
iv[i] = (plaintext we want)xor(plaintext which was encrypted)xor(iv[i])
```
Let's implement the attack:
```python
import requests
import json

host = 'http://127.0.0.1:5000' #change

url = host+'/get_invitation/'
response = requests.get(url)
response_dict = json.loads(response.text)
ct = response_dict.get("invitation")

ct = bytearray.fromhex(ct)
iv = ct[:16]
ct1 = ct[16:32]


iv = list(bytes(iv))
ct = list(bytes(ct))
ct1 = list(bytes(ct1))


iv[5] = ord("I")^ord('E')^iv[5]
iv[6] = ord("N")^ord('e')^iv[6]
iv[7] = ord("S")^ord('s')^iv[7]
iv[8] = ord("S")^ord('t')^iv[8]
iv[9] = ord("e")^ord('e')^iv[9]
iv[10] = ord("c")^ord('c')^iv[10]


iv = bytes(iv).hex()
invitation = bytes(ct[16:]).hex()

payload = host+'/check_invitation/'+str(invitation)+"/"+str(iv)
response = requests.get(payload)
print(response.text)
```
The flag is: `INSSEC{fl1pping_b1ts_like_a_pr0}`
