from datetime import datetime
from pathlib import Path
from threading import Lock


# Store chat history inside the server folder
CHAT_HISTORY_FILE = Path(__file__).with_name("chat_history.txt")

# Protect the file when multiple users send messages at the same time
file_lock = Lock()


def save_message(username, message, room_name="General"):
    """
    Save a valid chat message to chat_history.txt.

    Each message contains:
    - date and time
    - room name
    - sender username
    - message
    """

    message = message.strip()

    # Do not store empty messages
    if not message:
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    chat_record = (
        f"{timestamp} | "
        f"Room: {room_name} | "
        f"User: {username} | "
        f"Message: {message}\n"
    )

    with file_lock:
        with CHAT_HISTORY_FILE.open("a", encoding="utf-8") as file:
            file.write(chat_record)

    return True