import socket
import re  # For parsing math problems

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

def parse_and_calculate(message):
    operators = ['+', '-', '*', '/']
    for operator in operators:
        if operator in message:
            parts = re.split(rf'\{operator}', message)  # Split by the operator
            if len(parts) == 2:
                try:
                    num1 = int(re.search(r'\d+', parts[0]).group())  # First number
                    num2 = int(re.search(r'\d+', parts[1]).group())  # Second number
                except (ValueError, AttributeError):
                    return "Error: Could not parse numbers."

                # Perform calculation
                if operator == '+':
                    return num1 + num2
                elif operator == '-':
                    return num1 - num2
                elif operator == '*':
                    return num1 * num2
                elif operator == '/':
                    return num1 // num2 if num2 != 0 else "Error: Division by zero"
    return "Error: No valid operator found."

print(f"[STARTING] Server is starting on {SERVER}:{PORT}")
while True:
    conn, addr = server.accept()
    print(f"[NEW CONNECTION] {addr} connected.")

    msg = conn.recv(1024).decode('utf-8')
    print(f"[CLIENT] {msg}")
    result = parse_and_calculate(msg)
    conn.send(str(result).encode('utf-8'))
    conn.close()
