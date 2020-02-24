from unittest import TestCase
from yuri.app import Yuri
from yuri.responses import Response


class AppTests(TestCase):
    def setUp(self):
        self.app = Yuri()
        self.dummy_start_response = lambda x, y: None

        @self.app.route('/')
        def dummy_func():
            return Response('hello')

        @self.app.route('/test/{typed_id}')
        def typed_url_var(typed_id: int):
            body = 'type: {}, value: {}'.format(type(typed_id), typed_id)
            return Response(body)

        @self.app.route('/test/raise500')
        def raise500(type_id: int):
            1 / 0
            return Response("Don't reach here")
