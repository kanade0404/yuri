import json
from http.client import responses as http_response
from wsgiref.headers import Headers
from urllib.parse import urljoin

HTTP_CODES = http_response.copy()
_HTTP_STATUS_DICT = dict((k, '%d %s' % (k, v)) for (k, v) in HTTP_CODES.items())


class BaseResponse(object):
    default_status = 200
    default_charset = 'UTF-8'
    default_content_type = 'text/html;charset=UTF-8'

    def __init__(self, body=None, status=None, headers=None, charset=None):
        self._body = body if body else [b'']
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
        return self._body

    def __iter__(self):
        return iter(self.body)


class Response(BaseResponse):
    default_status = 200
    default_charset = 'UTF-8'
    default_content_type = 'text/html;charset=UTF-8'

    def __init__(self, body='', status=None, headers=None, charset=default_charset):
        if isinstance(body, str):
            body = body.encode(charset)
        iterable_body = [body]
        super().__init__(iterable_body, status, headers)
        self.charset = charset


class JSONResponse(BaseResponse):
    default_content_type = 'text/json;charset=UTF-8'

    def __init__(self, dic, status=200, headers=None, charset='UTF-8', **dump_args):
        body = [json.dumps(dic, **dump_args).encode(charset)]
        super().__init__(body=body, status=status, headers=headers, charset=charset)


class TemplateResponse(BaseResponse):
    default_content_type = 'text/html;charset=UTF-8'

    def __init__(self, filename, status=200, headers=None, charset='UTF-8', **tpl_args):
        from .app import current_config
        template_env = current_config('TEMPLATE_ENVIRONMENT')
        if template_env is None:
            raise HTTPError('TEMPLATE_ENVIRONMENT is not found in your config.')
        template = template_env.get_template(filename)
        body = [template.render(**tpl_args).encode(charset)]
        super().__init__(body, status=status, headers=headers, charset=charset)


def http404(request=None):
    return Response('404 Not Found', status=404)


def http405(request=None):
    return Response('405 Method Not Allowed', status=405)


def make_redirect_response(request, path):
    status = 303 if request.server_protocol != "HTTP/1.0" else 302
    location = urljoin(f"{request.url_schema}://{request.host}", path)
    headers = {'location': location}
    return Response(f"Redirecting to {location}", status=status, headers=headers)


class HTTPError(Response, Exception):
    default_status = 500

    def __init__(self, body, status, headers=None, charset='UTF-8'):
        super().__init__(body=body, status=status, headers=headers, charset=charset)
