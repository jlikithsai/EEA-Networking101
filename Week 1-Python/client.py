import socket
import threading

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HEADER =64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
FORMAT = "utf-8"

client.connect(ADDR)
print(f"client is connected to {SERVER}")
print(f"{client.recv(1024)}")
def send(msg):
    message=msg.encode(FORMAT)
    msg_len=len(message)
    send_len=str(msg_len).encode(FORMAT)
    send_len+=b' ' * (HEADER - len(send_len))      ## padding 
    client.send(send_len)
    client.send(message)

statement = input(" \n")
# print(statement)
send(statement)
    