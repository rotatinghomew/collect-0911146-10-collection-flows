from contextlib import contextmanager
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen


@dataclass
class Reply:
    status: int = 200
    body: bytes = b''
    headers: dict = field(default_factory=dict)

    @classmethod
    def json(cls, value, status=200, headers=None):
        return cls(status, json.dumps(value, ensure_ascii=False).encode(),
                   {'Content-Type': 'application/json; charset=utf-8', **(headers or {})})


@contextmanager
def serve(site):
    class Handler(BaseHTTPRequestHandler):
        def handle_request(self):
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            response = site.handle(self.command, self.path, dict(self.headers), body)
            self.send_response(response.status)
            for name, value in response.headers.items():
                self.send_header(name, value)
            self.send_header('Content-Length', str(len(response.body)))
            self.end_headers()
            self.wfile.write(response.body)

        do_GET = handle_request
        do_POST = handle_request
        do_PUT = handle_request

        def log_message(self, *args):
            return None

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield 'http://127.0.0.1:' + str(server.server_address[1])
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)


def request(url, body=None, headers=None, method=None):
    payload = None if body is None else json.dumps(body).encode()
    supplied = {'Accept': 'application/json', **(headers or {})}
    if payload is not None:
        supplied['Content-Type'] = 'application/json'
    outgoing = Request(url, data=payload, headers=supplied, method=method)
    try:
        response = urlopen(outgoing, timeout=4)
    except HTTPError as error:
        response = error
    with response:
        return Reply(response.status, response.read(), dict(response.headers))
