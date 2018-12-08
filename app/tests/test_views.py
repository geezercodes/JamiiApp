import unittest
from app import app


class TestViews(unittest.TestCase):

    def test_home(self):
        with app.test_client() as c:
            resp = c.get('/')
            self.assertEqual(resp.status_code, 200)

    def test_available_business(self):
        with app.test_client() as c:
            resp = c.get('/available-business')
            self.assertEqual(resp.status_code, 200)
