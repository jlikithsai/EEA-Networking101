import socket

client = socket.socket()

client.connect(("127.0.0.1", 9995))

user_input = input()

client.send(bytes(user_input, 'utf-8'))

print(client.recv(1024).decode())