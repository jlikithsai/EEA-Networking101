import socket

def start_client(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        while True:
            expression = input("Enter a mathematical expression (or 'exit' to quit): ")
            if expression.lower() == 'exit':
                break
            client.send(expression.encode())
            response = client.recv(1024).decode()
            print(f"Result: {response}")
    except:
        print("Disconnected from server")
    finally:
        client.close()

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9999
    start_client(HOST, PORT)