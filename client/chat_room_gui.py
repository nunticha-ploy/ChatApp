# import library
import tkinter as tk

from room_class import ChatRoom

dark_gray = "#434343"
mid_gray = "#9E9E9E"
light_gray = "#D9D9D9"
white = "#FFFFFF"
online_status = "#A5FF56"

medium_font = ("Inclusive Sans", 15)
header_font = ("Inclusive Sans", 25)
status_font = ("Inclusive Sans", 10)
name_font = ("Inclusive Sans", 10)
msg_font = ("Inclusive Sans", 10)
bold_font = ("Inclusive Sans", 15, "bold")


# create class
class ChatRoomGUI:

    def __init__(self, root, chat_service):
        # create window
        self.root = root
        self.chat_service = chat_service

        # set variable for current chat room
        self.current_room = None

        self.root.title("Company Chat")
        self.root.geometry("415x700")
        self.root.resizable(width=False, height=False)

        # create frame
        top_frame = tk.Frame(self.root, width=415, height=60, background=dark_gray)
        top_frame.grid(row=0, column=0, sticky="nsew")
        mid_frame = tk.Frame(self.root, width=415, height=580, background=white)
        mid_frame.grid(row=1, column=0, sticky="nsew")
        button_frame = tk.Frame(self.root, width=415, height=60, background=dark_gray)
        button_frame.grid(row=2, column=0, sticky="nsew")
        button_frame.pack_propagate(False)

        self.show_user_page()

        def _clear(self, frame):
            for widget in frame.winfo_children():
                widget.destroy()

        # crate text box
        msg_textbox = tk.Entry(button_frame, width=45, background=dark_gray, font=medium_font, fg=white, bd=0,
                               highlightthickness=0)
        msg_textbox.pack(side=tk.LEFT, padx=25, pady=15)

    def show_user_page(self):
        # create header
        top_frame = tk.Frame(self.root, width=415, height=60, background=dark_gray)
        top_frame.grid(row=0, column=0, sticky="nsew")

        # users part
        user_title = tk.Label(top_frame, text="USERS", font=header_font, fg=white, bd=0, )
        user_title.pack(anchor=tk.NW, padx=0, pady=15)

        # get user from server
        users = self.chat_service.get_all_users()

        for user in users:
            self.create_user_row(content, user)

        # line
        line = tk.Frame(content, width=415, height=60, background=dark_gray)
        line.pack(fill="x", pady=20)

        # groups part
        group_title = tk.Label(line, text="GROUPS", font=header_font, fg=white, bd=0, )
        group_title.pack(anchor=tk.NW, padx=0, pady=15)

        groups = self.chat_service.get_all_groups()
        for group in groups:
            self.create_group_row(content, group)

        # create group button
        create_new_group_button = tk.Button(content, text="+ create new group chat", fg=mid_gray, bd=0,
                                            command=self.create_group_chat)
        create_new_group_button.pack(anchor=tk.NW, padx=0, pady=15)

    # create user row to display
    def create_user_row(self, container, user):

        user_id = user["id"]
        username = user["username"]
        status = user["status"]

        row = tk.Frame(container, width=415, height=580, background=dark_gray)
        row.pack(fill="x", pady=20)

        # username in row
        name_label = tk.Label(row, text=username, font=header_font, fg=white, bd=0, )
        name_label.pack(anchor=tk.NW, padx=0, pady=15)

        # if else statement check status
        if status == "online":
            status_text = "Online"
            status_color = online_status
        else:
            status_text = "Offline"
            status_color = mid_gray

        # enter chat sign
        enter_chat_sign = tk.Label(row, text=">", fg=mid_gray, bd=0, )
        enter_chat_sign.pack(side=right)

        # click enter chat
        for widget in (row, name_label, enter_chat_sign, status_text):
            widget.bind("<Button-1>", lambda e, uid=user_id, name=username:
            self.open_one_on_one_chat(uid, name, status))

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

        row = tk.Frame(container, width=415, height=580, background=dark_gray)
        row.pack(fill="x", pady=20)

        # group in row
        name_label = tk.Label(row, text=group_name, font=header_font, fg=white, bd=0, )
        name_label.pack(anchor=tk.NW, padx=0, pady=15)

        # enter chat sign
        enter_chat_sign = tk.Label(row, text=">", fg=mid_gray, bd=0, )
        enter_chat_sign.pack(side=right)

        # click enter chat
        for widget in (row, name_label, enter_chat_sign):
            widget.bind("<Button-1>", lambda e, uid=group_id, name=group_name:
            self.open_one_on_one_chat(uid, name))

        # function open group chat room

    def open_group_chat(self, group_id, group_name):

        # set this room as current room
        self.current_room = ChatRoom(id=group_id, type="group", name=group_name)

        msg = self.chat_service.get_group_chat(group_id)

        self.show_chat_page(self.current_room, msg, "Group")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatRoomGUI(root)
    root.mainloop()
