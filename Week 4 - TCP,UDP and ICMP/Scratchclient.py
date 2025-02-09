import socket

def send_message(server_ip, server_port, message):
    """Send a message to the UDP server and wait for acknowledgment."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        try:
            # Send message to server
            client_socket.sendto(message.encode(), (server_ip, server_port))
            print(f"Sent message to server {server_ip}:{server_port}")
            
            # Receive acknowledgment
            ack, _ = client_socket.recvfrom(1024)
            print(f"Server acknowledgment: {ack.decode()}")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace '127.0.0.1' and '8080' with server IP and port
    server_ip = "127.0.0.1"
    server_port = 8080
    message = input("Enter a message to send to the server: ")
    
    send_message(server_ip, server_port, message)
