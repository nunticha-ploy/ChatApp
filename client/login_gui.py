import tkinter as tk
from tkinter import messagebox
import socket
import subprocess
from chat_room_gui import ChatRoomGUI
from chat_service import ChatService


host = "localhost"
data_buff = 2048
port = 5000

# style
dark_gray = "#434343"
mid_gray = "#9E9E9E"
light_gray = "#D9D9D9"
bubble_gray = "#8C8C8C"
white = "#FFFFFF"
black = "#000000"
online_status = "#A5FF56"

header_font = ("Inclusive Sans", 26)
medium_font = ("Inclusive Sans", 15)
status_font = ("Inclusive Sans", 9)
title_font = ("Inclusive Sans", 28, "bold")

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
parent.title("COMPANY CHAT")
parent.geometry("415x700")
parent.configure(bg=white)
parent.resizable(False, False)

#content
content = tk.Frame(parent, bg=white, width=220)
content.place(relx=0.5, rely=0.30, anchor="center")

#title
title_label= tk.Label(content, text="WELCOME", font=title_font, fg=black, bg=white)
title_label.pack(pady=(0, 25))

# email
email_label = tk.Label(content, text="E-mail", font=status_font, fg=black, bg=white)
email_label.pack(anchor="w", pady=(0, 5))
email_entry = tk.Entry(content, font=medium_font,bg=light_gray, fg=black, relief="flat", bd=0)
email_entry.pack(fill="x", ipady=6, pady=(0, 15))

#password
password_label = tk.Label(content, text="Password", font=status_font, fg=black, bg=white)
password_label.pack(anchor="w", pady=(10, 5))
password_entry = tk.Entry(content, font=medium_font, bg=light_gray, fg=black, relief="flat", bd=0, show="*")
password_entry.pack(fill="x", ipady=6, pady=(0, 15))

#login button
login_button = tk.Button(content, text="Login", font=status_font, fg=white, bg=dark_gray, activebackground=mid_gray, activeforeground=white, command=validate_login)
login_button.pack(fill="x", ipady=5)


#add signup
signup_label = tk.Label(content, text="Don't have an account?", font=status_font, fg=mid_gray, bg=white, relief="flat", bd=0)
signup_label.pack(fill="x", pady=(20, 5))

#signup button
signup_button = tk.Button(content, text="Sign Up", font=status_font, fg=black, bg=white, command=open_signup)
signup_button.pack()

#start GUI loop
parent.mainloop()