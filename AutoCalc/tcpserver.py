import socketserver
import rsa
import datetime
import time
import struct


class Packer:

    @staticmethod
    def pack(num):
        fmt = "I"
        return struct.pack(fmt, num)

    @staticmethod
    def unpack(packed):
        fmt = "I"
        return struct.unpack(fmt, packed)[0]


def make_timestamp():
    timestamp = datetime.datetime.now().timestamp()
    return int(timestamp)


def check_timestamp(before):
    delta = 10
    after = int(datetime.datetime.now().timestamp())
    print("before : {} after : {}".format(before, after))

    if(after - before < delta):
        return True
    else:
        return False


def get_server_keys():
    pubkey = rsa.PublicKey(9168571582432257053702075294818760020273587677271514650749610727046406386676190898163647513461476198234761835988352906600823933181728494997312924815612083,
                           65537)
    privkey = rsa.PrivateKey(9168571582432257053702075294818760020273587677271514650749610727046406386676190898163647513461476198234761835988352906600823933181728494997312924815612083,
                             65537,
                             455931379024775710484383834869071500161307692452017429036925421661721445816432318260083938361199528408421439141505851343160543410033685094774247193093649,
                             6046695701246579417924837985200791782205481995975620729753057861853235346813559499,
                             1516294524386612593732737817815743270405285273553439697256928195279199417)
    return pubkey, privkey

def get_client_pubkey():
    pubkey = rsa.PublicKey(7157919685780998040030268198690435899059491873181568440366064487608153356073537591530515598465502649272062627915514689661196740137864362592337214857205123,
                           65537)
    return pubkey

class RSAManager:
    def __init__(self):
        (self.pubkey, self.privkey) = get_server_keys()

    def receive_message(self,encrypted_message):
        crypto = rsa.decrypt(encrypted_message, self.privkey)
        return crypto

    def send_message(self,message, receiver_pubkey):
        dec = rsa.encrypt(message, receiver_pubkey)
        return dec

    def get_pub(self):
        return "{},{}".format(self.pubkey.n, self.pubkey.e)

    @staticmethod
    def parse_pub(str_pub):
        temp = str_pub.split(',') #temp[0] = n, temp[1] = e
        pubkey = rsa.PublicKey(int(temp[0]), int(temp[1]))
        return pubkey

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        sender = RSAManager()
        client_pubkey = get_client_pubkey()

        random = make_timestamp()
        response = "{}".format(str(random))
        print("Phase 1: Timestamp {}".format(response))
        self.request.sendall(bytes(response,'UTF-8'))

        tmp = self.request.recv(1024).strip()
        print("Phase 2 : Recv {}".format(tmp))

        expected = Packer.pack(random+1)
        is_true = rsa.verify(expected, tmp, client_pubkey)

        if(is_true):
            print("Phase 2 Response: Correct")
            response = "Timestamp correct! flag{RSA_Authe}\n"

        else:
            print("Phase 2 Response: Failed")
            response = "Nope!"

        self.request.sendall(bytes(response,'UTF-8'))

if __name__ == "__main__":
    HOST, PORT = "", 7777
    server = socketserver.TCPServer((HOST,PORT), TCPHandler)

    server.serve_forever()
