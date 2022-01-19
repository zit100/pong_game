import msvcrt
import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = '0.0.0.0'


def print_client_sockets(client_sockets):
    print("clients connected:")
    for c in client_sockets:
        print("\t", c.getpeername())


def client_sockets_can_read(client_sockets, wlist):
    for c in client_sockets:
        if c not in wlist:
            return False
    return True


print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")

client_sockets = []
messages_to_send = []

while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            print_client_sockets(client_sockets)
        else:
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            if data == "":
                print("Connection closed from:", current_socket.getpeername())
                client_sockets.remove(current_socket)
                current_socket.close()
                print_client_sockets(client_sockets)
            else:
                messages_to_send.append((current_socket, data))
    for message in messages_to_send:
        current_socket, data = message
        if client_sockets_can_read(client_sockets, wlist):
            print(current_socket.getpeername(), "sent:", data)
            for c in client_sockets:
                if c.getpeername() == current_socket.getpeername():
                    continue
                c.send(data.encode())
            messages_to_send.remove(message)

server_socket.close()