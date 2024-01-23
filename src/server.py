'''
dieter whittingham
january 22, 2024
server.py
socket server
'''

import socket
import threading

# server port
PORT = 9999
# gets my ip address
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
# 8 byte header - tells us the length of the upcoming message
HEADER = 8
FORMAT = 'utf-8'
#disconnect message to indicate disconnections
DISCONNECT_MESSAGE = '!disconnect'

# make new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# handling individual communication between client and server
def handle_client(conn, addr):
    print(f'new connection: {addr} connected.')

    connected = True
    while connected:
        # blocking line: this line won't be passed until a message is received
        # this is why it's necessary to run threads so that we can handle multiple
        # processes at once
        # here we're taking the first message which will be the header
        # containing the length of the next message
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        # can now put the msg length for the number of bytes received in the second message
        msg = conn.recv(msg_length).decode(FORMAT)
        # check disconnect
        if msg == DISCONNECT_MESSAGE:
            # stop while loop
            connected = False
        print(f'[{addr}]: {msg}')
    # while loop ended: close connection
    conn.close()

# starting server
# handling new connections
def start():
    server.listen()
    print(f'[LISTENING] server is listening on {SERVER}')
    while True:
        # waiting for server connections
        # conn is the socket object that allows us to send information back to the client
        # addr is the ip address and port that connected
        conn, addr = server.accept()
        # new connection: pass the connection to handle_client in a new thread
        # this thread will run parallel with the server waiting for connections
        thread = threading.thread(target=handle_client, args=(conn, addr))
        thread.start()
        # print number of connections
        print(f'active connections: {threading.activeCount() - 1}')


print(f'[STARTING] starting server')
start()
