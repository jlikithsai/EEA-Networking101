import socket
import threading
import sys
import websockets
import asyncio
import os 
import time 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

IP = socket.gethostbyname(socket.gethostname())
PORT = 80
ADDR = ("",PORT)
HEADER = 1024
FORMAT = "utf-8"

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(True)

class WebSocketServer:
    def __init__(self):
        self.connections = set()  # Store active WebSocket connections

    async def register(self, websocket):
        self.connections.add(websocket)

    async def unregister(self, websocket):
        self.connections.remove(websocket)

    async def handler(self, websocket, path):
        # Register new connection
        await self.register(websocket)
        try:
            # Wait for any message from the client (this is just to keep the connection open)
            await websocket.recv()
        except:
            pass
        finally:
            # Unregister connection when closed
            await self.unregister(websocket)

    def broadcast_reload_notification(self):
        # Broadcast the reload notification to all connected clients
        message = "Content has changed. Please reload the page."
        for connection in self.connections:
            asyncio.create_task(connection.send(message))

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, websocket_server):
        self.websocket_server = websocket_server

    def on_modified(self, event):
        # If any file is modified, notify clients
        if not event.is_directory:
            print(f"File changed: {event.src_path}")
            self.websocket_server.broadcast_reload_notification()

    def on_created(self, event):
        # If a new file is created, notify clients
        if not event.is_directory:
            print(f"New file created: {event.src_path}")
            self.websocket_server.broadcast_reload_notification()

def handle_client(conn,addr):
    try:
        message=conn.recv(HEADER).decode()
        filename=message.split()[1]
        try:
            with open(filename[1:], 'r') as f:
                outputdata = f.read()

            # Send HTTP header for successful request
            conn.send("HTTP/1.1 200 OK\r\n".encode())
            conn.send("Content-Type: text/html\r\n\r\n".encode())

            # Send the content of the requested file to the client
            conn.send(outputdata.encode())
        except IOError:
            # If file is not found, send HTTP 404 error
            conn.send("HTTP/1.1 404 Not Found\r\n".encode())
            conn.send("Content-Type: text/html\r\n\r\n".encode())
            conn.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
    except Exception as e:
        print(f"Error handling request: {e}")
    finally :
        conn.close()
    
def start():
    print("server is ready ")   
    print(f"server connected to {server}")
    websocket_server = WebSocketServer()
    websocket_thread = threading.Thread(target=asyncio.run, args=(start_websocket_server(websocket_server),))
    websocket_thread.daemon = True
    websocket_thread.start()
    while True:
     conn,addr=server.accept()
     
     thread = threading.Thread(target = handle_client,args=(conn,addr))
    #  conn.send("Welcome to the server")
     thread.start()
     print(f"active connections {threading.activeCount() - 1}")

async def start_websocket_server(websocket_server):
    async with websockets.serve(websocket_server.handler, "localhost", 8765):
        print("WebSocket server started...")
        await asyncio.Future()  # Keep the server running forever

start()
sys.exit()