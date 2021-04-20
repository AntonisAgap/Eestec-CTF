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