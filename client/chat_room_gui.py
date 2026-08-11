# import library
import tkinter as tk
from tkinter import simpledialog, messagebox

from model.room_class import ChatRoom

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

        if group_name is None:
            return

        group_name = group_name.strip()

        #validation input field cannot be empty
        if not group_name:
            messagebox.showwarning("Invalid", "Group name cannot be empty.")
            return

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
        y = button.winfo_rooty() + button.winfo_width().winfo_height()

        option.post(x, y)

    #rename group
    def rename_group_chat(self, group_id, group_name, current_name):
        new_name = simpledialog.askstring("Rename", "New group name:", initialvalue=current_name, parent=self.root)

        if new_name is None:
            return

        group_name = group_name.strip()

        # validation input field cannot be empty
        if not new_name:
            messagebox.showwarning("Invalid", "Group name cannot be empty.")
            return

        self.chat_service.create_group_chat(new_name)
        self.show_user_page()


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
        frame = tk.Frame(self.root, background=white)
        frame.pack(fill="both", expand=True)

        # bubble message
        for message in msg:
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

        typing_label = tk.Label(typing_frame, text="Typing....", font=medium_font,
                                fg=white, bg=dark_gray)
        typing_label.pack(side=tk.LEFT, padx=20, pady=15)


# hardcode data for testing

if __name__ == "__main__":
    class TestChatService:

        def __init__(self):
            self._groups = [
                {"id": 1, "name": "Group 1"},
                {"id": 2, "name": "Group 2"},
                {"id": 3, "name": "Group 3"},
            ]

        def get_current_user(self):
            return {"id": 0, "username": "User A", "status": "online"}

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


    root = tk.Tk()

    chat_service = TestChatService()

    app = ChatRoomGUI(
        root,
        chat_service
    )

    root.mainloop()
