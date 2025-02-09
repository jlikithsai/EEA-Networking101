import sys, socket
from ServerWorker import ServerWorker

class Server:	
    
    def main(self):
        try:
            # Try to get the server port from the command-line arguments.
            SERVER_PORT = int(sys.argv[1])
        except:
            # If the user did not supply a port number, print usage instructions.
            print("[Usage: Server.py Server_port]\n")
            return  # Exit if no valid port is provided
        
        # Create a TCP socket for the RTSP connection.
        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to all available network interfaces on the specified port.
        rtspSocket.bind(('', SERVER_PORT))
        # Start listening for incoming connections. The argument 5 indicates the maximum
        # number of queued connections.
        rtspSocket.listen(5)        

        # Infinite loop to continually accept new client connections.
        while True:
            clientInfo = {}
            # Accept a new connection. This call returns a tuple: (client_socket, client_address)
            clientInfo['rtspSocket'] = rtspSocket.accept()
            # Create a ServerWorker for this client and run it.
            # The ServerWorker is responsible for handling the RTSP protocol
            # (e.g., SETUP, PLAY, PAUSE, TEARDOWN requests) for that client.
            ServerWorker(clientInfo).run()		

if __name__ == "__main__":
    # Instantiate the server and start its main function.
    (Server()).main()
