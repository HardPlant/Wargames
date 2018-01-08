import socketserver
import datetime
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
    delta = 2
    after = int(datetime.datetime.now().timestamp())
    print("before : {} after : {}".format(before, after))

    if(after - before < delta):
        return True
    else:
        return False


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        '''
        random = make_timestamp()
        response = Packer.pack(random)
        '''
        response = bytes("Give me Python timestamp, please?", "UTF-8")
        self.request.sendall(response)

        tmp = self.request.recv(1024).strip()
        recv = Packer.unpack(tmp)

        if(check_timestamp(recv)):
            print("Response: Correct")
            response = "Timestamp correct! flag{Tim3st@mpWi11NeedS00n}\n"

        else:
            print("Response: Failed")
            response = "Nope!\n"

        self.request.sendall(bytes(response,'UTF-8'))

if __name__ == "__main__":
    HOST, PORT = "", 6666
    server = socketserver.TCPServer((HOST,PORT), TCPHandler)

    server.serve_forever()
