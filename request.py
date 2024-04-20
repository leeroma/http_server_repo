from typing import Any


class Request:
    def __init__(self, file) -> None:
        self.file = file

        self.method: str = ''
        self.url: str = ''
        self.protocol: str = ''

        self.headers: dict = {}

        self.body: Any = None

        self.parse_request_line()
        self.parse_headers()
        self.parse_body()

    def parse_request_line(self) -> None:
        request_line: str = self.read_line()

        self.method, self.url, self.protocol = request_line.split(' ')
        if self.protocol != 'HTTP/1.1':
            raise ValueError('Invalid protocol')

    def parse_headers(self) -> None:
        while True:
            header: str = self.read_line()

            if header == '':
                break

            header_name, header_value = header.split(': ')
            self.headers[header_name] = header_value

    def read_line(self) -> str:
        return self.file.readline().decode().strip()

    def parse_body(self):
        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            self.body = self.file.read(content_length)
