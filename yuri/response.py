import json
from http.client import responses as http_response
from wsgiref.headers import Headers
from urllib.parse import urljoin


class Response:
    default_status = 200
    default_charset = 'utf-8'
    default_content_type = 'text/html;charset=UTF-8'

    def __init__(self, body='', status=None, headers=None, charset=None):
        self._body = body
        self.status = status or self.default_status
        self.headers = Headers()
        self.charset = charset or self.default_charset

        if headers:
            for name, value in headers.items():
                self.headers.add_header(name, value)

    @property
    def status_code(self):
        return "%d %s" % (self.status, http_response[self.status])

    @property
    def header_list(self):
        if 'Content-Type' not in self.headers:
            self.headers.add_header('Content-Type', self.default_content_type)
        return self.headers.items()

    @property
    def body(self):
        if isinstance(self._body, str):
            return [self._body.encode(self.charset)]
        return [self._body]


class JSONResponse(Response):
    default_content_type = 'text/json;charset=UTF-8'

    def __init__(self, dic, status=200, headers=None, charset=None, **dump_args):
        self.dic = dic
        self.json_dump_args = dump_args
        super().__init__('', status=status, headers=headers, charset=charset)

    @property
    def body(self):
        return [json.dumps(self.dic, **self.json_dump_args).encode(self.charset)]


class TemplateResponse(Response):
    default_content_type = 'text/html;charset=UTF-8'

    def __init__(self, filename, status=200, headers=None, charset=None, **tpl_args):
        self.filename = filename
        self.tpl_args = tpl_args
        super().__init__(body='', status=status, headers=headers, charset=charset)

    def render_body(self, jinja2_environment):
        template = jinja2_environment.get_template(self.filename)
        return [template.render(**self.tpl_args).encode(self.charset)]


def http404(env, start_response):
    return Response('404 Not Found', status=404)


def http405(env, start_response):
    return Response('405 Method Not Allowed', status=405)


def make_redirect_response(request, path):
    status = 303 if request.server_protocol != "HTTP/1.0" else 302
    location = urljoin(f"{request.url_schema}://{request.host}", path)
    headers = {'location': location}
    return Response(f"Redirecting to {location}", status=status, headers=headers)