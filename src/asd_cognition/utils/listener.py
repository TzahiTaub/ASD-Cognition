import socket

from asd_cognition.utils.connection import Connection


class Listener:
    def __init__(self, port, host="0.0.0.0", backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr

    def _address(self):
        return (self.host, self.port)

    def __repr__(self):
        return f"Listener(port={self.port}, host='{self.host}', backlog={self.backlog}, reuseaddr={self.reuseaddr})"

    def start(self):
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # check
        server.bind(self._address())
        server.listen(1000)  # parallel connections
        self.server = server

    def stop(self):
        self.server.close()

    def accept(self):
        conn, _ = self.server.accept()
        return Connection(conn)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()
