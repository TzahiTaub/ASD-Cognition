import sys
from datetime import datetime
from pathlib import Path

from asd_cognition.website import RoutingHTTPRequestHandler, Website


def create_index_html(data_dir: Path):
    _INDEX_HTML = """
    <html>
        <head></head>
        <body>
            <ul>
                {users}
            </ul>
        </body>
    </html>
    """

    _USER_LINE_HTML = """
    <li><a href="/users/{user_id}">user {user_id}</a></li>
    """

    users_html = []
    for user_dir in data_dir.iterdir():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    index_html = _INDEX_HTML.format(users="\n".join(users_html))
    return index_html.encode()


def create_user_html(user_id: str, user_dir: Path):
    _USER_HTML = """
    <html>
        <head>
            <title>Brain Computer Interface: User {user_id}</title>
        </head>
        <body>
            <table>
            {thoughts}
        </table>

        </body>
    </html>
    """

    _THOUGHT_LINE_HTML = """
    <tr>
        <td>{timestamp}</td>
        <td>{thought}</td>
    </tr>
    """

    thoughts_html = []
    for thought_file in user_dir.iterdir():
        with thought_file.open() as f:
            thought = f.read()
        ts = thought_file.stem
        dt = datetime.strptime(ts, "%Y-%m-%d_%H-%M-%S")
        formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
        thoughts_html.append(
            _THOUGHT_LINE_HTML.format(timestamp=formatted, thought=thought)
        )

    user_html = _USER_HTML.format(user_id=user_id, thoughts="\n".join(thoughts_html))
    return user_html.encode()


class DataDirHttpHandler(RoutingHTTPRequestHandler):
    def __init__(self, *args, data_dir: Path, **kwargs):
        self.data_dir = data_dir
        super().__init__(*args, **kwargs)


def run_webserver(address, data_dir: Path):
    website = Website()

    @website.route("/")
    def index():
        index_html = create_index_html(data_dir)
        return 200, index_html

    @website.route(r"^/users/(\d+)$")
    def user_page(user_id: str):
        user_dir = data_dir / user_id
        if not user_dir.exists() or not user_dir.is_dir():
            return 404, None, None
        user_html = create_user_html(user_id, user_dir)
        return 200, user_html

    website.run(address)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(f"USAGE: {sys.argv[0]} <address> <data_dir>")
        sys.exit(1)

    address, port = sys.argv[1].split(":")
    data_dir = Path(sys.argv[2])
    try:
        run_webserver((address, int(port)), data_dir)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
