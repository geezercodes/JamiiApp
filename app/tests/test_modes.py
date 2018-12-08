import unittest
from app.models.models import User, Business
from werkzeug.security import check_password_hash, generate_password_hash

class TestModel(unittest.TestCase):
    def setUp(self):
        self.user = User()
        self.business = Businesses()

    def test_user_instance(self):
        Dennis = User()
        self.assertIsInstance(Dennis, User)

    def test_business_instance(self):
        Teaching = Business()
        self.assertIsInstance(Teaching, Business)

    def test_user_object_type(self):
        meshack = User()
        self.assertTrue(type(meshack) is User)

    def test_business_object_type(self):
        Teaching = Business()
        self.assertTrue(type(Teaching) is Business)

    # def test_check_password_method(self):
    #     result = self.user.check_password(check_password_hash(self.user.set_password('mypassword'),'mypassword'))
    #     self.assertEqual(result, True)
