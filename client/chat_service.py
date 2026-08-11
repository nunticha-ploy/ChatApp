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
        return self.groups

    # Create group chat
    def create_group_chat(self, group_chat_name):

        new_id = len(self.groups) + 1

        new_group = {
            "id": new_id,
            "name": group_chat_name
        }

        self.groups.append(new_group)

        return new_group

    # Get private chat
    def get_one_on_one_chat(self, user_id):
        return []

    # Get group chat
    def get_group_chat(self, group_id):
        return []

    # Rename group chat
    def rename_group_chat(
        self,
        group_id,
        new_group_name
    ):
        pass

    # Delete group chat
    def delete_group_chat(self, group_id):
        pass

    # Send message
    def send_msg(self, room, msg):

        if not msg.strip():
            return False

        if room.type == "private":

            command = (
                f"SEND_MESSAGE|PRIVATE|"
                f"{room.name}|{msg}"
            )

        else:

            command = (
                f"SEND_MESSAGE|GROUP|"
                f"{room.id}|{msg}"
            )

        try:

            print(
                "Sending:",
                command
            )

            # Do not call recv() here.
            # The background listener receives all server messages.
            self.sock.sendall(
                command.encode()
            )

            return True

        except Exception as error:

            print(
                "Error sending message:",
                error
            )

            return False

    # Start receiving messages
    def start_message_listener(self, callback):

        self.message_callback = callback

        if self.listener_started:
            return

        self.listener_started = True

        thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )

        thread.start()

        print(
            "Message listener started."
        )

    # Receive messages from server
    def receive_messages(self):

        while True:

            try:

                data = self.sock.recv(
                    2048
                )

                if not data:
                    break

                message = data.decode().strip()

                print(
                    "Received:",
                    message
                )

                if message.startswith(
                    "MESSAGE|"
                ):

                    parts = message.split(
                        "|",
                        2
                    )

                    if len(parts) == 3:

                        sender = parts[1]
                        text = parts[2]

                        if self.message_callback:

                            self.message_callback(
                                sender,
                                text
                            )

            except Exception as error:

                print(
                    "Receive error:",
                    error
                )

                break