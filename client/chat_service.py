# create service for chat room
class ChatService:

    #mockup data for test
    def __init__(self):
        self.current_user = {"id": "u1", "username": "User A", "status": "online"}

        self.users = [
            {"id": "u2", "username": "User B", "status": "online"},
            {"id": "u3", "username": "User C", "status": "offline"},
            {"id": "u4", "username": "User D", "status": "offline"},
        ]

        self.groups = [
            {"id": "g1", "name": "Group 1"},
            {"id": "g2", "name": "Group 2"},
            {"id": "g3", "name": "Group 3"},
        ]

        # messages keyed by room_id (user_id for 1-on-1, group_id for group)
        self.messages = {
            "u2": [
                {"sender": "User A", "text": "Hello..."},
                {"sender": "User A", "text": "My name is A"},
                {"sender": "User B", "text": "Hello A"},
                {"sender": "User B", "text": "My name is B"},
            ],
        }

    # get client obj
    #def __init__(self):
    #    self.client = "client"

    # get all user
    def get_all_users(self):
        return self.client.get_all_users()

    # get all group
    def get_all_groups(self):
        return self.client.get_all_groups()

    # get private chat
    def get_one_on_one_chat(self, user_id):
        return self.client.get_one_on_one_chat(user_id)

    # get group chat
    def get_group_chat(self, group_id):
        return self.client.get_group_chat(group_id)

    # create group chat
    def create_group_chat(self, group_chat_name):
        return self.client.create_group_chat(group_chat_name)

    # rename group chat
    def rename_group_chat(self, group_id, new_group_name):
        return self.client.rename_group_chat(group_id, new_group_name)

    # delete group chat
    def delete_group_chat(self, group_id):
        return self.client.delete_group_chat(group_id)

    # send msg
    def send_msg(self, room_id, msg):
        return self.client.send_msg(room_id, msg)
