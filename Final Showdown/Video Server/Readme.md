# Additional Info

# The Client

Your first task is to implement the RTSP protocol on the client side. To do this, you need to complete the functions that are called when the user clicks on the buttons on the user interface. You will need to implement the actions for the following request types.

When the client starts, it also opens the RTSP socket to the server. Use this socket for sending all RTSP requests.

## SETUP
- Send SETUP request to the server. You will need to insert the Transport header in which you specify the port for the RTP data socket you just created.
- Read the server’s response and parse the Session header (from the response) to get the RTSP session ID.
- Create a datagram socket for receiving RTP data and set the timeout on the socket to 0.5 seconds.

## PLAY
- Send PLAY request. You must insert the Session header and use the session ID returned in the SETUP response. You must not put the Transport header in this request.
- Read the server's response.

## PAUSE
- Send PAUSE request. You must insert the Session header and use the session ID returned in the SETUP response. You must not put the Transport header in this request.
- Read the server's response.

## TEARDOWN
- Send TEARDOWN request. You must insert the Session header and use the session ID returned in the SETUP response. You must not put the Transport header in this request.
- Read the server's response.

**The Server**

On the server side, you will need to implement the packetization of the video data into RTP packets. You will need to create the packet, set the fields in the packet header and copy the payload (i.e., one video frame) into the packet. 

When the server receives the PLAY-request from the client, the server reads one video frame from the file and creates an RtpPacket-object which is the RTP-encapsulation of the video frame. It then sends the frame to the client over UDP every 50 milliseconds.

For the encapsulation, the server calls the encode function of the RtpPacket class. Your task is to write this function. You will need to do the following: (the letters in parenthesis refer to the fields in the RTP packet format below).

* **Set the RTP-version field (V).** You must set this to 2.
* **Set padding (P), extension (X), number of contributing sources (CC), and marker (M) fields.** These are all set to zero in this lab.
* **Set payload type field (PT).** In this lab we use MJPEG and the type for that is 26.
* **Set the sequence number.** The server gives this the sequence number as the frameNbr argument to the encode function.
* **Set the timestamp using the Python's time module.**
* **Set the source identifier (SSRC).** This field identifies the server. You can pick any integer value you like.

Because we have no other contributing sources (field CC0), the CSRC-field does not exist.

The length of the packet header is therefore 12 bytes, or the first three lines from the diagram below.
 # Optional Excercise 

The user interface on the RTPClient has 4 buttons for the 4 actions. If you compare this to a standard
media player, such as RealPlayer or Windows Media Player, you can see that they have only 3
buttons for the same actions: PLAY, PAUSE, and STOP (roughly corresponding to TEARDOWN).
There is no SETUP button available to the user. Given that SETUP is mandatory in an RTSPinteraction, how would you implement that in a media player? When does the client send the SETUP?
Come up with a solution and implement it. Also, is it appropriate to send TEARDOWN when the
user clicks on the STOP button?
