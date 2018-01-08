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
    delta = 10
    after = int(datetime.datetime.now().timestamp())
    print("before : {} after : {}".format(before, after))

    if(after - before < delta):
        return True
    else:
        return False


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        random = make_timestamp()
        response = Packer.pack(random)
        self.request.sendall(response)

        tmp = self.request.recv(1024).strip()
        recv = Packer.unpack(tmp)

        if(check_timestamp(recv)):
            print("Phase 2 Response: Correct")
            response = "Timestamp correct! flag{s0cket!}\n"

        else:
            print("Phase 2 Response: Failed")
            response = "Nope!\n"

        self.request.sendall(bytes(response,'UTF-8'))

if __name__ == "__main__":
    HOST, PORT = "", 6666
    server = socketserver.TCPServer((HOST,PORT), TCPHandler)

    server.serve_forever()
