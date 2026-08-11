
#Assign how sever adjust data

#assign chat_file variable
chat_file = "chat.txt"

#function get all groups
def get_all_groups():
    groups = []

    with open(chat_file, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            parts = line.split("|")

            if parts[0] == "GROUP":
                groups.append({
                    "id": int(parts[1]),
                    "name": parts[2],
                    "created_by": parts[3]
                })
    return groups

#function get group by id
def get_group_by_id(group_id):
    groups = get_all_groups()

    for group in groups:
        if group["id"] == int(group_id):
            return group

    return None

#function create group
def create_group(group_name, username):
    groups = get_all_groups()

    new_id = max((group["id"] for group in groups), default=0)+1

    with open(chat_file, "a") as f:
        f.write(f"GROUP|{new_id}|{group_name}|{username}\n")

    return new_id
