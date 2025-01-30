# Final Showdown 

In this assignment, you will implement a streaming video server and client that communicate using the Real-Time
Streaming Protocol (RTSP) and send data using the Real-time Transfer Protocol (RTP). Your task is to
implement the RTSP protocol in the client and implement the RTP packetization in the server.
We will provide you code that implements the RTSP protocol in the server, the RTP de-packetization in
the client, and takes care of displaying the transmitted video. 

# Code

## Client, ClientLauncher
The `ClientLauncher` starts the `Client` and the user interface which you use to send RTSP commands and which is used to display the video. In the `Client` class, you will need to implement the actions that are taken when the buttons are pressed. You do not need to modify the `ClientLauncher` module.

## ServerWorker, Server
These two modules implement the server which responds to the RTSP requests and streams back the video. The RTSP interaction is already implemented, and the `ServerWorker` calls methods from the `RtpPacket` class to packetize the video data. You do not need to modify these modules.

## RtpPacket
This class is used to handle the RTP packets. It has separate methods for handling the received packets at the client side, and you do not need to modify them. The `Client` also de-packetizes (decodes) the data, and you do not need to modify this method. You will need to complete the implementation of video data RTP-packetization (which is used by the server).

## VideoStream
This class is used to read video data from the file on disk. You do not need to modify this class.

# Running the Code

After completing the code, you can run it as follows:

First, start the server with the command:
where `server_port` is the port your server listens to for incoming RTSP connections. The standard RTSP port is 554, but you will need to choose a port number greater than 1024.

Then, start the client with the command:
where:
- `server_host` is the name of the machine where the server is running.
- `server_port` is the port where the server is listening on.
- `RTP_port` is the port where the RTP packets are received.
- `video_file` is the name of the video file you want to request (we have provided one example file `movie.Mjpeg`). 

The file format is described in the Appendix section.

The client opens a connection to the server and pops up a window.

You can send RTSP commands to the server by pressing the buttons. A normal RTSP interaction goes as follows:
1. The client sends **SETUP**. This command is used to set up the session and transport parameters.
2. The client sends **PLAY**. This command starts the playback.
3. The client may send **PAUSE** if it wants to pause during playback.
4. The client sends **TEARDOWN**. This command terminates the session and closes the connection.

The server always replies to all the messages that the client sends. The code 200 means that the request was successful while the codes 404 and 500 represent **FILE_NOT_FOUND** error and **connection error**, respectively. 

