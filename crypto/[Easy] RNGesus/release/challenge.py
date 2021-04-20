import binascii

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

# x^13+x^12+x^8+x^3+x^2
def keystreamGenerator(flag_bits,init_state):
    keystream = []
    state = init_state
    for i in range(len(flag_bits)):
        keystream.append(state[15])
        x = (((state[12]^state[11])^state[7])^state[2])^state[1]
        state = [x] + state[0:15]
    return keystream

def encrypt(flag_bits,keystream):
    ciphertext_bits = ''
    for i in range(len(flag_bits)):
        c_bit = int(flag_bits[i]) ^ keystream[i]
        ciphertext_bits = ciphertext_bits+str(c_bit)
    return ciphertext_bits

flag = ''
init_state = []
flag_bits = string2bits(flag)
keystream = keystreamGenerator(flag_bits,init_state)
print(encrypt(flag_bits,keystream))