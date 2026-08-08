import socket
import argparse
from login_client import menu
from chat_client import chat

host = "localhost"
data_buff = 2048
port = 5000

#create client function
def TCPclient1(port):
  while True:
    #Create message: The data we want to send
    message = menu()
    if message == "EXIT":
      print("Exit chat application")
      break

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port) 
     

    try:
        print("Connecting to %s port %s" % server_address)
        sock.connect(server_address)

        print("Sending:", message)
        sock.sendall(message.encode("utf-8"))#Send message: encode() Converts string into bytes
        
        #Receive data
        response = sock.recv(data_buff).decode() 
        print("Server: ", response)

        #keep the sock open after login
        if response.startswith("SUCCESS"):
          username = response.split()[1]
          print(f"Welcome, {username}!")
          chat(sock, username)
          break
     
    #Socket error handling
    except socket.error as e:
      print("Socket error: %s" %str(e))
    except Exception as e:
      print("Other exception: %s" %str(e))

    #Step 18: Finally block: Always runs, even if an error occurs
    finally:
      print("Closing connection to the server")
      sock.close()                     


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Socket Server Example") 
  parser.add_argument("--port", action="store", dest="port", type=int, required=True)
  given_args = parser.parse_args()
  port = given_args.port
  TCPclient1(port)  