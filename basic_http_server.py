from socketserver import StreamRequestHandler, TCPServer, ThreadingMixIn

from request import Request


class BasicServerTCPHandler(StreamRequestHandler):
    def handle(self):
        request = Request(self.rfile)

        print('Method: ', request.method)
        print('URL: ', request.url)
        print('Protocol: ', request.protocol)
        if request.url.endswith('hello_world'):
            response_body = "<h1>Hello World</h1>"
        else:
            response_body = "<h1>Main page</h1>"
        response_body_length = str(len(response_body)).encode()

        response = [
            'HTTP/1.1 200 OK',
            'Content-Type: text/html',
            'Content-Length: ' + str(response_body_length),
            'Connection: close',
            '',
            response_body
        ]

        self.wfile.write('\r\n'.join(response).encode())


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    ...


HOST, PORT = "localhost", 8000
TCPServer.allow_reuse_address = True

with ThreadedTCPServer((HOST, PORT), BasicServerTCPHandler) as server:
    server.serve_forever()
