import socketserver
import rsa
import datetime
import time
import struct
import socket

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

def make_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost",7777))
    return sock

if __name__ == "__main__":
    receiver = RSAManager()
    tmp = receiver.get_pub()
    receiver_public_key = bytes(tmp, "UTF-8")

    connection = make_socket()
    connection.send(receiver_public_key)
    tmp = connection.recv(1024)
    response = tmp.decode('UTF-8')
    print("Phase 1 Response : {}".format(response))
    tmp = response.split(',')
    random = int(tmp[0])
    sender_public = ",".join((tmp[1], tmp[2]))
    sender_public_key = RSAManager.parse_pub(sender_public)

    enc_msg = rsa.sign(Packer.pack(make_timestamp()),receiver.privkey, 'SHA-1')
    print("Phase 1 Request : {}".format(enc_msg))
    connection.send(enc_msg)

    tmp = connection.recv(1024)
    flag = tmp.decode('UTF-8')
    print(flag)