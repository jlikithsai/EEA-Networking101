import socket
client = socket.socket()
try:
    client.connect(("127.0.0.1", 9992))
    print(f"[INFO] Connected to the server at ('127.0.0.1','9992')")

    while True:    
        user_input = input()
        client.send(bytes(user_input, 'utf-8'))

        print(client.recv(1024).decode())
except Exception as e:
    print(f"[ERROR] An error occurred: {e}")
finally:
    client.close()
    print("[INFO] Disconnected from the server.")