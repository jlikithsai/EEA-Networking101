import sys
import socket
from ServerWorker import ServerWorker

class Server:    
    def main(self):
        # Set a default port in case no argument is provided
        SERVER_PORT = 12000  # Default RTSP port
        
        # Try getting the port from command-line arguments
        if len(sys.argv) > 1:
            try:
                SERVER_PORT = int(sys.argv[1])
            except ValueError:
                print("[Error] Invalid port number. Using default port 8554.")
        
        # Create and bind RTSP socket
        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtspSocket.bind(('', SERVER_PORT))
        rtspSocket.listen(5)        
        print(f"Server is listening on port {SERVER_PORT}...")

        # Receive client info (address, port) through RTSP/TCP session
        while True:
            clientInfo = {}
            clientInfo['rtspSocket'] = rtspSocket.accept()
            ServerWorker(clientInfo).run()        

if __name__ == "__main__":
    (Server()).main()



