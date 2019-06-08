from unittest import TestCase
from yuri.requests import Request


class RequestTests(TestCase):
    def test_init(self):
        env = {'hoge': 'HOGE'}
        request = Request(env)
        self.assertEqual(request['hoge'], 'HOGE')

    def test_get(self):
        request = Request({'hoge': 'HOGE'})
        self.assertEqual(request.get('hoge'), 'HOGE')

    def test_getitem(self):
        request = Request({'hoge': 'HOGE'})
        self.assertEqual(request['hoge'], 'HOGE')

    def test_path_property(self):
        request = Request({'PATH_INFO': '/hoge'})
        self.assertEqual(request.path, '/hoge')

    def test_method_name(self):
        self.assertEqual(Request({'REQUEST_METHOD': 'get'}).method, 'GET')

    def test_server_protocol(self):
        self.assertEqual(Request({'SERVER_PROTOCOL': 'hoge'}).server_protocol, 'hoge')

    def test_url_schema(self):
        self.assertEqual(Request({'HTTP_X_FORWARDED_PROTO': 'hoge'}).url_scheme, 'hoge')

    def test_host(self):
        self.assertEqual(Request({'HTTP_X_FORWARDED_HOST': 'hoge'}).host, 'hoge')
