import socket
import threading
import re
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

HEADER =64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "Disconnected!"
server.bind(ADDR)


def handle_client(conn,addr) :
    print(f"new connection {addr} connected")
    connected =True
    while(connected):
        msg_len=conn.recv(HEADER).decode(FORMAT)
        if msg_len :
         msg_len=int(msg_len)
         msg=conn.recv(msg_len).decode(FORMAT)
         print(f"{type(msg)}")
         msg=str(msg)
         match = re.search(r"(\d+)\s*([+\-*/])\s*(\d+)", msg)
         if match:
        
             num1 = int(match.group(1))
             print (num1)
             operator = match.group(2)
             num2 = int(match.group(3))
             # num3 = int(match.group(4))
       
             if operator == "*":
               print(f"[{ num1 * num2}]")
             elif operator == "+":
               print(num1 + num2)
             elif operator == "-":
               print( num1 - num2)
             elif operator == "/":
              print (num1 / num2)
             else:
               print( "No valid mathematical expression found.")
         
         
         if msg == DISCONNECT_MESSAGE :
                connected = False
        
         print(f"[{addr}]{msg}")
    
    conn.close()

def start():
    server.listen()
    print(f"server is listening to          {SERVER}")
    while True:
        conn,addr=server.accept()
        thread =threading.Thread(target=handle_client,args=(conn,addr))
        conn.send("welcome to the server")
        thread.start()
        print(f"active connections {threading.activeCount() - 1}")
        
print(f"server is starting ")
start()

    