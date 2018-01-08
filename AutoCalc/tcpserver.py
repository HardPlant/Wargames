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


class RSAManager:
    def __init__(self):
        (self.pubkey, self.privkey) = rsa.newkeys(512)

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
        temp = self.request.recv(1024).strip()
        recv = temp.decode('UTF-8')
        print("Phase 1: {}".format(recv))
        receiver_pubkey = RSAManager.parse_pub(recv)

        random = make_timestamp()
        response = "{},{}".format(str(random),sender.get_pub())
        print("Phase 1 Response: {}".format(response))
        self.request.sendall(bytes(response,'UTF-8'))

        tmp = self.request.recv(1024).strip()
        print("Phase 2 : {}".format(tmp))
        recv = rsa.verify(tmp,receiver_pubkey)
        recv = Packer.unpack(recv)

        if(check_timestamp(recv)):
            print("Phase 2 Response: Correct")
            self.request.sendall("Timestamp correct! flag{RSA_Authe}\n")
        else:
            print("Phase 2 Response: Failed")
            self.request.sendall("Nope!")


if __name__ == "__main__":
    HOST, PORT = "", 7777
    server = socketserver.TCPServer((HOST,PORT), TCPHandler)

    server.serve_forever()
