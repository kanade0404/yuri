import re
from .responses import make_redirect_response, http404, http405


class Router:
    def __init__(self, append_slash=True):
        self.routes = []
        self.append_slash = append_slash

    def add(self, method, path, callback):
        self.routes.append({
            'method': method,
            'path': path,
            'path_compiled': re.compile('^(%s)$' % path),
            'callback': callback
        })

    def match(self, method, path):
        if self.append_slash and not path.endswith('/'):
            def callback(request):
                return make_redirect_response(request, path + '/')
            return callback, {}

        error_callback = http404
        for r in self.routes:
            matched = r['path_compiled'].match(path)
            if not matched:
                continue

            error_callback = http405
            url_vars = matched.groupdict()
            if method == r['method']:
                return r['callback'], url_vars
        return error_callback, {}
