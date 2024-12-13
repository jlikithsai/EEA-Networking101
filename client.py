import socket

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

message = "Please calculate 9*5"
client.send(message.encode('utf-8'))  # Send math problem to server
response = client.recv(1024).decode('utf-8')  # Receive result
print(f"[SERVER RESPONSE] {response}")
client.close()
