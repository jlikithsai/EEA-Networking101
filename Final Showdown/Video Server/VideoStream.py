class VideoStream:
	def __init__(self, filename):
		self.filename = filename
		try:
			self.file = open(filename, 'rb')
		except:
			raise IOError
		self.frameNum = 0
		
	def nextFrame(self):
		"""Get next frame."""
		data = self.file.read(5) # Get the framelength from the first 5 bits
		if data: 
			framelength = int(data)
							
			# Read the current frame
			data = self.file.read(framelength)
			self.frameNum += 1
		return data
		
	def frameNbr(self):
		"""Get frame number."""
		return self.frameNum
	
# import cv2

# class VideoStream:
#     def __init__(self, filename):
#         self.filename = filename
#         self.video = cv2.VideoCapture(filename)
#         if not self.video.isOpened():
#             raise IOError(f"Error opening video file: {filename}")
#         self.frameNum = 0

#     def nextFrame(self):
#         """Get the next video frame."""
#         # Read the next frame from the video file
#         ret, frame = self.video.read()
#         if not ret:
#             return None  # No more frames to read

#         self.frameNum += 1
#         # Encode frame as a byte stream in JPEG format
#         encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()

#         # Return the frame length prefixed to the frame bytes (as expected by RTP)
#         framelength = len(encoded_frame).to_bytes(5, byteorder='big')
#         return framelength + encoded_frame

#     def frameNbr(self):
#         """Return the current frame number."""
#         return self.frameNum

# if __name__ == "__main__":
#     stream = VideoStream("video1.mp4")
    
#     while True:
#         frame_data = stream.nextFrame()
#         if not frame_data:
#             break
#         print(f"Streaming frame {stream.frameNbr()}, length: {len(frame_data)} bytes")
