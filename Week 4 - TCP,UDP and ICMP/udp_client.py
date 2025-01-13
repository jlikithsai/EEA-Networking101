import socket


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


IP = "127.0.0.1"  
PORT = 80
ADDR = (IP, PORT)


client.settimeout(5)  

def main():
    while True:
        
        data = input("Enter Message: ")

        
        data = data.encode("utf-8")

        try:
            
            client.sendto(data, ADDR)

            
            response, addr = client.recvfrom(1024)
            response = response.decode("utf-8")
            print(f"Message from server: {response}")

        except socket.timeout:
            print("No acknowledgment from server (timeout)")
            break
        except socket.error as e:
            print(f"Socket error occurred: {e}")
            break

    
    client.close()


main()
