# create room entity

class ChatRoom:
    def __init__(self, id, type, name):
        self.id = id
        self.type = type
        self.name = name

    # create property chat room type as private for 1-1 chat
    @property
    def one_on_one_chat(self):
        return self.type == "private"

    # create property chat room type as group for group chat
    @property
    def group_chat(self):
        return self.type == "group"
