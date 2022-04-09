import http.server
import socketserver
from http.server import HTTPStatus
from pathlib import Path
from urllib.parse import unquote
import importlib
import sys

# Most of this is copied from http.server:
# https://github.com/python/cpython/blob/3.9/Lib/http/server.py

if __name__ == "__main__" and __package__ is None:
    __package__ = "mumath2"


class MuMathHandler(http.server.SimpleHTTPRequestHandler):
    @property
    def _is_test(self):
        return self._path.name.startswith("mumath")

    @property
    def _path(self):
        return Path(self.translate_path(self.path))

    def _set_headers(self, content):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", len(content))
        # self.send_header("Last-Modified",
        #     self.date_time_string(fs.st_mtime))
        self.end_headers()

    def _set_content(self, content):
        self.wfile.write(content)

    def _get_post_data(self):
        # https://stackoverflow.com/questions/28884947/is-there-a-function-in-python-to-convert-html-entities-to-percent-encoding
        def split(string):
            key, value = string.split("=", maxsplit=1)
            return key, unquote(value)

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.replace(b"+", b" ")
        post_data = post_data.decode("utf-8")
        parameters = dict(map(split, post_data.split("&")))

        return parameters

    @staticmethod
    def _update(content, data):
        # hacky way to force reload
        for mod in list(sys.modules):
            if mod.startswith("mumath2"):
                del sys.modules[mod]
        # importlib.reload(mumath2)

        from .core import MuMath
        from .test import tests
        from functools import partial

        if data is None:
            data = "\n".join(tests)

        def apply(func):
            def _apply(lines):
                return "<br>".join(map(func, lines.splitlines()))
            return _apply

        mu = MuMath(area="chemistry")
        transformed = apply(partial(mu.convert, infer=True))(data)

        content = content.replace(b"$INPUT", data.encode("utf-8"))
        content = content.replace(b"$OUTPUT", transformed.encode("utf-8"))

        return content

    def _get_content(self, data=None):
        path = self._path
        if path.is_dir():
            path = path / "index.html"

        with open(path, mode="rb") as f:
            content = f.read()

        if self._is_test:
            return self._update(content, data)
        else:
            return content

    def do_GET(self):
        if self._path.name == "favicon.ico":
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return

        content = self._get_content()

        self._set_headers(content)
        self._set_content(content)


        # path = Path(self.translate_path(self.path))

        # print(path)

        # path = Path(self.translate_path(self.path))
        # if path.is_dir():
        #     path = path / "index"

        # if path.with_suffix(".add").is_file():
        #     # importlib.reload(core)
        #     from .core import Addup

        #     html = path.with_suffix(".html")
        #     addup = html.with_suffix(".add")
        #     self.log_message(f"Converting {html}")
        #     Addup().convert_file(addup, html)

        # super().do_GET()

    def do_POST(self):
        # https://stackoverflow.com/a/53348829
        post_data = self._get_post_data()
        content = self._get_content(post_data.get("mumath", "error"))

        self._set_headers(content)
        self._set_content(content)


def _get_best_family(*address):
    # pre-3.8
    import socket
    infos = socket.getaddrinfo(
        *address,
        type=socket.SOCK_STREAM,
        flags=socket.AI_PASSIVE,
    )
    family, _type, _proto, _canonname, sockaddr = next(iter(infos))
    return family, sockaddr


def serve(HandlerClass=http.server.BaseHTTPRequestHandler,
         ServerClass=http.server.ThreadingHTTPServer,
         protocol="HTTP/1.0", port=8000, bind=None, open=False):
    """Test the HTTP request handler class.
    This runs an HTTP server on port 8000 (or the port argument).
    """
    ServerClass.address_family, addr = _get_best_family(bind, port)

    HandlerClass.protocol_version = protocol
    with ServerClass(addr, HandlerClass) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f'[{host}]' if ':' in host else host
        url = f"http://{url_host}:{port}/"
        url = url.replace("[::]", "localhost")
        print(f"Serving HTTP on {host} port {port} ({url}) ...")
        if open:
            import webbrowser
            webbrowser.open_new_tab(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            import sys; sys.exit(0)


if __name__ == "__main__":
    import argparse
    import os
    import socket
    import contextlib
    from functools import partial

    parser = argparse.ArgumentParser()
    parser.add_argument('--cgi', action='store_true',
                       help='Run as CGI Server')
    parser.add_argument('--bind', '-b', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory '
                        '[default:current directory]')
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8000]')
    parser.add_argument('--open', action='store_true',
                        default=False,
                        help='Open new tab')
    parser.add_argument('--test', action='store_true',
                        default=False,
                        help='Run test file')

    args = parser.parse_args()
    if args.cgi:
        handler_class = http.server.CGIHTTPRequestHandler
    else:
        if args.test:
            test_directory = (Path(args.directory) / __file__).parent.as_posix()
            args.directory = test_directory

        directory = args.directory if not args.test else test_directory

        handler_class = partial(MuMathHandler, directory=args.directory)

    # ensure dual-stack is not disabled; ref #38907
    class DualStackServer(http.server.ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

    print(args.directory)

    serve(
        HandlerClass=handler_class,
        ServerClass=DualStackServer,
        port=args.port,
        bind=args.bind,
        open=args.open,
    )


