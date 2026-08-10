import socket
import argparse
import threading #This module lets us create multiple threads
from authentication import login, signup, get_all_registered_users

host = "localhost"
data_buff = 2048 #receive up to 2048 bytes at a time
backlog = 5 #up to 5 clients can wait to connect.
port = 5000

user_status = {}
connected_clients = {}

def userLoginHandle(client, address):
  print("Clent connected:", address)

  try: 
    data = client.recv(data_buff) 
    #Check if data exists 
    if data:
      message = data.decode().strip()
      #removes any accidental spaces before or after the message and makes the parsing a little more robust
      parts = message.strip().split()
      if not parts:
        client.sendall("Cannot be empty" .encode())
        return

      #login
      if parts[0] == "LOGIN":
        if len(parts) != 3:
          client.sendall("Invalid LOGIN." .encode())
        else:
          #client send data 
          email = parts[1]
          password = parts[2]
          success, reply, username = login(email, password)
          if success:
            #user status
            user_status[username] = "online"
            connected_clients[username] = client
            client.sendall(f"SUCCESS {username}" .encode())
          else:
            client.sendall(reply.encode())

          #keeps the loggin client connected
          if success:
            while True:
              data = client.recv(data_buff) #Wait for the next message from the client.
              if not data:
                break
              message = data.decode().strip()
              #logout
              if message.upper() == "LOGOUT":
                #user status
                user_status[username] = "offline"
                client.sendall("Logout successfully!" .encode())
                break
              #get users
              elif message.upper() == "GET_USERS":
                print("GET_USERS received")
                registered_users = get_all_registered_users()
                print("Registerd user:", registered_users)
                user_list = []
                for registered_username in registered_users:
                  status = user_status.get(registered_username, "offline")
                  if username in connected_clients:
                    del connected_clients[username]
                  print(registered_username, status)
                  user_list.append(f"{registered_username},{status}")
                response = "|".join(user_list)
                print("Sending users", response)
                client.sendall(response.encode())
                continue

              print(f"{username}: {message}")
              client.sendall(("Server received: " + message).encode())
      #singup
      elif parts[0] == "SIGNUP":
        if len(parts) != 4:
          client.sendall("Invalid SINGUP." .encode())
        else:
          username = parts[1]
          email = parts[2]
          password = parts[3]
          success, reply = signup(username, email, password)
          client.sendall(reply.encode())
      #other choose
      else:
        message = data.decode().strip()
        print("Client:", message)

        response = "Server received: " + message
        client.send(response.encode())
  except Exception as error:
    print("Error:", error)
  finally:
    if "username" in locals():
      user_status[username] = "offline"
    client.close()
    print("Client disconnected:", address) 

#create a TCP socket
def TCPserver1(port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  #bind it to a port
  server_address = (host, port)
  print("Starting up echo server on %s port %s" % server_address)
  sock.bind(server_address)

  #listen       
  sock.listen(backlog)

  #loop
  while True:
    print("Waiting to receive message from client")
    
    #accept clients
    client, address = sock.accept() ## accept new connection

    #start a threading
    thread = threading.Thread(target=userLoginHandle, args=(client, address))
    thread.start()

   

#Main program
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Socket Server Example")
  parser.add_argument("--port", action="store", dest="port", type=int, required=True)
  given_args = parser.parse_args()
  port = given_args.port
  TCPserver1(port)  