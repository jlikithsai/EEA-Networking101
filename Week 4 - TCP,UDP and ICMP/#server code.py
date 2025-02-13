#server code

import socket

def start_udp_server(ip=socket.gethostbyname(socket.gethostname()), port=12345):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the address and port
    server_socket.bind((ip, port))
    print(f"UDP Server is listening on {ip}:{port}")

    while True:
        try:
            # Wait for a message from the client
            message, client_address = server_socket.recvfrom(1024)
            print(f"Received from {client_address}: {message.decode()}")

            # Send acknowledgment back to the client
            ack_message = "ACK: Message received"
            server_socket.sendto(ack_message.encode(), client_address)
            print(f"Sent acknowledgment to {client_address}")

        except KeyboardInterrupt:
            print("\nServer shutting down.")
            break
        except Exception as e:
            print(f"Error: {e}")

    server_socket.close()

if __name__ == "__main__":
    start_udp_server()