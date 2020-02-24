from yuri.app import Yuri
from yuri.responses import Response

app = Yuri()


@app.route('/')
def hello(request) -> Response:
    return Response('Hello, world')
