import cgi
import json
import threading
from urllib.parse import parse_qs


class Request:
    def __init__(self, environ=None, charset='utf-8'):
        self.environ = {} if environ is None else environ
        self._body = None
        self.charset = charset
        self._forms = None

    def get(self, value, default=None):
        return self.environ.get(value, default)

    @property
    def path(self):
        return self.environ['PATH_INFO'] or '/'

    @property
    def method(self):
        return self.environ['REQUEST_METHOD'].upper()

    @property
    def server_protocol(self):
        return self.environ['SERVER_PROTOCOL']

    @property
    def url_scheme(self):
        return self.environ.get('HTTP_X_FORWARDED_PROTO') or self.environ.get('wsgi.url_scheme', 'http')

    @property
    def host(self):
        return self.environ.get('HTTP_X_FORWARDED_HOST') or self.environ.get('HTTP_HOST')

    @property
    def form(self):
        if self._forms is None:
            form = cgi.FieldStorage(
                fp=self.environ['wsgi.input'],
                environ=self.environ,
                keep_blank_values=True
            )
            self._forms = {k: form[k].value for k in form}
        return self._forms

    @property
    def query(self):
        return parse_qs(self.environ['QUERY_STRING'])

    @property
    def body(self):
        if self._body is None:
            content_length = int(self.environ.get('CONTENT_LENGTH', 0))
            self._body = self.environ['wsgi.input'].read(content_length)
        return self._body

    @property
    def text(self):
        return self.body.decode(self.charset)

    @property
    def json(self):
        return json.loads(self.body)

    def __getitem__(self, key):
        return self.environ[key]

    def __delitem__(self, key):
        self[key] = ''
        del (self.environ[key])

    def __len__(self):
        return len(self.environ)


def _local_property():
    ls = threading.local()

    def fget(_):
        try:
            return ls.var
        except AttributeError:
            raise RuntimeError('Request context not initialized.')

    def fset(_, value):
        ls.var = value

    def fdel(_):
        del ls.var

    return property(fget, fset, fdel, 'Thread-local property')


class LocalRequest(Request):
    bind = Request.__init__
    environ = _local_property()
    _body = _local_property()
    _forms = _local_property()


request = LocalRequest()
