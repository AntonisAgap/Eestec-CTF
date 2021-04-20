# [__RNGesus ⛪__](#)

## Description: 

* We recovered a ciphertext in binary and the source code of the encryption algorithm. It looks like they used a LFSR as a keystream generator. Can you decipher the message? 

## Objective: 

* We can perform a known plaintext attack or bruteforce to find the initial state of the LFSR generator. After that we can produce the same keystream and XOR it with the bits of the ciphertext and recover the flag.

## Flag: 🏁
* `INSSEC{4ll_h4il_rNg3sus_0ur_l0rd_and_s4vi0r}`

### Difficulty:
* Easy 


## Writeup

From the `challenge.py` code we can see that the ciphertext was generated from the flag using a LFSR prng. The LFSR was used to create a keystream using an initial state and then the keystream was XORed with the plaintext to create the ciphertext.

How LFSRs work: https://www.cs.purdue.edu/homes/ninghui/courses/Fall05/lectures/355_Fall05_lect10.pdf

Since we have the source code of the LFSR, the only thing we need to do is to find the initial state and generate the keystream to XOR it with the ciphertext. There are 2 ways to find the initial state:
1. Bruteforce it
2. Recover it using known plaintext attack

We know that all flags start with the prefic `INSSEC{`. We can use this information to recover the initial state. The first 16 bits of the ciphertext were produced like this:
```
"IN" xor keystream[:16] = ct[:16]
```
So in order to find the first 16 bits we need to xor the bits of "IN" 
(pt[:16]) with the first 16 bits of the ciphertext. After that we need to reverse the bitstream to find the initial state (read how LFSRs work).
After we find the inital state we can easily produce the keystream and xor it with the ciphertext to recover the plaintext.

Let's put all of this to code:
```python
import binascii

ct = "1010010010110010101110000010001111100101011000001100001011100101101001010101110111101110001100100011000010110000100111001100100001000010100110111110101111100100001101100000111110010001000111001100011011011100011000101011000000110111010100000111110101000111010101001101101111001110100110111010101100010011100010010011111000001011010001001001011110111000"

def string2bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits2string(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def keystreamGenerator(flag_bits,init_state):
    keystream = []
    state = init_state
    for i in range(len(flag_bits)):
        keystream.append(state[15])
        x = (((state[12]^state[11])^state[7])^state[2])^state[1]
        state = [x] + state[0:15]
    return keystream

def decrypt(flag_bits,keystream):
    plaintext_bits = ''
    for i in range(len(flag_bits)):
        c_bit = int(flag_bits[i]) ^ keystream[i]
        plaintext_bits = plaintext_bits+str(c_bit)
    return plaintext_bits

known_pt = string2bits("INSSEC{")
known_pt = known_pt[:16]
init_state = []
for i in range(len(known_pt)):
    init_state.append(int(known_pt[i])^int(ct[i]))

init_state.reverse()

keystream = keystreamGenerator(ct,init_state)
print(bits2string(decrypt(ct,keystream)))
```

The flag is: `INSSEC{4ll_h4il_rNg3sus_0ur_l0rd_and_s4vi0r}`