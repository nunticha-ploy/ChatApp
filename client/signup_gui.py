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
title_font = ("Inclusive Sans", 24, "bold")



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

# add login
def open_login():
  #close signup window first
  parent.destroy() 
   
  #open signup GUI
  subprocess.Popen(["python", "login_gui.py"])


# create the main signup form
parent = tk.Tk()
parent.title("COMPANY CHAT")
parent.geometry("415x700")
parent.configure(bg=white)
parent.resizable(False, False)

#content
content = tk.Frame(parent, bg=white, width=220)
content.place(relx=0.5, rely=0.32, anchor="center")

#TITLE
title_label= tk.Label(content, text="CREATE ACCOUNT", font=title_font, fg=black, bg=white)
title_label.pack(pady=(0, 25))


#username
username_label = tk.Label(content, text="Username", font=status_font, fg=black, bg=white)
username_label.pack(anchor="w", pady=(0, 5))
username_entry = tk.Entry(content, font=medium_font,bg=light_gray, fg=black, relief="flat", bd=0)
username_entry.pack(fill="x",ipady=6, pady=(0, 15))

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

#signup button
signup_button = tk.Button(content, text="Sign Up", font=status_font, fg=white, bg=dark_gray, activebackground=mid_gray, activeforeground=white, relief="flat", bd=0, command=signup)
signup_button.pack(fill="x", pady=5)

#add login
login_label = tk.Label(content, text="Already have an account?", font=status_font, fg=mid_gray, bg=white, relief="flat", bd=0, )
login_label.pack(fill="x", pady=(20, 5))

#signup button
login_button = tk.Button(content, text="Login", font=status_font, fg=black, bg=white, command=open_login)
login_button.pack()

#start GUI loop
parent.mainloop()