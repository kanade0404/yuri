import os
from .route import Router
from .requests import Request
from .response import TemplateResponse
from jinja2 import Environment, FileSystemLoader


class Yuri:
    def __init__(self, templates=None):
        self.router = Router()
        loader = FileSystemLoader(templates or [os.path.join(os.path.abspath('.'), 'templates')])
        self.jinja2_environment = Environment(loader=loader)

    def route(self, path=None, method='GET', callback=None):
        def decorator(callback_func):
            self.router.add(method, path, callback_func)
            return callback_func
        return decorator(callback) if callback else decorator

    def __call__(self, env, start_response):
        request = Request(env)
        callback, kwargs = self.router.match(request.method, request.path)

        response = callback(request, **kwargs)
        start_response(response.status_code, response.header_list)
        if isinstance(response, TemplateResponse):
            return response.render_body(self.jinja2_environment)
        return response.body
