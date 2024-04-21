from socketserver import TCPServer

from server import BasicServerTCPHandler, ThreadedTCPServer


HOST = "localhost", 1999

TCPServer.allow_reuse_address = True
with ThreadedTCPServer(HOST, BasicServerTCPHandler) as server:
    server.serve_forever()
