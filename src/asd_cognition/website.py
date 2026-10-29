import re
from collections.abc import Callable
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer


class Response:
    """
    A text http response helper.
    """

    def __init__(self, status_code: int, body: bytes | str | None = None):
        self.status_code = status_code
        self.content_type = "text/html" if body is not None else None
        if body is not None and isinstance(body, str):
            self.body = body.encode()
        else:
            self.body = body

    def respond(self, request_handler: BaseHTTPRequestHandler):
        request_handler.send_response(self.status_code)
        if self.content_type:
            request_handler.send_header("Content-type", self.content_type)
        request_handler.end_headers()
        if self.body:
            request_handler.wfile.write(self.body)


class RoutingHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, routes: dict[str, Callable], **kwargs):
        self.routes = routes
        super().__init__(*args, **kwargs)

    def do_GET(self):
        for path, handler in self.routes.items():
            if match := re.fullmatch(path, self.path):
                status_code, body = handler(*match.groups())
                response = Response(status_code, body)
                response.respond(self)
                return
        Response(404).respond(self)


class Website:
    def __init__(self):
        self.routes: dict[str, Callable] = {}

    def route(self, path: str):
        def decorator(f: Callable):
            if path in self.routes:
                raise ValueError(f"Route {path} already exists")
            self.routes[path] = f
            return f

        return decorator

    def run(self, address: tuple[str, int]):
        server = HTTPServer(
            address, partial(RoutingHTTPRequestHandler, routes=self.routes)
        )
        server.serve_forever()
