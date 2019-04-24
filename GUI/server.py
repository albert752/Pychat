import socket
import select
import datetime
from pprint import pprint as pp


class server:
    def __init__(self):
        self.HEADER_LENGTH = 10

        self.IP = "127.0.0.1"
        self.PORT = 1234

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen()

        self.sockets_list = [self.server_socket]
        self.clients = {self.server_socket: {'header': b'1         ', 'data': b'@'}}
        self.forbidden = [b'broadcast', b'list', b'close', b'time']

        print(f'Listening for connections on {self.IP}:{self.PORT}...')

    def receive_message(self, client_socket):
        try:
            message_header = client_socket.recv(self.HEADER_LENGTH)
            if not len(message_header):
                return False
            message_length = int(message_header.decode('utf-8').strip())
            return {'header': message_header, 'data': client_socket.recv(message_length)}

        except:
            return False

    def _compute_header(self, message):
        if isinstance(message, str):
            message = message.encode('utf-8')
        return {'header': f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8'), 'data': message}

    def is_forb(self, aux):
        if aux in self.forbidden or aux[0] == '@':
            return True
        return False


    def send_message(self, message, src=None, dst='broadcast'):
        ''''
        Send a message
        :param message: List containing {'header': header, 'data': data} or just the string.
        :param src: Dict containing [self.user_name_header, user_name] from witch the massage was sent.
        :param dst: Dict containing [self.user_name_header, user_name] from witch message has to be sent.
        '''
        src = self._compute_header(src)
        message = self._compute_header(message)

        if dst == 'broadcast':

            for client_socket in self.clients:
                if client_socket != self.notified_socket and client_socket != self.server_socket:
                    print(f'Sent a message from {self.user["data"].decode("utf-8")} '
                          f'to {self.clients[client_socket]["data"].decode("utf-8")}')
                    client_socket.send(src['header'] + src['data'] + message['header'] + message['data'])
        else:
            dst = self._compute_header(dst)
            for client_socket in self.clients:
                if self.clients[client_socket] == dst:
                    client_socket.send(src['header'] + src['data'] + message['header'] + message['data'])
                    break

    def users_to_string(self):
        message = "Registered users: "
        for client in self.clients.values():
            message += '\t\n' + client['data'].decode('utf-8')
        return message

    def run(self):
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

            for self.notified_socket in read_sockets:

                if self.notified_socket == self.server_socket:

                    client_socket, client_address = self.server_socket.accept()
                    self.user = self.receive_message(client_socket)

                    unique = True
                    for sock in self.clients.values():
                        if sock['data'] == self.user['data']:
                            unique = False
                            break
                    if not unique or self.is_forb(self.user['data']):
                        print("Refused new connection")
                        client_socket.send("Refused!  ".encode('utf-8'))
                        client_socket.close()
                    else:

                        if self.user is False:
                            continue
                        self.sockets_list.append(client_socket)
                        self.clients[client_socket] = self.user
                        print('Accepted new connection from {}:{}, self.username: {}'.format(*client_address,
                                                                                        self.user['data'].decode('utf-8')))
                        client_socket.send("Connected!".encode('utf-8'))
                else:

                    message = self.receive_message(self.notified_socket)

                    if message is False:
                        print('Closed connection from: {}'.format(self.clients[self.notified_socket]['data'].decode('utf-8')))
                        self.sockets_list.remove(self.notified_socket)
                        del self.clients[self.notified_socket]
                        continue

                    self.user = self.clients[self.notified_socket]
                    print(f'Received message from {self.user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                    payload = message["data"].decode("utf-8")

                    if payload[0] == '@':
                        if payload[1:] == "list":
                            self.send_message(self.users_to_string(), src=self.clients[self.server_socket]['data'],
                                         dst=self.clients[self.notified_socket]['data'])

                        elif payload[1:] == "close":
                            self.notified_socket.send("ByeBye  :)".encode('utf-8'))
                            print('Closed connection from: {}'.format(self.clients[self.notified_socket]['data'].decode('utf-8')))
                            self.sockets_list.remove(self.notified_socket)
                            del self.clients[self.notified_socket]


                        elif payload[1:] == "time":
                            self.send_message(str(datetime.datetime.now()), src=self.clients[self.server_socket]['data'],
                                         dst=self.clients[self.notified_socket]['data'])

                        else:
                            self.user_dst = payload[1:].split(' ', 1)[0]
                            print("It is a private message to " + self.user_dst)
                            self.send_message(payload, src=self.user['data'], dst=self.user_dst)

                    else:
                        self.send_message(message['data'], src=self.user['data'])

            for self.notified_socket in exception_sockets:
                self.sockets_list.remove(self.notified_socket)
                del self.clients[self.notified_socket]


if __name__ == '__main__':
    s = server()
    s.run()
