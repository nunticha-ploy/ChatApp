# create service for chat room

import threading


class ChatService:

    def __init__(self, sock, username):
        self.sock = sock
        self.username = username

        self.groups = []
        self.users = None

        self.message_callback = None
        self.listener_started = False

    # Get all users
    def get_all_users(self):

        # GET_USERS is requested only once.
        # After the message listener starts, the listener owns recv().
        if self.users is not None:
            return self.users

        self.sock.sendall(
            "GET_USERS".encode()
        )

        response = self.sock.recv(
            2048
        ).decode()

        print(
            "GET_USERS response:",
            response
        )

        users = []

        if not response:
            self.users = users
            return users

        for index, item in enumerate(
            response.split("|"),
            start=1
        ):

            if "," not in item:
                continue

            username, status = item.split(
                ",",
                1
            )

            if username == self.username:
                continue

            users.append({
                "id": index,
                "username": username,
                "status": status
            })

        self.users = users

        return users

    # Get current user
    def get_current_user(self):

        return {
            "id": 0,
            "username": self.username,
            "status": "online"
        }

    # Get all groups
    def get_all_groups(self):
        self.sock.sendall("GET_GROUPS".encode())
        response = self.sock.recv(2048).decode()

        if response == "NO_GROUPS":
            self.groups = []
            return self.groups

        groups = []
        for item in response.split("|"):
            group_id, group_name = item.split(",", 1)
            groups.append({"id": group_id, "name": group_name, "members": [self.username]})

        self.groups = groups
        return self.groups

    # find group by id
    def find_group(self, group_id):
        for group in self.groups:
            if group["id"] == group_id:
                return group
        return None

    # add member to group
    def add_member(self, group_id, username):
        group = self.find_group(group_id)
        if group is None:
            return False, "Group not found."
        username = username.strip()
        if not username:
            return False, "Username cannot be empty."
        # existing_users = [u["username"] for u in self.get_all_users()]
        # if username not in existing_users:
        #     return False, "User not found."
        # if username in group["members"]:
        #     return False, "User is already a member."
        # group["members"].append(username)
        # return True, "Member added successfully."

        #send command to server, let server know add a new user
        add = f"ADD_MEMBER|{group_id}|{username}"
        self.sock.sendall(add.encode())
        response = self.sock.recv(2048).decode()
        return response

    # remove member from group
    def remove_member(self, group_id, username):
        group = self.find_group(group_id)
        if group is None:
            return False, "Group not found."
        username = username.strip()
        # if username == self.username:
        #     return False, "Use Leave Group to leave the group."
        # if username not in group["members"]:
        #     return False, "User is not a member of this group."
        # group["members"].remove(username)
        # return True, "Member removed successfully."

        #send command to server, let server know add a new user
        remove = f"REMOVE_MEMBER|{group_id}|{username}"
        self.sock.sendall(remove.encode())
        response = self.sock.recv(2048).decode()
        return response


    # current user leaves group
    def leave_group(self, group_id):
        group = self.find_group(group_id)

        if group is None:
            return False, "Group not found."

        # if self.username not in group["members"]:
        #     return False, "You are not a member of this group."
        # group["members"].remove(self.username)
        # # remove group from current user's group list
        # self.groups.remove(group)
        # return True, "You left the group successfully."

        #send command to server, let server know add a new user
        leave = f"LEAVE_GROUP|{group_id}"
        self.sock.sendall(leave.encode())
        response = self.sock.recv(2048).decode()
        return response

    # get group members
    def get_group_members(self, group_id):
        group = self.find_group(group_id)

        if group is None:
            return []

        return group["members"]

    # Get private chat
    def get_one_on_one_chat(self, user_id):
        return []

    # Get group chat
    def get_group_chat(self, group_id):
        return []

    # create group chat
    def create_group_chat(self, group_chat_name):
        create = f"CREATE_GROUP: {group_chat_name}"
        self.sock.sendall(create.encode())
        response = self.sock.recv(2048).decode()
        return response

    # Rename group chat
    def rename_group_chat(self, group_id, new_group_name):
        msg = f"RENAME_GROUP:{group_id}:{new_group_name}"
        self.sock.sendall(msg.encode())
        response = self.sock.recv(2048).decode()
        return response
      
    # Delete group chat
    def delete_group_chat(self, group_id):
        msg = f"DELETE_GROUP:{group_id}"
        self.sock.sendall(msg.encode())
        response = self.sock.recv(2048).decode()
        return response

    # Send message
    def send_msg(self, room, msg):
        message = msg.strip()
        if not message:
            return False
        try:
            self.sock.sendall(message.encode())
            response = self.sock.recv(2048).decode()
            print("Server:", response)
            return True
        except Exception as error:
            print("Error sending message:", error)
            return False

    # Start receiving messages
    def start_message_listener(self, callback):
        self.message_callback = callback
        if self.listener_started:
            return
        self.listener_started = True
        thread = threading.Thread(target=self.receive_messages, daemon=True)
        thread.start()
        print("Message listener started.")

    # Receive messages from server
    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(2048)
                if not data:
                    break
                message = data.decode().strip()
                print("Received:", message)
                if message.startswith("MESSAGE|"):
                    parts = message.split("|", 2)
                    if len(parts) == 3:
                        sender = parts[1]
                        text = parts[2]
                        if self.message_callback:
                            self.message_callback(sender, text)
            except Exception as error:
                print("Receive error:", error)
                break