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


def make_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost",6666))
    return sock

if __name__ == "__main__":
    connection = make_socket()

    tmp = connection.recv(1024)
    response = tmp
    print("Server Says: {}".format(response))
    time.sleep(10)
    timestamp = make_timestamp()
    request = Packer.pack(timestamp)
    print("I Says: {}".format(request))
    connection.send(request)

    tmp = connection.recv(1024)
    response = tmp
    print("Server Says: {}".format(response))