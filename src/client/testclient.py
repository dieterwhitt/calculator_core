'''
dieter whittingham
jan 22 2024
socket test client file
'''

import socket

HEADER = 8
PORT = 9999
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"
# no static ip: add the ip manually
SERVER = ""
ADDR = (SERVER, PORT)

# set up client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server
client.connect(ADDR)

# way to send message
def send(msg_str):
    # encoding the message with utf-8
    message = msg_str.encode(FORMAT)
    # need to send header, so get length
    msg_length = len(message)
    # encoding the header as a string
    send_length = str(msg_length).encode(FORMAT)
    # need to ensure send_length is 8 bytes long
    # therefore we need to add empty space
    # adding byte representations of spaces
    send_length += b" " * (HEADER - len(send_length))
    # test to see what the header looks like
    # send header
    client.send(send_length)
    # send message
    client.send(message)

# testing
send("hello world!")
connected = True
while connected:
    x = input("enter a message: ")
    send(x)
    if(x == DISCONNECT_MESSAGE):
        connected = False
        print("you have been disconnected.")
        