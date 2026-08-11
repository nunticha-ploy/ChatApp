# import library

import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

from room_class import ChatRoom


dark_gray = "#434343"
mid_gray = "#9E9E9E"
light_gray = "#D9D9D9"
bubble_gray = "#8C8C8C"
white = "#FFFFFF"
black = "#000000"
online_status = "#A5FF56"

header_name_font = ("Inclusive Sans", 26)
medium_font = ("Inclusive Sans", 15)
row_name_font = ("Inclusive Sans", 17)
section_font = ("Inclusive Sans", 17, "bold")
header_font = ("Inclusive Sans", 25)
status_font = ("Inclusive Sans", 11)
name_font = ("Inclusive Sans", 10)
msg_font = ("Inclusive Sans", 10)
bold_font = ("Inclusive Sans", 15, "bold")
chevron_font = ("Inclusive Sans", 14)


class ChatRoomGUI:

    def __init__(self, root, chat_service):

        self.root = root
        self.chat_service = chat_service

        self.current_user = (
            self.chat_service.get_current_user()
        )

        self.current_room = None
        self.current_messages = []

        self.root.title("Company Chat")
        self.root.geometry("415x700")
        self.root.resizable(
            width=False,
            height=False
        )

        # Load the user list before starting
        # the background message listener.
        self.show_user_page()

        # The listener is the only code that
        # receives messages after this point.
        self.chat_service.start_message_listener(
            self.receive_message
        )

    # Clear window
    def clear(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # Receive a message from ChatService
    def receive_message(
        self,
        sender,
        text
    ):

        # Tkinter widgets must be changed
        # from the main GUI thread.
        self.root.after(
            0,
            self.display_received_message,
            sender,
            text
        )

    # Display received message
    def display_received_message(
        self,
        sender,
        text
    ):

        new_message = {
            "username": sender,
            "msg": text,
            "time": datetime.now().strftime("%I:%M:%S %p")
        }

        # Only add the message to the open
        # private chat when it belongs there.
        if (
            self.current_room is not None
            and self.current_room.type == "private"
            and self.current_room.name == sender
        ):

            self.current_messages.append(
                new_message
            )

            self.show_chat_page(
                self.current_room,
                self.current_messages,
                "online"
            )

    # Status
    def create_status_row(
        self,
        container,
        status,
        dot_size=8,
        text_font=status_font
    ):

        if status == "online":

            status_text = "Online"
            status_color = online_status

        else:

            status_text = "Offline"
            status_color = mid_gray

        status_row = tk.Frame(
            container,
            background=container["background"]
        )

        status_dot = tk.Label(
            status_row,
            text="\u25CF",
            font=(
                "Inclusive Sans",
                dot_size
            ),
            fg=status_color,
            bg=container["background"]
        )

        status_dot.pack(
            side=tk.LEFT
        )

        status_label = tk.Label(
            status_row,
            text=status_text,
            font=text_font,
            fg=mid_gray,
            bg=container["background"]
        )

        status_label.pack(
            side=tk.LEFT,
            padx=(4, 0)
        )

        return status_row

    # Display user page
    def show_user_page(self):

        self.clear()

        # Header
        top_frame = tk.Frame(
            self.root,
            width=415,
            background=dark_gray
        )

        top_frame.pack(
            fill="x"
        )

        header_inner = tk.Frame(
            top_frame,
            background=dark_gray
        )

        header_inner.pack(
            anchor=tk.NW,
            padx=20,
            pady=15
        )

        current_name_label = tk.Label(
            header_inner,
            text=self.current_user["username"],
            font=header_name_font,
            fg=white,
            bg=dark_gray
        )

        current_name_label.pack(
            anchor=tk.NW
        )

        self.create_status_row(
            header_inner,
            self.current_user["status"]
        ).pack(
            anchor=tk.NW
        )

        content = tk.Frame(
            self.root,
            background=white
        )

        content.pack(
            fill="both",
            expand=True
        )

        # Users
        users_title = tk.Label(
            content,
            text="USERS",
            font=section_font,
            fg=mid_gray,
            bg=white,
            bd=0
        )

        users_title.pack(
            anchor=tk.NW,
            padx=20,
            pady=(15, 8)
        )

        # ChatService caches the initial list.
        users = self.chat_service.get_all_users()

        for user in users:

            self.create_user_row(
                content,
                user
            )

        # Separator
        line = tk.Frame(
            content,
            width=415,
            height=1,
            background=light_gray
        )

        line.pack(
            fill="x",
            pady=10
        )

        # Groups
        group_title = tk.Label(
            content,
            text="GROUPS",
            font=section_font,
            fg=mid_gray,
            bg=white,
            bd=0
        )

        group_title.pack(
            anchor=tk.NW,
            padx=20,
            pady=(5, 8)
        )

        groups = self.chat_service.get_all_groups()

        for group in groups:

            self.create_group_row(
                content,
                group
            )

        # Create group
        create_new_group_label = tk.Label(
            content,
            text="+ Create new group",
            fg=mid_gray,
            bg=white,
            font=status_font,
            cursor="hand2"
        )

        create_new_group_label.pack(
            anchor=tk.NW,
            padx=20,
            pady=15
        )

        create_new_group_label.bind(
            "<Button-1>",
            lambda e: self.create_group_chat()
        )

    # Create new group
    def create_group_chat(self):

        group_name = simpledialog.askstring(
            "New group",
            "Group name:",
            parent=self.root
        )

        if group_name:

            self.chat_service.create_group_chat(
                group_name
            )

            self.show_user_page()

    # Create user row
    def create_user_row(
        self,
        container,
        user
    ):

        user_id = user["id"]
        username = user["username"]
        status = user["status"]

        row = tk.Frame(
            container,
            width=415,
            background=white
        )

        row.pack(
            fill="x",
            padx=20,
            pady=8
        )

        name_label = tk.Label(
            row,
            text=username,
            font=row_name_font,
            fg=black,
            bg=white,
            bd=0
        )

        name_label.pack(
            anchor=tk.NW
        )

        status_row = self.create_status_row(
            row,
            status
        )

        status_row.pack(
            anchor=tk.NW
        )

        enter_chat_sign = tk.Label(
            row,
            text="\u203A",
            font=chevron_font,
            fg=mid_gray,
            bg=white,
            bd=0
        )

        enter_chat_sign.place(
            relx=1.0,
            rely=0.5,
            anchor="e"
        )

        clickable = [
            row,
            name_label,
            status_row,
            enter_chat_sign
        ] + list(
            status_row.winfo_children()
        )

        for widget in clickable:

            widget.bind(
                "<Button-1>",
                lambda e,
                uid=user_id,
                name=username,
                user_status=status:
                self.open_one_on_one_chat(
                    uid,
                    name,
                    user_status
                )
            )

    # Open one-on-one chat
    def open_one_on_one_chat(
        self,
        user_id,
        name,
        status
    ):

        self.current_room = ChatRoom(
            id=user_id,
            type="private",
            name=name
        )

        msg = self.chat_service.get_one_on_one_chat(
            user_id
        )

        self.current_messages = list(msg)

        self.show_chat_page(
            self.current_room,
            self.current_messages,
            status
        )

    # Create group row
    def create_group_row(
        self,
        container,
        group
    ):

        group_id = group["id"]
        group_name = group["name"]

        row = tk.Frame(
            container,
            width=415,
            background=white
        )

        row.pack(
            fill="x",
            padx=20,
            pady=8
        )

        name_label = tk.Label(
            row,
            text=group_name,
            font=row_name_font,
            fg=black,
            bg=white,
            bd=0
        )

        name_label.pack(
            anchor=tk.NW
        )

        enter_chat_sign = tk.Label(
            row,
            text="\u203A",
            font=chevron_font,
            fg=mid_gray,
            bg=white,
            bd=0
        )

        enter_chat_sign.place(
            relx=1.0,
            rely=0.5,
            anchor="e"
        )

        for widget in (
            row,
            name_label,
            enter_chat_sign
        ):

            widget.bind(
                "<Button-1>",
                lambda e,
                uid=group_id,
                name=group_name:
                self.open_group_chat(
                    uid,
                    name
                )
            )

    # Open group chat
    def open_group_chat(
        self,
        group_id,
        group_name
    ):

        self.current_room = ChatRoom(
            id=group_id,
            type="group",
            name=group_name
        )

        msg = self.chat_service.get_group_chat(
            group_id
        )

        self.current_messages = list(msg)

        self.show_chat_page(
            self.current_room,
            self.current_messages,
            "Group"
        )

    # Chat page
    def show_chat_page(
        self,
        room,
        msg,
        status
    ):

        self.clear()

        # Chat header
        top_frame = tk.Frame(
            self.root,
            width=415,
            height=60,
            background=dark_gray
        )

        top_frame.pack(
            fill="x"
        )

        top_frame.pack_propagate(
            False
        )

        # Back button
        back_button = tk.Label(
            top_frame,
            text="<",
            fg=mid_gray,
            bg=dark_gray,
            font=header_font
        )

        back_button.pack(
            side=tk.LEFT,
            padx=20
        )

        back_button.bind(
            "<Button-1>",
            lambda e: self.show_user_page()
        )

        # Chat name
        group_chat_name = tk.Label(
            top_frame,
            text=room.name,
            font=header_font,
            fg=white,
            bg=dark_gray
        )

        group_chat_name.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Background
        frame = tk.Frame(
            self.root,
            background=white
        )

        frame.pack(
            fill="both",
            expand=True
        )

        # Messages
        for message in msg:

            sender = message["username"]
            text = message["msg"]
            message_time = message.get("time", "")

            row = tk.Frame(
                frame,
                bg=white
            )

            row.pack(
                fill="x",
                padx=20,
                pady=7
            )

            is_other_party = (
                sender == room.name
            )

            bubble_bg = (
                bubble_gray
                if is_other_party
                else light_gray
            )

            bubble_fg = (
                white
                if is_other_party
                else black
            )

            bubble = tk.Label(
                row,
                text=text,
                font=msg_font,
                fg=bubble_fg,
                bg=bubble_bg,
                padx=12,
                pady=6
            )

            sender_label = tk.Label(
                row,
                text=f"{sender}  {message_time}",
                font=name_font,
                fg=mid_gray,
                bg=white
            )

            if is_other_party:

                sender_label.pack(
                    side=tk.RIGHT
                )

                bubble.pack(
                    side=tk.RIGHT,
                    padx=(0, 8)
                )

            else:

                sender_label.pack(
                    side=tk.LEFT
                )

                bubble.pack(
                    side=tk.LEFT,
                    padx=(8, 0)
                )

        # Message input area
        typing_frame = tk.Frame(
            self.root,
            width=415,
            height=60,
            background=dark_gray
        )

        typing_frame.pack(
            fill="x",
            side=tk.BOTTOM
        )

        typing_frame.pack_propagate(
            False
        )

        # Message entry
        self.message_entry = tk.Entry(
            typing_frame,
            font=msg_font
        )

        self.message_entry.pack(
            side=tk.LEFT,
            fill="x",
            expand=True,
            padx=(10, 5),
            pady=12
        )

        # Send button
        send_button = tk.Button(
            typing_frame,
            text="Send",
            font=name_font,
            command=self.send_message
        )

        send_button.pack(
            side=tk.RIGHT,
            padx=(5, 10),
            pady=12
        )

        # Clear chat button
        clear_button = tk.Button(
        typing_frame,
        text="Clear Chat",
        font=name_font,
        command=self.clear_chat_history
)

        clear_button.pack(
        side=tk.RIGHT,
        padx=10,
        pady=12
)
        # Enter sends message
        self.message_entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )
        # Clear messages from the current chat
    def clear_chat_history(self):

        if not self.current_messages:
            messagebox.showinfo(
                "Clear Chat",
                "There are no messages to clear."
            )
            return

        confirm = messagebox.askyesno(
            "Clear Chat",
            "Are you sure you want to clear this chat history?"
        )

        if not confirm:
            return

        self.current_messages.clear()

        self.render_messages(
            self.current_messages
        )
    # Send message
    def send_message(self):

        message = self.message_entry.get().strip()

        # Prevent empty messages
        if not message:

            messagebox.showwarning(
                "Empty Message",
                "Message cannot be empty."
            )

            return

        if self.current_room is None:
            return

        success = self.chat_service.send_msg(
            self.current_room,
            message
        )

        if success:
         
        # Save sent message with current time
            self.current_messages.append({
        "username": self.current_user["username"],
        "msg": message,
        "time": datetime.now().strftime("%I:%M:%S %p")
})
            self.message_entry.delete(
                0,
                tk.END
            )

            print(
                "Message sent:",
                message
            )
            self.show_chat_page(
            self.current_room,
            self.current_messages,
            "online"
)
            