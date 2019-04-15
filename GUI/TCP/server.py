import socket, time
from threading import Thread


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
        msg = "Welcome to the server!"
        msg = f"{len(msg):<{header_size}}"+msg

        clientsocket.send(bytes(msg,"utf-8"))
        msg = clientsocket.recv(1600)
        print(msg.decode("utf-8"))
        #while True:
        #    time.sleep(3)
        #    msg = f"The time is {time.time()}"
        #    msg = f"{len(msg):<{header_size}}"+msg

            #print(msg)

            #clientsocket.send(bytes(msg,"utf-8"))

    s = Server()
    s.start(_test_handler)
