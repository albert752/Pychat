import socket
import errno
import sys
from threading import Thread
import time
from codes import *

class Client:

    def __init__(self, usr_name, remote="127.0.0.1", port=1234):
        self.ip = remote
        self.port = port
        self.usr_name = usr_name
        self.HEADER_LENGTH = 10
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_state = DISCONNECTED

    def start(self, handler):
        self.client_socket.connect((self.ip, self.port))
        self.client_socket.setblocking(True)

        username = self.usr_name.encode('utf-8')
        username_header = f"{len(username):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(username_header + username)
        greeter = self.client_socket.recv(self.HEADER_LENGTH)
        self.connection_state = CONNECTED
        handler(greeter.decode('utf-8'))

    def send_message(self, payload):
        message = payload.encode('utf-8')
        message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + message)

    def listen(self, handler):
        def _target(hand):
            while self.connection_state == CONNECTED:
                try:
                    while True:
                        username_header = self.client_socket.recv(self.HEADER_LENGTH)
                        if not len(username_header):
                            print('Connection closed by the server')
                            sys.exit()

                        username_length = int(username_header.decode('utf-8').strip())
                        username = self.client_socket.recv(username_length).decode('utf-8')

                        message_header = self.client_socket.recv(self.HEADER_LENGTH)
                        message_length = int(message_header.decode('utf-8').strip())
                        message = self.client_socket.recv(message_length).decode('utf-8')
                        if hand(username, message) == 'close':
                            break

                except IOError as e:
                    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                        print('Reading error: {}'.format(str(e)))

        thread = Thread(target=_target, args=[handler])
        thread.daemon = True
        thread.start()

    def disconnect(self, handler):
        print("disconnecting")
        self.connection_state = DISCONNECTED
        self.send_message("@close")
        handler(self.client_socket.recv(self.HEADER_LENGTH).decode('utf-8'))

if __name__ == '__main__':
    print("=== Test execution of TCP client ===")
    print("Creating two clients...")
    alice = Client("Alice")
    print("Created Alice!")
    bob = Client("Bob")
    print("Created Bob!")

    print("* Starting Alice and Bob... *")
    try:
        alice.start()
        bob.start()
    except:
        print("Error with the server!\nExiting...")
        sys.exit(1)

    print("* Setting Alice to listen... *")
    try:
        alice.listen(print, 100)
        time.sleep(1)
    except:
        print("Error setting Alice to listen!\nExiting...")
        sys.exit(1)
    print("Alice set to listen succesfuly!")

    print("* Sending a messages from Bob to Alice... *")
    try:
        bob.send_message("Hello Alice!")
        time.sleep(1)
        #alice.listen(print)
        #time.sleep(1)
        bob.send_message("Bye Alice!")
    except:
        print("Error sending message from Alice to Bob\nExiting...")
        sys.exit(1)
    print("Message sent succesfuly!")

