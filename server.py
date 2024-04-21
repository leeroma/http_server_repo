from socketserver import StreamRequestHandler, TCPServer, ThreadingMixIn

from requests.request import Request
from requests.response import Response, Status


class BasicServerTCPHandler(StreamRequestHandler):
    def handle(self):
        request = Request(self.rfile)
        response = Response(self.wfile)
        if '.css' in request.url:
            body = self._set_css(request, response)
        elif '.js' in request.url:
            body = self._set_js(request, response)
        else:
            server_answer = self._parse_body_url(request.url)
            if '501' in server_answer:
                response.status = Status.NOT_IMPLEMENTED
            if 'white_rabbit' in request.url:
                body = self._prepare_body('static/index.html', body=server_answer)
            else:
                body = self._prepare_body('static/main.html', body=server_answer)
            self._set_html(response)

        response.add_header('Connection', 'Close')
        response.set_body(body)
        response.send()

    @staticmethod
    def _prepare_body(file, **kwargs):
        with open(file, 'r') as template:
            body = template.read()
            body = body.format(**kwargs)

        return body

    @staticmethod
    def _set_css(request: Request, response: Response):
        with open(request.url.lstrip('/')) as css:
            body = css.read()
            response.add_header('Content-Type', 'text/css')
            response.set_status(Status.OK)

        return body

    @staticmethod
    def _set_js(request: Request, response: Response):
        with open(request.url.lstrip('/')) as js:
            body = js.read()
            response.add_header('Content-Type', 'text/js')

        return body

    @staticmethod
    def _set_html(response: Response):
        response.add_header('Content-Type', 'text/html')

    @staticmethod
    def _parse_body_url(url):
        match url:
            case '/':
                return ('<div class="wrapper"><div class="text-wrapper"><h1 class="title">Follow the white rabbit . . .'
                        '</h1></div></div>')
            case '/white_rabbit':
                return ('<div class="wrapper"><div class="text-wrapper"><h1 class="title">You are living in matrix . . '
                        '.</h1></div></div>')
            case _:
                return ('<div class="wrapper"><div class="text-wrapper"><h1 class="title">501 Not Implemented . . .'
                        '</h1></div></div>')


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    ...

