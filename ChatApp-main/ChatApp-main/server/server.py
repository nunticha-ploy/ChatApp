import socket
import argparse
import threading  # This module lets us create multiple threads
from authentication import login, signup, get_all_registered_users


host = "localhost"
data_buff = 2048  # receive up to 2048 bytes at a time
backlog = 5  # up to 5 clients can wait to connect.
port = 5000

user_status = {}
connected_clients = {}


def userLoginHandle(client, address):
    print("Client connected:", address)

    try:
        data = client.recv(data_buff)

        # Check if data exists
        if data:
            message = data.decode().strip()

            # Removes accidental spaces
            parts = message.strip().split()

            if not parts:
                client.sendall("Cannot be empty".encode())
                return

            # LOGIN
            if parts[0] == "LOGIN":

                if len(parts) != 3:
                    client.sendall("Invalid LOGIN.".encode())

                else:
                    # Client sends data
                    email = parts[1]
                    password = parts[2]

                    success, reply, username = login(email, password)

                    if success:
                        # User status
                        user_status[username] = "online"
                        connected_clients[username] = client

                        client.sendall(
                            f"SUCCESS {username}".encode()
                        )

                    else:
                        client.sendall(reply.encode())

                    # Keeps the logged-in client connected
                    if success:

                        while True:
                            data = client.recv(data_buff)

                            # Wait for the next message from client
                            if not data:
                                break

                            message = data.decode().strip()

                            # LOGOUT
                            if message.upper() == "LOGOUT":

                                user_status[username] = "offline"

                                client.sendall(
                                    "Logout successfully!".encode()
                                )

                                break

                            # SEND MESSAGE
                            elif message.startswith("SEND_MESSAGE|"):

                                parts = message.split("|", 3)

                                if len(parts) != 4:
                                    client.sendall(
                                        "Invalid message format.".encode()
                                    )
                                    continue

                                command = parts[0]
                                chat_type = parts[1]
                                receiver = parts[2]
                                text = parts[3].strip()

                                # Prevent empty messages
                                if not text:
                                    client.sendall(
                                        "ERROR|EMPTY_MESSAGE".encode()
                                    )
                                    continue

                                # PRIVATE MESSAGE
                                if chat_type == "PRIVATE":

                                    if receiver in connected_clients:

                                        receiver_client = connected_clients[
                                            receiver
                                        ]

                                        chat_message = (
                                            f"MESSAGE|{username}|{text}"
                                        )

                                        # Send message to receiver
                                        receiver_client.sendall(
                                            chat_message.encode()
                                        )

                                        # Send message back to sender
                                        client.sendall(
                                            chat_message.encode()
                                        )

                                    else:

                                        client.sendall(
                                            f"ERROR|{receiver} is offline.".encode()
                                        )

                                continue

                            # GET USERS
                            elif message.upper() == "GET_USERS":

                                print("GET_USERS received")

                                registered_users = (
                                    get_all_registered_users()
                                )

                                print(
                                    "Registered users:",
                                    registered_users
                                )

                                user_list = []

                                for registered_username in registered_users:

                                    status = user_status.get(
                                        registered_username,
                                        "offline"
                                    )

                                    if registered_username in connected_clients:
                                        status = user_status[
                                            registered_username
                                        ]

                                    print(
                                        registered_username,
                                        status
                                    )

                                    user_list.append(
                                        f"{registered_username},{status}"
                                    )

                                response = "|".join(user_list)

                                client.sendall(
                                    response.encode()
                                )

                                continue

                            # OTHER MESSAGES
                            else:

                                print(
                                    f"{username}: {message}"
                                )

                                client.sendall(
                                    (
                                        "Server received: "
                                        + message
                                    ).encode()
                                )

            # SIGNUP
            elif parts[0] == "SIGNUP":

                if len(parts) != 4:
                    client.sendall(
                        "Invalid SIGNUP.".encode()
                    )

                else:

                    username = parts[1]
                    email = parts[2]
                    password = parts[3]

                    success, reply = signup(
                        username,
                        email,
                        password
                    )

                    client.sendall(
                        reply.encode()
                    )

            # OTHER CHOICE
            else:

                message = data.decode().strip()

                print(
                    "Client:",
                    message
                )

                response = (
                    "Server received: "
                    + message
                )

                client.send(
                    response.encode()
                )

    except Exception as error:

        print(
            "Error:",
            error
        )

    finally:

        if "username" in locals():

            user_status[username] = "offline"

            # Remove disconnected client
            if username in connected_clients:
                del connected_clients[username]

        client.close()

        print(
            "Client disconnected:",
            address
        )


# Create a TCP socket
def TCPserver1(port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    # Bind it to a port
    server_address = (
        host,
        port
    )

    print(
        "Starting up echo server on %s port %s"
        % server_address
    )

    sock.bind(
        server_address
    )

    # Listen
    sock.listen(
        backlog
    )

    # Loop
    while True:

        print(
            "Waiting to receive message from client"
        )

        # Accept clients
        client, address = sock.accept()

        # Start a thread
        thread = threading.Thread(
            target=userLoginHandle,
            args=(client, address)
        )

        thread.start()


# Main program
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Socket Server Example"
    )

    parser.add_argument(
        "--port",
        action="store",
        dest="port",
        type=int,
        required=True
    )

    given_args = parser.parse_args()

    port = given_args.port

    TCPserver1(port)