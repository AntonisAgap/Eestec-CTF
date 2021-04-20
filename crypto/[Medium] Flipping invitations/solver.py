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
