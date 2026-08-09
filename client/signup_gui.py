import tkinter as tk
from tkinter import messagebox
import socket
import subprocess

host = "localhost"
data_buff = 2048
port = 5000

# sign up
def signup():
  username = username_entry.get().strip()
  email = email_entry.get().strip()
  password = password_entry.get().strip()

  # check
  if not username or not email or not password:
    messagebox.showerror("Error", "All fields are required")
    return

  # connect sever
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  try:
    server_address = (host, port) 
    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)

    message = f"SIGNUP {username} {email} {password}"
    print("Sending:", message)
    sock.sendall(message.encode("utf-8"))#Send message: encode() Converts string into bytes
    
    #Receive response
    response = sock.recv(data_buff).decode() 
    print("Server: ", response)

    #after signup, go to login
    if "successfully" in response.lower():
      messagebox.showinfo("Signup Successful", "Account created successfully.\nPlease Login.")

      #close signup window first
      parent.destroy() 

      #open login GUI
      subprocess.Popen(["python", "login_gui.py"])

    else:
      messagebox.showerror("Signup Failed", response)

  #exception
  except socket.error as error:
    messagebox.showerror("Connection Error", str(error))

  finally:
    sock.close()

# create the main signup form
parent = tk.Tk()
parent.title("Signup Form")
parent.geometry("350x300")

#username
username_label = tk.Label(parent, text="Username:")
username_label.pack(pady=(20, 5))
username_entry = tk.Entry(parent, width=30)
username_entry.pack()

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

#signup button
signup_button = tk.Button(parent, text="Signup", command=signup)
signup_button.pack(pady=20)

#start GUI loop
parent.mainloop()