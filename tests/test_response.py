from unittest import TestCase
from yuri.responses import Response


class ResponseTests(TestCase):
    def test_response_body(self):
        response = Response(body='test')
        self.assertEqual(response.body, [b'test'])

    def test_response_status_200(self):
        response = Response(status=200)
        self.assertEqual(response.status, 200)

    def test_response_status_code_200(self):
        response = Response(status=200)
        self.assertEqual(response.status_code, '200 OK')

    def test_response_status_201(self):
        response = Response(status=201)
        self.assertEqual(response.status, 201)

    def test_response_status_code_201(self):
        response = Response(status=201)
        self.assertEqual(response.status_code, '201 Created')

    def test_response_status_404(self):
        response = Response(status=404)
        self.assertEqual(response.status, 404)

    def test_response_status_code_404(self):
        response = Response(status=404)
        self.assertEqual(response.status_code, '404 Not Found')

    def test_response_status_405(self):
        response = Response(status=405)
        self.assertEqual(response.status, 405)

    def test_response_status_code_405(self):
        response = Response(status=405)
        self.assertEqual(response.status_code, '405 Method Not Allowed')
