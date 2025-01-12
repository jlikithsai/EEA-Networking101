import socket 
import select

HEADER = 64
IP = "127.0.0.1"
PORT = 5050
ADDR = (IP,PORT)

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt( socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server_socket.bind(ADDR)
server_socket.listen()

sockets_list=[server_socket]
clients={}

def recv_msg(client_socket):
    try:
        msg_header=client_socket.recv(HEADER)
        if not len(msg_header):
            return False
    
        msg_length = int(msg_header.decode("utf-8").strip())
        return {"header" : msg_header , "data" : client_socket.recv(msg_length)}
    
    except :
        return False
    
while True:
    read_sockets, _,exception_sockets=select.select(sockets_list,[],sockets_list)

    for notified_sockets in read_sockets:
        if notified_sockets == server_socket:
            client_socket,client_address = server_socket.accept()

            user = recv_msg(client_socket)
            if user is False:
             continue
        
            sockets_list.append(client_socket)
            clients[client_socket]=user
        
            print(f"accepted the new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

        else:
            msg=recv_msg(notified_sockets)
            if msg is False:
                print(f"closed connection from {clients[notified_sockets]['data'].decode('utf-8')}")
                
        user = clients[notified_sockets]
        print(f"received message from {user['data'].decode("utf-8")} :{msg['data'].decode('utf-8')}")

        for client_sockets in clients:
            
            if client_socket != notified_sockets :
                client_socket.send(user['header'] + user['data'] + msg['header'] + msg['data'])

    for notified_sockets in exception_sockets:
        sockets_list.remove(notified_sockets)
        del clients[notified_sockets]
        
        
        
