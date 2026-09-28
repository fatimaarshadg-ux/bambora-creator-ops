"""Local helper server on 127.0.0.1:8765.

Chrome loads chat-helpers.js, roster-scan.js and sample-status.js from here during every sweep,
so jointrybe.com pages need the CORS and private-network headers below.

2026-09-28: was socketserver.TCPServer, which handles one request at a time. A single half-open
connection (a health check that timed out, a tab Chrome closed mid-request) blocked every later
request, and the chat stream then failed with nothing in the sweep output to explain it.
ThreadingHTTPServer with daemon threads means one stuck client can no longer take the server down.
The served folder is pinned to this file's own folder so it never depends on the caller's cwd.
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = str(Path(__file__).resolve().parent)
ADDR = ("127.0.0.1", 8765)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "https://jointrybe.com")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def log_message(self, fmt, *args):
        pass  # the server runs hidden; its output goes nowhere useful


class Server(ThreadingHTTPServer):
    daemon_threads = True      # a stuck client thread never holds up shutdown
    allow_reuse_address = True  # restarting straight after a stop does not hit "address in use"


if __name__ == "__main__":
    Server(ADDR, Handler).serve_forever()
