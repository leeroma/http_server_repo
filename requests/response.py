from enum import Enum
from typing import Any


class Status(Enum):
    OK = 200, "OK"
    NOT_IMPLEMENTED = 501, "Not Implemented"

    def __init__(self, code, message):
        self.code = code
        self.message = message


class Response:
    PROTOCOL = "HTTP/1.1"

    def __init__(self, file):
        self.file = file
        self.status = Status.OK
        self.headers = []
        self.body = None
        self.file_body = None
        self.response_body_length = None

    def set_status(self, status) -> None:
        self.status = status

    def add_header(self, name: str, value: Any):
        self.headers.append(
            {"name": name, "value": value}
        )

    def set_body(self, body: str) -> None:
        self.body = body.encode()
        self.add_header('Content-Length', len(self.body))

    def _get_status_line(self) -> str:
        return f'{self.PROTOCOL} {self.status.code} {self.status.message}'

    def send(self) -> None:
        headers = self._get_response_headers()
        self.file.write(headers)

        if self.body:
            self.file.write(self.body)

        elif self.file_body:
            self._write_file_body()

    def _get_response_headers(self) -> bytes:
        status_line = self._get_status_line()
        headers = [status_line]
        for header in self.headers:
            headers.append(f'{header["name"]}: {header["value"]}')

        header_string = '\r\n'.join(headers)
        header_string += '\r\n\r\n'
        return header_string.encode()

    def _write_file_body(self) -> None:
        while True:
            data = self.file_body.read(1024)
            if not data:
                break

            self.file.write(data)
