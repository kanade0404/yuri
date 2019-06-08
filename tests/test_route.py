from unittest import TestCase
from yuri.routes import Router
from yuri.responses import http404, http405


def sample_callback():
    return b'body'


class RouterTests(TestCase):
    def test_router_add(self):
        router = Router()
        router.add('get', '/users/', sample_callback)
        callback, args = router.match('get', '/users/')
        self.assertEqual(len(router.routes), 1)

    def test_router_404(self):
        router = Router()
        router.add('get', '/users/', sample_callback)
        callback, args = router.match('get', '/user/')
        self.assertEqual(http404, callback)

    def test_router_405(self):
        router = Router()
        router.add('get', '/users/', sample_callback)
        callback, args = router.match('post', '/users/')
        self.assertEqual(http405, callback)
