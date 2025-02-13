#client code
import socket

def udp_client(server_ip='127.0.0.1', server_port=12345):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        try:
            # Get user input to send to the server
            message = input("Enter message to send (or 'exit' to quit): ")
            if message.lower() == 'exit':
                print("Exiting client.")
                break

            # Send message to the server
            client_socket.sendto(message.encode(), (server_ip, server_port))
            
            # Wait for acknowledgment from the server
            ack, _ = client_socket.recvfrom(1024)
            print(f"Server: {ack.decode()}")

        except KeyboardInterrupt:
            print("\nClient shutting down.")
            break
        except Exception as e:
            print(f"Error: {e}")

    client_socket.close()

if __name__ == "__main__":
    udp_client()