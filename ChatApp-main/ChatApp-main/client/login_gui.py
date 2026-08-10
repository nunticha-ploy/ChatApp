import sys
import os
import tkinter as tk
from tkinter import messagebox
import socket
import subprocess

from chat_room_gui import ChatRoomGUI
from chat_service import ChatService


host = "localhost"
data_buff = 2048
port = 5000


def validate_login():
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not email or not password:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password"
        )
        return

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        server_address = (host, port)

        print(
            "Connecting to %s port %s"
            % server_address
        )

        sock.connect(server_address)

        message = f"LOGIN {email} {password}"

        print("Sending:", message)

        sock.sendall(
            message.encode("utf-8")
        )

        response = sock.recv(
            data_buff
        ).decode()

        print("Server:", response)

        if response.startswith("SUCCESS"):

            username = response.split()[1]

            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!"
            )

            parent.destroy()

            root = tk.Tk()

            chat_service = ChatService(
                sock,
                username
            )

            app = ChatRoomGUI(
                root,
                chat_service
            )

            root.mainloop()

        else:

            messagebox.showerror(
                "Login Failed",
                response
            )

            sock.close()

    except socket.error as error:

        messagebox.showerror(
            "Connection Error",
            str(error)
        )


def open_signup():

    parent.destroy()

    signup_path = os.path.join(
        os.path.dirname(__file__),
        "signup_gui.py"
    )

    subprocess.Popen([
        sys.executable,
        signup_path
    ])


parent = tk.Tk()

parent.title("Login Form")
parent.geometry("350x250")


email_label = tk.Label(
    parent,
    text="Email:"
)

email_label.pack(
    pady=(20, 5)
)


email_entry = tk.Entry(
    parent,
    width=30
)

email_entry.pack()


password_label = tk.Label(
    parent,
    text="Password:"
)

password_label.pack(
    pady=(10, 5)
)


password_entry = tk.Entry(
    parent,
    width=30,
    show="*"
)

password_entry.pack()


login_button = tk.Button(
    parent,
    text="Login",
    command=validate_login
)

login_button.pack(
    pady=20
)


signup_label = tk.Label(
    parent,
    text="Don't have an account?"
)

signup_label.pack()


signup_button = tk.Button(
    parent,
    text="Signup",
    command=open_signup
)

signup_button.pack(
    pady=5
)


parent.mainloop()