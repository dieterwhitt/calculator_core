'''
dieter whittingham
january 22, 2024
server.py
socket server
'''



import socket
import threading
from datetime import datetime

# ubuntu server
import os, stat
from dotenv import load_dotenv

load_dotenv()

# sets server ip address to my public ip address
# realistically this would be a static ip
SERVER = os.getenv('SERVER')
PORT = int(os.getenv('PORT'))
ADDR = (SERVER, PORT)
# 8 byte header - tells us the length of the upcoming message
HEADER = 8
FORMAT = 'utf-8'
# disconnect message to indicate disconnections
DISCONNECT_MESSAGE = '!d'
NAME_HEADER = '@@@'

# make new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# makes a directory if it doesn't exist yet, and gives owner permissions
def make_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        # give the server rwx permissions
        os.chmod(path, stat.S_IRWXO)

# getting the user of whoever sent a message.
# all messages have the format name@@@message
# returns (name, message)
def split_message(msg):
    # get index of name end
    header_index = msg.find(NAME_HEADER)
    if header_index != -1:
        return {"name": msg[:header_index], "message": msg[header_index + 3:]}
    else:
        return {"name": "", "message": msg}

# logging message
# should sort by name, if name not found then by ip address
def log_message(msg, ip):
    try:
        data = split_message(msg)
        # if user not found, replace name with ip address
        name = data["name"]
        msg_content = data["message"]
        if not name:
            name = "unknown user"
        now = datetime.now()
        list_log = f'{name} at {now.strftime("%d/%m/%Y %H:%M:%S")} from 
                {ip}: {msg_content}'
        print(list_log)
        # write message to file
        # only works if logs folder has read and write permissions
        # should be in logs folder and in a name folder
        # need 2 files: raw (raw text) and list (lists user, time, ip)

        dirpath = ""
        # creating directory for this user
        if data["name"]: 
            # name was found: use the name
            dirpath = f"/logs/{name}"
        else:
            # name wasn't found, use ip address
            dirpath = f"/logs/{ip}"

        # logging to list file
        with open(dirpath + "/list.txt", 'a+') as loglist:
            loglist.write(list_log)
        
        with open(dirpath + "/raw.txt", "a+") as lograw:
            lograw.write(msg_content)

    except Exception as e:
        print(f'[ERROR] couldn\'t log user input: {e}')

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
        # ensure that the message has some content, since upon connection a "blank" message is sent
        if msg_length:
            msg_length = int(msg_length)
            # can now put the msg length for the number of bytes received in the second message
            msg = conn.recv(msg_length).decode(FORMAT)
            # check disconnect
            if msg == DISCONNECT_MESSAGE:
                # stop while loop
                connected = False
            log_message(msg, clientaddr[0])
            
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

if __name__ == "__main__":
    print(f'[STARTING] starting server')
    # create logs folder if doesn't exist yet
    make_directory("logs")
    start()
