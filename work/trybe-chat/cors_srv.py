import http.server,socketserver
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin','https://jointrybe.com'); self.send_header('Access-Control-Allow-Private-Network','true'); super().end_headers()
    def do_OPTIONS(self):
        self.send_response(204); self.send_header('Access-Control-Allow-Methods','GET'); self.send_header('Access-Control-Allow-Headers','*'); self.end_headers()
socketserver.TCPServer(('127.0.0.1',8765),H).serve_forever()
