import os
import sys
import struct
import time
import select
from socket import *

ICMP_ECHO_REQUEST = 8

# Calculate checksum
def checksum(source_string):
    csum = 0
    countTo = (len(source_string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        csum += thisVal
        csum &= 0xFFFFFFFF
        count += 2

    if countTo < len(source_string):
        csum += source_string[-1]
        csum &= 0xFFFFFFFF

    csum = (csum >> 16) + (csum & 0xFFFF)
    csum += (csum >> 16)
    answer = ~csum & 0xFFFF
    return answer

# Send a single ping
def sendOnePing(mySocket, destAddr, ID):
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, ID, 1)
    data = struct.pack("d", time.time())
    myChecksum = checksum(header + data)

    if sys.platform == "darwin":
        myChecksum = htons(myChecksum) & 0xFFFF
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))

# Receive a single ping
def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while True:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)

        if whatReady[0] == []:  # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Extract ICMP header
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)

        if packetID == ID:
            # Calculate delay
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return f"Reply from {addr[0]}: time={round((timeReceived - timeSent) * 1000, 2)}ms"

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."

# Perform one ping
def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Return the current process ID
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay

# Ping a host
def ping(host, timeout=2):
    dest = gethostbyname(host)
    print(f"Pinging {host} ({dest}) using Python:\n")

    try:
        while True:
            delay = doOnePing(dest, timeout)
            print(delay)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nPing terminated.")

# Run the script
if __name__ == "__main__":
    host = input("Enter a host to ping (e.g., google.com): ")
    ping(host)
