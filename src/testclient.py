'''
dieter whittingham
jan 22 2024
socket test client file
'''

import socket

HEADER = 8
PORT = 9999
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!disconnect'
# figure this out later
SERVER = '10.32.120.165'
ADDR = (SERVER, PORT)

# set up client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server
client.connect(ADDR)