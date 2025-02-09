import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 8080))
    s.sendall(b"Add five plus nine 6/4")
    data = s.recv(1024)

print('Received', data.decode())
