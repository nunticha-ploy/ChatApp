import threading
data_buff = 2048
def chat(sock, username):
  print("****** Chat Room ******")
  print("Type 'LOGOUT' to exit")

  while True:
    message = input(f"{username}: ").strip()
    if not message:
      print("Message cannot be empty")
      continue
    # Send the message once
    sock.sendall(message.encode())
    # Wait for the server's response
    response = sock.recv(data_buff) 
    if not response:
      print("Server closed the connection.")
      break
    print("Server:", response.decode())
     # End the client chat loop after receiving logout confirmation
    if message.upper() == "LOGOUT":
      break

def receive_message(sock):
  while True:
    response = sock.recv(data_buff)
    print(response.decode())
    receive_thread = threading.Thread(target=receive_message, args=(sock, ))
    receive_thread.daemon = True
    receive_thread.start() 