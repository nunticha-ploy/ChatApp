# create service for chat room
class ChatService:

    # get client obj
    def __init__(self):
        self.client = "client"

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
