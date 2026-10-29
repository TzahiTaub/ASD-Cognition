import socket
from collections.abc import Buffer
from datetime import datetime as dt
from pathlib import Path
from threading import Thread

from asd_cognition.cli import CommandLineInterface
from asd_cognition.utils.listener import Listener

Socket = socket.socket
Address = tuple[str, int]


class EncodingSizes:
    USER_ID = 8
    TIMESTAMP = 8
    THOUGHT_SIZE = 4


TIMESTAMP_OFFSET = EncodingSizes.USER_ID
THOUGHT_SIZE_OFFSET = TIMESTAMP_OFFSET + EncodingSizes.TIMESTAMP
THOUGHT_OFFSET = THOUGHT_SIZE_OFFSET + EncodingSizes.THOUGHT_SIZE

cli = CommandLineInterface()


def write_to_file(user_id: int, ts: int, thought: str, data_dir: str):
    user_dir = Path(data_dir) / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    ts_str = dt.fromtimestamp(ts).strftime("%Y-%m-%d_%H-%M-%S")
    with open(user_dir / f"{ts_str}.txt", "a") as f:
        is_empty = f.tell() == 0
        if not is_empty:
            f.write("\n")  # Add a newline separator if the file already has content.
        f.write(f"{thought}")


def handle_connection_until_disconnected(
    conn: Socket, client_address: Address, data_dir: str
):
    data = b""
    while new_data := conn.recv(1024):
        data += new_data
    user_id, ts, thought = parse(data)
    write_to_file(user_id, ts, thought, data_dir)
    conn.close()


def handle_connection_until_schema_ends(
    conn: Socket, client_address: Address, data_dir: str
):
    buf = bytearray(1024)
    view = memoryview(buf)

    read = 0
    while read < THOUGHT_OFFSET:
        read += conn.recv_into(view[read:])
    user_id, ts, thought_size = parse_header(buf)

    thought_read = read - THOUGHT_OFFSET
    while thought_read < thought_size:
        thought_read += conn.recv_into(view[read + thought_read :])
    write_to_file(
        user_id,
        ts,
        buf[THOUGHT_OFFSET : THOUGHT_OFFSET + thought_size].decode(),
        data_dir,
    )


def run_server(address: Address, data_dir: str):
    host, port = address
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    with Listener(port, host) as server:
        while True:
            conn = server.accept()
            Thread(
                target=handle_connection_until_schema_ends,
                args=(conn, conn.get_peer_name(), data_dir),
            ).start()


def parse_header(data: Buffer) -> tuple[int, int, int]:
    try:
        data = memoryview(data)
        user_id = int.from_bytes(data[:TIMESTAMP_OFFSET], "little")
        ts = int.from_bytes(data[TIMESTAMP_OFFSET:THOUGHT_SIZE_OFFSET], "little")
        thought_size = int.from_bytes(
            data[THOUGHT_SIZE_OFFSET:THOUGHT_OFFSET], "little"
        )
        return user_id, ts, thought_size
    except Exception as e:
        raise ValueError(e)


def parse(data: bytes) -> tuple[int, int, str]:
    try:
        user_id, ts, _thought_size = parse_header(data)
        thought = data[20:].decode()
        return user_id, ts, thought
    except Exception as e:
        raise ValueError(e)


@cli.command
def run(address, data):
    """Run the server."""
    address, port = address.split(":")
    run_server((address, int(port)), data)


if __name__ == "__main__":
    cli.main()
