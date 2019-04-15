import socket

HEADERSIZE = 10

class Client():

    def __init__(self, remote=socket.gethostname(), port=1234):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote = remote
        self.port = port

    def start(self, handler):
        self.s.connect((self.remote, self.port))
        handler(self.s)

    def send_message(self, payload):
        msg = f"{len(payload):<{HEADERSIZE}}" + payload
        self.s.send(bytes(msg, "utf-8"))


if __name__ == '__main__':
    def _test_client(s):
        while True:
            full_msg = ''
            new_msg = True
            while True:
                msg = s.recv(16)
                if new_msg:
                    print("new msg len:",msg[:HEADERSIZE])
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                print(f"full message length: {msglen}")

                full_msg += msg.decode("utf-8")

                print(len(full_msg))

                if len(full_msg)-HEADERSIZE == msglen:
                    print("full msg recvd")
                    print(full_msg[HEADERSIZE:])
                    new_msg = True
                    full_msg = ""

    def _test(s):
        msg = "helloooo serverrrr"
        s.send(bytes(msg,"utf-8"))

    Client = Client()
    Client.start(_test)

