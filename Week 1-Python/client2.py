import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 8080))
    s.sendall(b"Cal 8*109")
    data = s.recv(1024)

print('received', data.decode())