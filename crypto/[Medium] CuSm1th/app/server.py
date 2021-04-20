from Crypto.Util.number import getPrime, inverse, long_to_bytes, bytes_to_long
from Crypto.Random import get_random_bytes
from secret import flag
import signal
import socketserver


def RSAencrypt(flag=flag):
    p = getPrime(1024, randfunc=get_random_bytes)
    q = getPrime(1024, randfunc=get_random_bytes)
    N = p*q
    e = 37
    flag = bytes_to_long(flag)
    ct = pow(flag, e, N)
    ct = str(long_to_bytes(ct).hex())
    N = str(N)
    return ct, N


def challenge(req):
    try:
        req.sendall(b'Most secure RSA encryption system\n' +
                    b'1. Get encrypted message\n')
        choice = int(req.recv(2).decode().strip())
        if choice == 1:
            ct, N = RSAencrypt(flag)
            req.sendall((ct+'\n'+N+'\n').encode())


    except Exception as e:
        try:
            req.sendall(b'Unexpected error.\n')
            print(e)
            req.close()
        except:
            pass
        exit()


class incoming(socketserver.BaseRequestHandler):
    def handle(self):
        signal.alarm(300)
        req = self.request
        while True:
            challenge(req)


class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


socketserver.TCPServer.allow_reuse_address = False
server = ReusableTCPServer(("0.0.0.0", 1337), incoming)
server.serve_forever()