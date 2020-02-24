import os
import traceback
from .routes import Router
from .requests import request
from .responses import HTTPError
from jinja2 import Environment, FileSystemLoader


class Yuri:
    def __init__(self, templates=None, config=None):
        self.router = Router()
        self.config = load_config(config=config)
        self.before_requests_callbacks = []
        self.after_requests_callbacks = []
        loader = FileSystemLoader(templates or [os.path.join(os.path.abspath('.'), 'templates')])
        self.jinja2_environment = Environment(loader=loader)

    def __call__(self, env, start_response):
        response = self._handle(env)
        start_response(response.status_code, response.header_list)
        return response.body

    def before_request(self, callback):
        def decorator(callback_func):
            self.before_requests_callbacks.append(callback_func)
            return callback_func
        return decorator(callback)

    def after_request(self, callback):
        def decorator(callback_func):
            self.after_requests_callbacks.append(callback_func)
            return callback_func
        return decorator(callback)

    def _handle(self, environ):
        environ['yuri.app'] = self
        request.bind(environ)
        try:
            for before_request_callback in self.before_requests_callbacks:
                before_request_callback()
            method = environ['REQUEST_METHOD']
            path = environ['PATH_INFO'] or '/'
            callback, kwargs = self.router.match(path, method)
            response = callback(**kwargs) if kwargs else callback()
            for after_request_callback in self.after_requests_callbacks:
                wrapped_response = after_request_callback(response)
                if wrapped_response:
                    response = wrapped_response
        except HTTPError as e:
            response = e
        except BaseException as e:
            error_message = _get_exception_message(e, self.config.get('DEBUG'))
            response = HTTPError(error_message, 500)
        return response

    def route(self, path=None, method='GET', callback=None):
        def decorator(callback_func):
            self.router.add(method, path, callback_func)
            return callback_func
        return decorator(callback) if callback else decorator


def _get_exception_message(e, debug):
    if debug:
        stacktrace = '\n'.join(traceback.format_tb(e.__traceback__))
        message = f'500: Internal Server Error\n\nException:\n {repr(e)}\n\n Stacktrace:\n{stacktrace}\n'
    else:
        message = 'Internal Server Error'
    return message


def load_config(config=None):
    default_config = {
        'BASE_DIR': os.path.abspath('.'),
        'TEMPLATE_DIRS': [os.path.join(os.path.abspath('.'), 'templates')],
        'DEBUG': False
    }
    if config is not None:
        default_config.update(config)
    if 'TEMPLATE_ENVIRONMENT' not in default_config:
        env = load_jinja2_env(default_config['TEMPLATE_DIRS'])
        if env:
            default_config['TEMPLATE_ENVIRONMENT'] = env
    return default_config


def load_jinja2_env(template_dir, global_variables=None, global_filters=None, **envoptions):
    try:
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader(template_dir), **envoptions)
        if global_variables:
            env.globals.update(global_variables)
        if global_filters:
            env.filters.update(global_filters)
        return env
    except ImportError:
        pass


def current_config(key, default=None):
    return request['yuri.app'].config.get(key, default)
