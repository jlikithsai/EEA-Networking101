from tkinter import *
import tkinter.messagebox as tkMessageBox
from PIL import Image, ImageTk
import socket, threading, os, sys
from RtpPacket import RtpPacket

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"

class Client:
    INIT = 0
    READY = 1
    PLAYING = 2
    state = INIT

    SETUP = 0
    PLAY = 1
    PAUSE = 2
    TEARDOWN = 3

    def __init__(self, master, serveraddr, serverport, rtpport, filename):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.handler)
        self.createWidgets()
        
        self.serverAddr = serveraddr
        self.serverPort = int(serverport)
        self.rtpPort = int(rtpport)
        self.fileName = filename
        
        self.rtspSeq = 0
        self.sessionId = 0
        self.requestSent = -1
        self.teardownAcked = 0
        self.frameNbr = 0
        self.playEvent = threading.Event()  # Initialize here
        
        self.connectToServer()
        threading.Thread(target=self.recvRtspReply, daemon=True).start()  # Start listening for RTSP replies

    def createWidgets(self):
        self.setup = Button(self.master, text="Setup", command=self.setupMovie)
        self.setup.grid(row=1, column=0)

        self.start = Button(self.master, text="Play", command=self.playMovie)
        self.start.grid(row=1, column=1)

        self.pause = Button(self.master, text="Pause", command=self.pauseMovie)
        self.pause.grid(row=1, column=2)

        self.teardown = Button(self.master, text="Teardown", command=self.exitClient)
        self.teardown.grid(row=1, column=3)

        self.label = Label(self.master)
        self.label.grid(row=0, column=0, columnspan=4)

    def setupMovie(self):
        if self.state == self.INIT:
            self.sendRtspRequest(self.SETUP)

    def exitClient(self):
        self.sendRtspRequest(self.TEARDOWN)
        self.master.destroy()
        try:
            os.remove(CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT)
        except FileNotFoundError:
            pass

    def pauseMovie(self):
        if self.state == self.PLAYING:
            self.sendRtspRequest(self.PAUSE)

    def playMovie(self):
        if self.state == self.READY:
            threading.Thread(target=self.listenRtp, daemon=True).start()
            self.playEvent.clear()
            self.sendRtspRequest(self.PLAY)

    def listenRtp(self):
        """Listens for RTP packets and updates the video frame."""
        while not self.playEvent.is_set():
            try:
                data = self.rtpSocket.recv(20480)
                if data:
                    rtpPacket = RtpPacket()
                    rtpPacket.decode(data)
                    currFrameNbr = rtpPacket.seqNum()

                    if currFrameNbr > self.frameNbr:  # Avoid duplicate frames
                        self.frameNbr = currFrameNbr
                        self.updateMovie(self.writeFrame(rtpPacket.getPayload()))
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error in listenRtp: {e}")
                break

    def writeFrame(self, data):
        cachename = CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT
        with open(cachename, "wb") as file:
            file.write(data)
        return cachename

    def updateMovie(self, imageFile):
        try:
            photo = ImageTk.PhotoImage(Image.open(imageFile))
            self.label.configure(image=photo)
            self.label.image = photo
        except Exception as e:
            print(f"Error updating frame: {e}")

    def connectToServer(self):
        """Connects to the RTSP server."""
        self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.rtspSocket.connect((self.serverAddr, self.serverPort))
            print(f"Connected to server at {self.serverAddr}:{self.serverPort}")
        except:
            tkMessageBox.showwarning('Connection Failed', f'Connection to {self.serverAddr} failed.')

    def sendRtspRequest(self, requestCode):
        """Sends an RTSP request to the server."""
        self.rtspSeq += 1
        requestType = ["SETUP", "PLAY", "PAUSE", "TEARDOWN"][requestCode]
        request = f"{requestType} {self.fileName} RTSP/1.0\nCSeq: {self.rtspSeq}\n"

        if requestCode == self.SETUP:
            request += f"Transport: RTP/UDP; client_port= {self.rtpPort}\n"
        else:
            request += f"Session: {self.sessionId}\n"

        self.rtspSocket.send(request.encode())
        self.requestSent = requestCode

    def recvRtspReply(self):
        """Receives and processes RTSP replies."""
        while True:
            try:
                reply = self.rtspSocket.recv(1024).decode()
                if reply:
                    self.parseRtspReply(reply)
                if self.requestSent == self.TEARDOWN:
                    self.rtspSocket.shutdown(socket.SHUT_RDWR)
                    self.rtspSocket.close()
                    break
            except Exception as e:
                print(f"Error receiving RTSP reply: {e}")
                break

    def parseRtspReply(self, data):
        """Parses the RTSP server reply."""
        lines = data.split('\n')
        seqNum = int(lines[1].split(' ')[1])

        if seqNum == self.rtspSeq:
            session = int(lines[2].split(' ')[1])
            if self.sessionId == 0:
                self.sessionId = session

            if self.sessionId == session:
                if int(lines[0].split(' ')[1]) == 200:
                    if self.requestSent == self.SETUP:
                        self.state = self.READY
                        self.openRtpPort()
                    elif self.requestSent == self.PLAY:
                        self.state = self.PLAYING
                    elif self.requestSent == self.PAUSE:
                        self.state = self.READY
                        self.playEvent.set()
                    elif self.requestSent == self.TEARDOWN:
                        self.state = self.INIT
                        self.teardownAcked = 1

    def openRtpPort(self):
        """Opens the RTP port for receiving video data."""
        self.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rtpSocket.settimeout(0.5)
        try:
            self.rtpSocket.bind(("", self.rtpPort))
            print(f"RTP socket bound to port {self.rtpPort}")
        except:
            tkMessageBox.showwarning('Unable to Bind', f'Unable to bind PORT={self.rtpPort}')

    def handler(self):
        """Handles window close event."""
        self.pauseMovie()
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            self.exitClient()
        else:
            self.playMovie()

if __name__ == "__main__":
    root = Tk()
    app = Client(root, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    root.mainloop()

