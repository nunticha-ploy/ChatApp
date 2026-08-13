import socket
import argparse
import threading #This module lets us create multiple threads
from authentication import login, signup, get_all_registered_users
from message_storage import save_message
from chat_data import get_all_groups, get_group_by_id, create_group, rename_group, delete_group
from chat_permission import can_edit_group


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
                connected_clients.pop(username, None)
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
                  print(registered_username, status)

                  user_list.append(f"{registered_username},{status}")

                response = "|".join(user_list)
                print("Sending users", response)
                client.sendall(response.encode())
                continue

              #get groups
              elif message.upper() == "GET_GROUPS":
                print("GET_GROUPS received")

                groups = get_all_groups()
                if not groups:
                  client.sendall("NO_GROUPS" .encode())
                  continue

                group_list = []

                for group in groups:
                  group_list.append(f'{group["id"]},{group["name"]}')

                response = "|".join(group_list)
                print("Sending groups", response)
                client.sendall(response.encode())
                continue

              #create group
              elif message.startswith("CREATE_GROUP"):
                group_name = message[len("CREATE_GROUP "):].strip()


                if not group_name:
                  client.sendall("Group name cannot be empty" .encode())
                  continue

                new_id = create_group(group_name, username)

                client.sendall(f"GROUP_CREATED|{new_id}|{group_name}" .encode())
                continue

              #create group
              elif message.startswith("RENAME_GROUP"):
                try:
                  _, group_id, new_name = message.split(":", 2)
                  new_name = new_name.strip()

                except ValueError:
                  client.sendall("Invalid RENAME_GROUP format".encode())
                  continue

                if not new_name:
                  client.sendall("Group name cannot be empty".encode())
                  continue

                allowed, reason = can_edit_group(group_id, username)
                if not allowed:
                  client.sendall(f"RENAME_FAILED|{reason}".encode())
                  continue

                rename_group(group_id, new_name)
                client.sendall(f"GROUP_RENAMED|{group_id}|{new_name}".encode())
                continue

              #delete group
              elif message.startswith("DELETE_GROUP:"):
                group_id = message.split(":", 1)[1].strip()

                allowed, reason = can_edit_group(group_id, username)
                if not allowed:
                  client.sendall(f"DELETE_FAILED|{reason}".encode())
                  continue

                delete_group(group_id)
                client.sendall(f"GROUP_DELETED|{group_id}".encode())
                continue

              print(f"{username}: {message}")
               # Kirandeep: automatically save every valid chat message
              save_message(username, message)
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
      connected_clients.pop(username, None)
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

