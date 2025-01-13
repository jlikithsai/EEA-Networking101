import socket
import threading


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


IP = "0.0.0.0" 
PORT = 80
ADDR = (IP, PORT)


server.bind(ADDR)

def handle_client(data, client_address):
    if data:
        data = data.decode("utf-8")
        print(f"Message from client: {data}")
        response = "Acknowledging to the message received."
        response = response.encode("utf-8")
        server.sendto(response, client_address)
    else:
        print("Message not received from client")


def start():
    print("Server started, waiting for clients...")
    while True:
        
        data, client_address = server.recvfrom(1024)
        print(f"Received message from {client_address}")
        
        
        threading.Thread(target=handle_client, args=(data, client_address)).start()

start()
