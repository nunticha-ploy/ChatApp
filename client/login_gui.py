import tkinter as tk
from tkinter import messagebox
import socket
import subprocess
from chat_room_gui import ChatRoomGUI
from chat_service import ChatService


host = "localhost"
data_buff = 2048
port = 5000

# function to validate the login
def validate_login():
  email = email_entry.get().strip()
  password = password_entry.get().strip()

  # check
  if not email or not password:
    messagebox.showerror("Login Failed", "Invalid username or password")
    return

  # connect sever
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  try:
    server_address = (host, port) 
    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)

    message = f"LOGIN {email} {password}"
    print("Sending:", message)
    sock.sendall(message.encode("utf-8"))#Send message: encode() Converts string into bytes
    
    #Receive data
    response = sock.recv(data_buff).decode() 
    print("Server: ", response)

    #keep the sock open after login
    if response.startswith("SUCCESS"):
      username = response.split()[1]
      messagebox.showinfo("Login Successful", f"Welcome, {username}!")

      #close login window first
      parent.destroy() 

      #open chat GUI
      root = tk.Tk()
      chat_service = ChatService(sock, username)
      app = ChatRoomGUI(root, chat_service)
      root.mainloop()
      

    else:
      messagebox.showerror("Login Failed", response)
      sock.close()

  #exception
  except socket.error as error:
    messagebox.showerror("Connection Error", str(error))

# add signup
def open_signup():
  #close login window first
  parent.destroy() 
   
  #open signup GUI
  subprocess.Popen(["python", "signup_gui.py"])

# create the main login form
parent = tk.Tk()
parent.title("Login Form")
parent.geometry("350x250")

# email
email_label = tk.Label(parent, text="Email:")
email_label.pack(pady=(20, 5))
email_entry = tk.Entry(parent, width=30)
email_entry.pack()

#password
password_label = tk.Label(parent, text="Password:")
password_label.pack(pady=(10, 5))
password_entry = tk.Entry(parent, width=30, show="*")
password_entry.pack()

#login button
login_button = tk.Button(parent, text="Login", command=validate_login)
login_button.pack(pady=20)


#add signup
signup_label = tk.Label(parent, text="Don't have an account?")
signup_label.pack()

#signup button
signup_button = tk.Button(parent, text="Signup", command=open_signup)
signup_button.pack(pady=5)

#start GUI loop
parent.mainloop()



# hardcode data for testing

if __name__ == "__main__":
    class TestChatService:

        def __init__(self, username):
            self.username = username

            self._groups = [
                {"id": 1, "name": "Group 1"},
                {"id": 2, "name": "Group 2"},
                {"id": 3, "name": "Group 3"},
            ]

        def get_current_user(self):
            return {"id": 0, "username": self.username, "status": "online"}

        def get_all_users(self):
            return [
                {"id": 2, "username": "User B", "status": "online"},
                {"id": 3, "username": "User C", "status": "offline"},
                {"id": 4, "username": "User D", "status": "offline"},
            ]

        def get_all_groups(self):
            return self._groups

        def get_one_on_one_chat(self, user_id):
            return [
                {"username": self.username, "msg": "Hello..."},
                {"username": self.username, "msg": "My name is " + self.username},
                {"username": "User B", "msg": "Hello A"},
                {"username": "User B", "msg": "My name is B"},
            ]

        def get_group_chat(self, group_id):
            return []

        # function create new group chat pop up
        def create_group_chat(self, group_chat_name):
            new_id = max((g["id"] for g in self._groups), default=0) + 1
            self._groups.append({"id": new_id, "name": group_chat_name})


    root = tk.Tk()

    chat_service = TestChatService()

    app = ChatRoomGUI(
        root,
        chat_service
    )

    root.mainloop()