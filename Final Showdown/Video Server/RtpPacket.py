import sys
from time import time
HEADER_SIZE = 12

class RtpPacket:	
	header = bytearray(HEADER_SIZE)
	
	def __init__(self):
		pass
		
	def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
		"""Encode the RTP packet with header fields and payload."""
		timestamp = int(time())
		header = bytearray(HEADER_SIZE)
		#--------------
		# TO COMPLETE
		#--------------
		# Fill the header bytearray with RTP header fields
		
		header[0] = (self.version << 6) | (self.padding << 5) | (self.extension << 4) | self.CC
		header[1] = (self.marker << 7) | self.pt
		header[2] = self.seqnum >> 8
		# ...
		header[3] = third_byte = self.sequence_number & 0xFF
		header[4] =  [(self.timestamp >> shift) & 0xFF for shift in (24, 16, 8, 0)]
		header[5] = [(self.timestamp >> shift) & 0xFF for shift in (24, 16, 8, 0)]
		header[6] =  [(self.timestamp >> shift) & 0xFF for shift in (24, 16, 8, 0)]
		header[7] =  [(self.timestamp >> shift) & 0xFF for shift in (24, 16, 8, 0)]
		header[8] = [(self.ssrc >> shift) & 0xFF for shift in (24, 16, 8, 0)]
		
		header[9] = [(self.ssrc >> shift) & 0xFF for shift in (24, 16, 8, 0)]
		header[10] = [(self.ssrc >> shift) & 0xFF for shift in (24, 16, 8, 0)]
		header[11] = [(self.ssrc >> shift) & 0xFF for shift in (24, 16, 8, 0)]
		# Get the payload from the argument
		self.payload = payload
		
	def decode(self, byteStream):
		"""Decode the RTP packet."""
		self.header = bytearray(byteStream[:HEADER_SIZE])
		self.payload = byteStream[HEADER_SIZE:]
	
	def version(self):
		"""Return RTP version."""
		return int(self.header[0] >> 6)
	
	def seqNum(self):
		"""Return sequence (frame) number."""
		seqNum = self.header[2] << 8 | self.header[3]
		return int(seqNum)
	
	def timestamp(self):
		"""Return timestamp."""
		timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
		return int(timestamp)
	
	def payloadType(self):
		"""Return payload type."""
		pt = self.header[1] & 127
		return int(pt)
	
	def getPayload(self):
		"""Return payload."""
		return self.payload
		
	def getPacket(self):
		"""Return RTP packet."""
		return self.header + self.payload
