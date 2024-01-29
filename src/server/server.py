'''
dieter whittingham
january 22, 2024
server.py
socket server
'''

import socket
import threading
from datetime import datetime

# server port
PORT = 9999
# sets server ip address to my public ip address
# realistically this would be a static ip
SERVER = '10.32.153.179'
ADDR = (SERVER, PORT)
# 8 byte header - tells us the length of the upcoming message
HEADER = 8
FORMAT = 'utf-8'
#disconnect message to indicate disconnections
DISCONNECT_MESSAGE = '!d'

# make new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# handling individual communication between client and server
def handle_client(conn, clientaddr):
    connectTime = datetime.now()
    print(f'[NEW CONNECTION]: {clientaddr} connected at {connectTime.strftime("%d/%m/%Y %H:%M:%S")}.')
    connected = True
    while connected:
        # blocking line: this line won't be passed until a message is received
        # this is why it's necessary to run threads so that we can handle multiple
        # processes at once
        # here we're taking the first message which will be the header
        # containing the length of the next message
        msg_length = conn.recv(HEADER).decode(FORMAT)
        #ensure that the message has some content, since upon connection a "blank" message is sent
        if msg_length:
            msg_length = int(msg_length)
            # can now put the msg length for the number of bytes received in the second message
            msg = conn.recv(msg_length).decode(FORMAT)
            # check disconnect
            if msg == DISCONNECT_MESSAGE:
                # stop while loop
                connected = False
            # print message with current date and time
            try:
                now = datetime.now()
                print(f'[{now.strftime("%d/%m/%Y %H:%M:%S")} from {clientaddr}: {msg}]')
                # write message to file
                '''
                filepath = f'~/logs/{clientaddr[0]}.txt'
                print('attempting to log to ' + filepath)
                with open(filepath, 'a+') as logfile:
                    logfile.write(f'[{now.strftime("%d/%m/%Y %H:%M:%S")} from {clientaddr}: {msg}]')
                    '''
            except Exception as e:
                print(f'[ERROR] couldn\'t log user input: {e}')
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
        conn, clientaddr = server.accept()
        # new connection: pass the connection to handle_client in a new thread
        # this thread will run parallel with the server waiting for connections
        thread = threading.Thread(target=handle_client, args=(conn, clientaddr))
        thread.start()
        # print number of connections
        print(f'active connections: {threading.active_count() - 1}')

print(f'[STARTING] starting server')
start()
