from yuri.app import Yuri
from yuri.responses import TemplateResponse
from wsgiref.simple_server import make_server
from wsgi_static_middleware import StaticMiddleware

app = Yuri()


@app.route('/')
def index(request) -> TemplateResponse:
    return TemplateResponse('user.html', title='TODO LIST')


if __name__ == '__main__':
    app = StaticMiddleware(app, static_root='static')
    httpd = make_server('', 8000, app)
    httpd.serve_forever()
