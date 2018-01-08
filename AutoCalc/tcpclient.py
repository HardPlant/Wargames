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


def get_client_keys():
    pubkey = rsa.PublicKey(7157919685780998040030268198690435899059491873181568440366064487608153356073537591530515598465502649272062627915514689661196740137864362592337214857205123,
                           65537)
    privkey = rsa.PrivateKey(7157919685780998040030268198690435899059491873181568440366064487608153356073537591530515598465502649272062627915514689661196740137864362592337214857205123,
                             65537,
                             2953841919861255351825970115104182963670353505808863977138108458845575894458374213828505117426236570451870346927080695776866504949047424394402686371008553,
                             4432995129140126532139099625504781507619770933889522645428471238296144681878392319,
                             1614691529600085178779141836636653810897261074378621408543337333988360317)
    return pubkey, privkey


class RSAManager:
    def __init__(self):
        (self.pubkey, self.privkey) = get_client_keys()

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

    connection = make_socket()

    tmp = connection.recv(1024)
    response = tmp.decode('UTF-8')
    print("Timestamp : {}".format(response)) # Timestamp

    tmp = int(response)
    server_timestamp = Packer.pack(tmp + 1)

    enc_msg = rsa.sign(server_timestamp, receiver.privkey, 'SHA-1')
    print("Timestamp Sent : {}".format(enc_msg))
    connection.send(enc_msg)

    tmp = connection.recv(1024)
    flag = tmp.decode('UTF-8')
    print(flag)