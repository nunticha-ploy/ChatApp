import tkinter as tk
from tkinter import messagebox
import socket
import subprocess

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
status_font = ("Inclusive Sans", 11)



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
parent.title("Signup")
parent.geometry("415x700")

#header
header = tk.Frame(parent, bg=dark_gray, height=100)
header.pack(fill="x")
header.pack_propagate(False)


title_label= tk.Label(header, text="Create Account", font=header_font, fg=white, bg=dark_gray)
title_label.pack(padx=20, pady=25)

#content
content = tk.Frame(parent, bg=white)
content.pack(fill="both", expand=True, padx=25, pady=25)

#username
username_label = tk.Label(content, text="Username", font=medium_font, fg=black, bg=white)
username_label.pack(pady=(20, 5))
username_entry = tk.Entry(content, font=medium_font)
username_entry.pack(fill="x", pady=(0, 15))

# email
email_label = tk.Label(content, text="Email", font=medium_font, fg=black, bg=white)
email_label.pack(pady=(20, 5))
email_entry = tk.Entry(content, font=medium_font)
email_entry.pack(fill="x", pady=(0, 15))

#password
password_label = tk.Label(content, text="Password", font=medium_font, fg=black, bg=white)
password_label.pack(pady=(10, 5))
password_entry = tk.Entry(content, font=medium_font, show="*")
password_entry.pack(fill="x", pady=(0, 25))

#signup button
signup_button = tk.Button(content, text="Sign Up", font=medium_font, fg=black, bg=white, command=signup)
signup_button.pack(fill="x", pady=20)

#start GUI loop
parent.mainloop()