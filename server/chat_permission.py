from chat_room import get_group

#function to give permission for who can change/delete group name
#Assign that only user who created a group can remove/delete
def can_edit_group(group_id, username):

    group = get_group(group_id)

    if group is None:
        return False, "Group not found."

    if group["created_by"] != username:
        return False, "Only the group creator can do that."

    return True, "OK"

