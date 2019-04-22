import socket, time
from threading import Thread


HEADERSIZE = 10

class Server():
    def __init__(self, header_size=10, port=1234, queue_size = 5):
        self.headersize = header_size
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((socket.gethostname(), port))
        self.s.listen(queue_size)

    def start(self, handler):
        while True:
            clientsocket, address = self.s.accept()
            print(f"Connection from {address} has been established.")
            thread = Thread(target=handler, args=[clientsocket, self.headersize])
            thread.daemon = True
            thread.start()


if __name__ == '__main__':

    def _test_handler(clientsocket, header_size):
        while True:
            full_msg = ''
            new_msg = True
            while True:
                msg = clientsocket.recv(16)
                if new_msg:
                    print("new msg len:", msg[:HEADERSIZE])
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                print(f"full message length: {msglen}")

                full_msg += msg.decode("utf-8")

                print(len(full_msg))

                if len(full_msg) - HEADERSIZE == msglen:
                    print("full msg recvd")
                    print(full_msg[HEADERSIZE:])
                    break

    s = Server()
    s.start(_test_handler)
