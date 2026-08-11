# create service for chat room
class ChatService:

    # get client obj
    def __init__(self, sock, username):
        self.sock = sock
        self.username= username

    # get all user
    def get_all_users(self):
        self.sock.sendall("GET_USERS" .encode())
        response = self.sock.recv(2048).decode()
        print("GET_USERS response:", response)
        users = []
        if not response:
            return users
        for index, item in enumerate(response.split("|"), start=1):
            username, status = item.split(",")
            if username == self.username:
                continue
            users.append({"id": index, "username": username, "status": status})
        return users

    # get currrent user
    def get_current_user(self):
        return{"id": 0, "username": self.username, "status": "online"}

    # get all group
    def get_all_groups(self):
        return []
    #self.client.get_all_groups()

    # get private chat
    def get_one_on_one_chat(self, user_id):
        return []
    #self.client.get_one_on_one_chat(user_id)

    # get group chat
    def get_group_chat(self, group_id):
        return []
    #self.client.get_group_chat(group_id)

    # create group chat
    def create_group_chat(self, group_chat_name):
        pass#return self.client.create_group_chat(group_chat_name)

    # rename group chat
    def rename_group_chat(self, group_id, new_group_name):
        pass#return self.client.rename_group_chat(group_id, new_group_name)

    # delete group chat
    def delete_group_chat(self, group_id):
        pass#return self.client.delete_group_chat(group_id)

    # send msg
    def send_msg(self, room_id, msg):
        pass#return self.client.send_msg(room_id, msg)
