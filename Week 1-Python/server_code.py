import socket
import re
import threading

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            
            print(f"Received: {data}")
            response = calculate(data)
            client_socket.send(response.encode())
    except:
        print("Client disconnected")
    finally:
        client_socket.close()

def calculate(expression):
    try:
        # Extract the mathematical expression using regex
        match = re.search(r'(\d+)\s*([\+\-\*/])\s*(\d+)', expression)
        if not match:
            return "Error: Invalid expression"
        
        operand1, operator, operand2 = match.groups()
        operand1 = int(operand1)
        operand2 = int(operand2)
        
        if operator == '+':
            result = operand1 + operand2
        elif operator == '-':
            result = operand1 - operand2
        elif operator == '*':
            result = operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                return "Error: Division by zero"
            result = operand1 / operand2
        else:
            return "Error: Unsupported operator"
        
        return str(int(result)) if operator != '/' else str(result)
    except Exception as e:
        return f"Error: {str(e)}"
    
def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9999
    start_server(HOST, PORT)
