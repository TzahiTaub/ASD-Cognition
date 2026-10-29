from socket import socket


class Connection:
    def __init__(self, socket: socket):
        self.socket = socket

    @classmethod
    def connect(cls, host, port):
        conn = socket()
        conn.connect((host, port))
        return cls(conn)

    def __repr__(self):
        address, port = self.socket.getsockname()
        peer_address, peer_port = self.get_peer_name()
        return f"<Connection from {address}:{port} to {peer_address}:{peer_port}>"

    def get_peer_name(self):
        return self.socket.getpeername()

    def send(self, data):
        return self.socket.send(data)

    def receive(self, size):
        buf = bytearray(1024)
        view = memoryview(buf)

        total_read = 0
        while total_read < size:
            read = self.socket.recv_into(view[total_read:], nbytes=size)
            if not read:
                raise ConnectionAbortedError(
                    f"Connection closed after {total_read}/{size} bytes read."
                )
            total_read += read
        return buf[:size]

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
