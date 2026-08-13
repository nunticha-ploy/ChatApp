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


# create class
class ChatRoomGUI:

    def __init__(self, root, chat_service):
        # create window
        self.root = root
        self.chat_service = chat_service

        self.current_user = self.chat_service.get_current_user()

        # set variable for current chat room
        self.current_room = None
        self.current_messages = []
        self.refresh_job = None

        self.root.title("Company Chat")
        self.root.geometry("415x700")
        self.root.resizable(width=False, height=False)

        self.show_user_page()

    # clear window
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # status
    def create_status_row(self, container, status, dot_size=8, text_font=status_font):
        # if else statement check status
        if status == "online":
            status_text = "Online"
            status_color = online_status
        else:
            status_text = "Offline"
            status_color = mid_gray

        status_row = tk.Frame(container, background=container["background"])

        status_dot = tk.Label(status_row, text="\u25CF", font=("Inclusive Sans", dot_size), fg=status_color,
                              bg=container["background"])
        status_dot.pack(side=tk.LEFT)

        # status text
        status_label = tk.Label(status_row, text=status_text, font=text_font, fg=mid_gray, bg=container["background"])
        status_label.pack(side=tk.LEFT, padx=(4, 0))

        return status_row

    # display user page
    def show_user_page(self):

        # Stop real-time message checking
        if self.refresh_job is not None:

            self.root.after_cancel(
                self.refresh_job
            )

            self.refresh_job = None
        self.clear()

        # create header
        top_frame = tk.Frame(self.root, width=415, background=dark_gray)
        top_frame.pack(fill="x")

        header_inner = tk.Frame(top_frame, background=dark_gray)
        header_inner.pack(anchor=tk.NW, padx=20, pady=15)

        current_name_label = tk.Label(header_inner, text=self.current_user["username"], font=header_name_font, fg=white, bg=dark_gray)
        current_name_label.pack(anchor=tk.NW)

        # add status row into header container
        self.create_status_row(header_inner, self.current_user["status"]).pack(anchor=tk.NW)

        content = tk.Frame(self.root, background=white)
        content.pack(fill="both", expand=True)

        # users part
        users_title = tk.Label(content, text="USERS", font=section_font, fg=mid_gray, bg=white, bd=0)
        users_title.pack(anchor=tk.NW, padx=20, pady=(15, 8))

        # get user from server
        users = self.chat_service.get_all_users()

        for user in users:
            self.create_user_row(content, user)

        # line
        line = tk.Frame(content, width=415, height=1, background=light_gray)
        line.pack(fill="x", pady=10)

        # groups part
        group_title = tk.Label(content, text="GROUPS", font=section_font, fg=mid_gray, bg=white, bd=0)
        group_title.pack(anchor=tk.NW, padx=20, pady=(5, 8))

        groups = self.chat_service.get_all_groups()
        for group in groups:
            self.create_group_row(content, group)

        # create group button
        create_new_group_label = tk.Label(
            content, text="+ Create new group", fg=mid_gray, bg=white, font=status_font, cursor="hand2")
        create_new_group_label.pack(anchor=tk.NW, padx=20, pady=15)
        create_new_group_label.bind("<Button-1>", lambda e: self.create_group_chat())

    # function create new group chat
    def create_group_chat(self):
        group_name = simpledialog.askstring("New group", "Group name:", parent=self.root)
        if group_name:
            self.chat_service.create_group_chat(group_name)
            self.show_user_page()

    # create user row to display
    def create_user_row(self, container, user):

        user_id = user["id"]
        username = user["username"]
        status = user["status"]

        row = tk.Frame(container, width=415, background=white)
        row.pack(fill="x", padx=20, pady=8)

        # username in row
        name_label = tk.Label(row, text=username, font=row_name_font, fg=black, bg=white, bd=0)
        name_label.pack(anchor=tk.NW)

        status_row = self.create_status_row(row, status)
        status_row.pack(anchor=tk.NW)

        # enter chat sign >
        enter_chat_sign = tk.Label(row, text="\u203A", font=chevron_font, fg=mid_gray, bg=white, bd=0)
        enter_chat_sign.place(relx=1.0, rely=0.5, anchor="e")

        # click enter chat
        clickable = [row, name_label, status_row, enter_chat_sign] + list(status_row.winfo_children())
        for widget in clickable:
            widget.bind("<Button-1>", lambda e, uid=user_id, name=username: self.open_one_on_one_chat(uid, name, status))

    # function open 1-1 chat room
    def open_one_on_one_chat(self, user_id, name, status):

        # set this room as current room
        self.current_room = ChatRoom(id=user_id, type="private", name=name)

        msg = self.chat_service.get_one_on_one_chat(user_id)

        self.show_chat_page(self.current_room, msg, status)

    # create group row to display
    def create_group_row(self, container, group):

        group_id = group["id"]
        group_name = group["name"]

        row = tk.Frame(container, width=415, background=white)
        row.pack(fill="x", padx=20, pady=8)

        # group in row
        name_label = tk.Label(row, text=group_name, font=row_name_font, fg=black, bg=white, bd=0)
        name_label.pack(anchor=tk.NW)

        #setting button for rename/ delete
        setting_button = tk.Label(row, text="\u22EE", font=chevron_font, fg=mid_gray, bg=white, bd=0, cursor="hand2")
        setting_button.place(relx=1.0, rely=0.5, anchor="e", x=-25)
        setting_button.bind(
            "<Button-1>",
            lambda e, b=setting_button, gid=group_id, gname=group_name: self.group_setting(b, gid, gname)
        )

        # enter chat sign >
        enter_chat_sign = tk.Label(row, text="\u203A", font=chevron_font, fg=mid_gray, bg=white, bd=0)
        enter_chat_sign.place(relx=1.0, rely=0.5, anchor="e")

        # click enter chat
        for widget in (row, name_label, enter_chat_sign):
            widget.bind("<Button-1>", lambda e, uid=group_id, name=group_name: self.open_group_chat(uid, name))

    # function open group chat room
    def open_group_chat(self, group_id, group_name):

        # set this room as current room
        self.current_room = ChatRoom(id=group_id, type="group", name=group_name)
        msg = self.chat_service.get_group_chat(group_id)
        self.show_chat_page(self.current_room, msg, "Group")

         #group setting container
    def group_setting(self, button, group_id, group_name):
        option =tk.Menu(self.root, tearoff=0)

        option.add_command(label="Rename", command=lambda: self.rename_group_chat(group_id, group_name, group_name))
        option.add_command(label="Delete", command=lambda: self.delete_group_chat(group_id, group_name))
        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()

        option.post(x, y)

    #rename group
    def rename_group_chat(self, group_id, group_name, current_name):
        new_name = simpledialog.askstring("Rename", "New group name:", initialvalue=current_name, parent=self.root)

        if new_name is None:
            return

        new_name = new_name.strip()

        # validation input field cannot be empty
        if not new_name:
            messagebox.showwarning("Invalid", "Group name cannot be empty.")
            return

        response = self.chat_service.rename_group_chat(group_id, new_name)
        if response.startswith("GROUP_RENAMED"):  # <<< เพิ่มการเช็ค response
            self.show_user_page()
        else:
            messagebox.showerror("Error", response)
        self.show_user_page()

    #delete group chat
    def delete_group_chat(self, group_id, group_name):
        confirm = messagebox.askyesno(
            "Delete group",
            f"Are you sure you want to delete '{group_name}'?"
        )
        if not confirm:
            return

        response = self.chat_service.delete_group_chat(group_id)

        if response.startswith("GROUP_DELETED"):
            self.show_user_page()
        else:
            messagebox.showerror("Error", response)

    # Chat page
    def show_chat_page(self, room, msg, status):

        self.clear()
        # chat header
        top_frame = tk.Frame(self.root, width=415, height=60, background=dark_gray)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)

        # back button to user page
        back_button = tk.Label(top_frame, text="<", fg=mid_gray, bg=dark_gray, font=header_font)
        back_button.pack(side=tk.LEFT, padx=20)
        back_button.bind("<Button-1>", lambda e: self.show_user_page())

        # Group chat name
        group_chat_name = tk.Label(top_frame, text=room.name, font=header_font, fg=white, bg=dark_gray)
        group_chat_name.place(relx=0.5, rely=0.5, anchor="center")

        # background
                # Search messages area
        search_frame = tk.Frame(
            self.root,
            background=white
        )

        search_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.search_entry = tk.Entry(
            search_frame,
            font=msg_font
        )

        self.search_entry.pack(
            side=tk.LEFT,
            fill="x",
            expand=True,
            padx=(5, 5)
        )

        search_button = tk.Button(
            search_frame,
            text="Search",
            font=name_font,
            command=self.search_messages
        )

        search_button.pack(
            side=tk.RIGHT,
            padx=5
        )

        # Press Enter to search
        self.search_entry.bind(
            "<Return>",
            self.search_messages
        )
               # Frame containing chat messages
        self.message_frame = tk.Frame(
            self.root,
            background=white
        )

       
        self.message_frame.pack(
            fill="both",
            expand=True
        )

                # Save messages for the current chat
        self.current_messages = msg

        # Display messages
        for message in self.current_messages:
            sender = message["username"]
            text = message["msg"]

            row = tk.Frame(frame, bg=white)
            row.pack(fill="x", padx=20, pady=7)

            is_other_party = (sender == room.name)

            bubble_bg = bubble_gray if is_other_party else light_gray
            bubble_fg = white if is_other_party else black

            bubble = tk.Label(row, text=text, font=msg_font, fg=bubble_fg, bg=bubble_bg, padx=12, pady=6)
            sender_label = tk.Label(row, text=sender, font=name_font, fg=mid_gray, bg=white)

            # if else check user(me or other)
            if is_other_party:
                sender_label.pack(side=tk.RIGHT)
                bubble.pack(side=tk.RIGHT, padx=(0, 8))
            else:
                sender_label.pack(side=tk.LEFT)
                bubble.pack(side=tk.LEFT, padx=(8, 0))

        typing_frame = tk.Frame(self.root, width=415, height=60, background=dark_gray)

        typing_frame.pack(fill="x", side=tk.BOTTOM)
        typing_frame.pack_propagate(False)
                # Message input box
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
            text="Clear",
            font=name_font,
            command=self.clear_chat_history
        )

        clear_button.pack(
            side=tk.RIGHT,
            padx=(5, 5),
            pady=12
        )

                # Press Enter to send
        self.message_entry.bind(
            "<Return>",
            self.send_message
        )

        # Start checking for new messages
        self.start_message_refresh()


        
             # Send a message
    def send_message(self, event=None):

        message = self.message_entry.get().strip()

        # Prevent empty messages
        if not message:
            messagebox.showwarning(
                "Empty Message",
                "Please enter a message before sending."
            )

            self.message_entry.focus_set()

            return "break"
        

        try:

            # Send message using the existing chat service
            success = self.chat_service.send_msg(
                self.current_room,
                message
            )

            if success:

                # Add the new message to the current chat
                # Get the current time
                current_time = datetime.now().strftime("%I:%M %p")

                # Create the new message
                new_message = {
                "username": self.current_user["username"],
                "msg": message,
                "time": current_time
}

                self.current_messages.append(
                    new_message
                )

                # Clear the message box
                self.message_entry.delete(
                    0,
                    tk.END
                )

                # Refresh the chat display
                self.display_messages(
                    self.current_messages
                )

        except Exception as error:

            print(
                "Error sending message:",
                error
            )

        return "break"


            # Search messages in the current chat
    def search_messages(self, event=None):

        search_text = (
            self.search_entry.get()
            .strip()
            .lower()
        )

        # If search box is empty, show all messages
        if not search_text:

            self.display_messages(
                self.current_messages
            )

            return "break"

        # Store matching messages
        matching_messages = []

        # Check each message
        for message in self.current_messages:

            username = message["username"].lower()
            text = message["msg"].lower()

            # Search username or message text
            if (
                search_text in username
                or search_text in text
            ):

                matching_messages.append(
                    message
                )

        # Display search results
        self.display_messages(
            matching_messages
        )

        return "break"
            # Clear messages from the current chat
    def clear_chat_history(self):

        # Ask the user for confirmation
        confirm = messagebox.askyesno(
            "Clear Chat History",
            "Are you sure you want to clear this chat?"
        )

        if not confirm:
            return

        # Remove messages from the current chat display
        self.current_messages.clear()

        # Refresh the message area
        self.display_messages(
            self.current_messages
        )

        # Show confirmation
        messagebox.showinfo(
            "Clear Chat",
            "Chat history cleared."
        )
            # Display messages in the chat window
    def display_messages(self, messages):

        # Remove old message bubbles
        for widget in self.message_frame.winfo_children():
            widget.destroy()

        # Display each message
        for message in messages:

            sender = message["username"]
            text = message["msg"]

            # Get message time
            message_time = message.get(
            "time",
            datetime.now().strftime("%I:%M %p")
)

            row = tk.Frame(
                self.message_frame,
                bg=white
            )

            row.pack(
                fill="x",
                padx=20,
                pady=7
            )

            is_other_party = (
                sender != self.current_user["username"]
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
                pady=6,
                wraplength=260
            )

            sender_label = tk.Label(
                row,
                text=sender,
                font=name_font,
                fg=mid_gray,
                bg=white
            )
             
            time_label = tk.Label(
                row,
                text=message_time,
                font=("Inclusive Sans", 8),
                fg=mid_gray,
                bg=white
)
                  
            sender_label.pack(
                side=tk.RIGHT
            )

            time_label.pack(
                side=tk.RIGHT,
                padx=(0, 5)
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

            time_label.pack(
                side=tk.LEFT,
                padx=(5, 0)
            )

                    # Start checking for new messages
    def start_message_refresh(self):

        # Cancel an existing refresh timer
        if self.refresh_job is not None:

            self.root.after_cancel(
                self.refresh_job
            )

        # Start a new timer
        self.refresh_job = self.root.after(
            1000,
            self.refresh_messages
        )


    # Check the server for new messages
    def refresh_messages(self):

        # Stop if no chat is open
        if self.current_room is None:
            return

        try:

            # Get the latest messages
            if self.current_room.type == "private":

                latest_messages = (
                    self.chat_service.get_one_on_one_chat(
                        self.current_room.id
                    )
                )

            else:

                latest_messages = (
                    self.chat_service.get_group_chat(
                        self.current_room.id
                    )
                )

                        # Update messages only when search is not active
            search_text = ""

            if hasattr(self, "search_entry"):
                search_text = (
                    self.search_entry.get()
                    .strip()
                    .lower()
                )

            if len(latest_messages) > len(self.current_messages):

                # Save the new messages
                self.current_messages = latest_messages

                # Do not replace search results
                if not search_text:

                    self.display_messages(
                        self.current_messages
                    )

            # Check again after 1 second
            self.refresh_job = self.root.after(
                1000,
                self.refresh_messages
            )

        except Exception as error:

            print(
                "Error receiving messages:",
                error
            )

            # Try again after 1 second
            self.refresh_job = self.root.after(
                1000,
                self.refresh_messages
            )
# hardcode data for testing

#if __name__ == "__main__":
class TestChatService:

    def __init__(self, username="User A"):
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
            {"username": "User A", "msg": "Hello..."},
            {"username": "User A", "msg": "My name is A"},
            {"username": "User B", "msg": "Hello A"},
            {"username": "User B", "msg": "My name is B"},
        ]

    def get_group_chat(self, group_id):
        return []

    # function create new group chat pop up
    def create_group_chat(self, group_chat_name):
        new_id = max((g["id"] for g in self._groups), default=0) + 1
        self._groups.append({"id": new_id, "name": group_chat_name})

if __name__ == "__main__":
    root = tk.Tk()

    chat_service = TestChatService()

    app = ChatRoomGUI(
        root,
        chat_service
    )

    root.mainloop()


