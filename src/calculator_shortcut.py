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

def handleKeyPress(key):
    print(str(key))
# main execution
if __name__ == '__main__':
    #creating listener object
    listener = keyboard.Listener(on_press=handleKeyPress)
    listener.start()
    #getting input
    input()
    #open windows calculator
    if sys.platform == 'win32':
        os.Startfile('C:\WINDOWS\system32\calc.exe')

