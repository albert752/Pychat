import socket
import select
import datetime
from pprint import pprint as pp

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {server_socket: {'header': b'1         ', 'data': b'@'}}
forbidden = [b'broadcast']

print(f'Listening for connections on {IP}:{PORT}...')


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False


def _compute_header(message):
    if isinstance(message, str):
        message = message.encode('utf-8')
    return {'header': f"{len(message):<{HEADER_LENGTH}}".encode('utf-8'), 'data': message}


def is_forb(aux):
    if aux in forbidden or aux[0] == '@':
        return True
    return False


def send_message(message, src=None, dst='broadcast'):
    ''''
    Send a message
    :param message: List containing {'header': header, 'data': data} or just the string.
    :param src: Dict containing [user_name_header, user_name] from witch the massage was sent.
    :param dst: Dict containing [user_name_header, user_name] from witch message has to be sent.
    '''
    src = _compute_header(src)
    message = _compute_header(message)

    if dst == 'broadcast':

        for client_socket in clients:
            if client_socket != notified_socket and client_socket != server_socket:
                print(f'Sent a message from {user["data"].decode("utf-8")} '
                      f'to {clients[client_socket]["data"].decode("utf-8")}')
                client_socket.send(src['header'] + src['data'] + message['header'] + message['data'])
    else:
        dst = _compute_header(dst)
        for client_socket in clients:
            if clients[client_socket] == dst:
                client_socket.send(src['header'] + src['data'] + message['header'] + message['data'])


def users_to_string():
    message = "Registered users: "
    for client in clients.values():
        message += '\t\n' + client['data'].decode('utf-8')
    return message


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:

        if notified_socket == server_socket:

            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            unique = True
            for sock in clients.values():
                if sock['data'] == user['data']:
                    unique = False
                    break
            if not unique or is_forb(user['data']):
                print("Refused new connection")
                client_socket.send("Refused!  ".encode('utf-8'))
                client_socket.close()
            else:

                if user is False:
                    continue
                sockets_list.append(client_socket)
                clients[client_socket] = user
                print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                                user['data'].decode('utf-8')))
                client_socket.send("Connected!".encode('utf-8'))
        else:

            message = receive_message(notified_socket)

            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            payload = message["data"].decode("utf-8")

            if payload[0] == '@':
                if payload[1:] == "list":
                    send_message(users_to_string(), src=clients[server_socket]['data'],
                                 dst=clients[notified_socket]['data'])
                elif payload[1:] == "close":
                    notified_socket.send("ByeBye  :)".encode('utf-8'))
                    print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                elif payload[1:] == "time":
                    send_message(str(datetime.datetime.now()), src=clients[server_socket]['data'],
                                 dst=clients[notified_socket]['data'])
                else:
                    user_dst = payload[1:].split(' ', 1)[0]
                    print("It is a private message to " + user_dst)
                    # user_message = payload[1:].split(' ', 1)[1]
                    send_message(payload, src=user['data'], dst=user_dst)

            else:
                send_message(message['data'], src=user['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
