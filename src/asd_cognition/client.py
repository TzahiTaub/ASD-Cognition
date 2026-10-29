import socket
from datetime import datetime as dt

from asd_cognition.cli import CommandLineInterface
from asd_cognition.utils.connection import Connection

cli = CommandLineInterface()


def upload_thought(address, user_id: int, thought: str):
    serv_socket = socket.socket()
    serv_socket.connect(address)

    conn = Connection(serv_socket)

    timestamp = int(dt.now().timestamp())
    data = b"".join(map(encode, (user_id, timestamp, len(thought)), (8, 8, 4)))
    data += thought.encode()

    conn.send(data)


@cli.command
def upload(address, user, thought: str):
    try:
        upload_thought(to_address(address), int(user), thought)
        print("done")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


def encode(val: int, n_bytes):
    return val.to_bytes(n_bytes, "little")


def to_address(address_str: str) -> tuple[str, int]:
    address, port = address_str.split(":")
    return (address, int(port))


if __name__ == "__main__":
    cli.main()
