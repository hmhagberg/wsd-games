from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import unittest


class TestBasicClient(unittest.TestCase):
    FIXTURES = ['wsd-games-data'] # Doesn't work!!

    def setUp(self):
        self.client = Client()
        
        
    def assert_url(self, url, expected_code):
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_code,
                        "url='"+url+"' responded: "+str(response.status_code)+
                        " --- "+str(expected_code)+" expected")

    def set_testUser(self):
        self.test_user_name = 'johnny'
        self.test_user_password = 'johnpassword'
        self.test_user_email = 'lennon@thebeatles.com'
        self.user = User.objects.create_user(self.test_user_name, self.test_user_email, self.test_user_email)

    def login_test_user(self):
        self.client.login(username=self.test_user_name, password=self.test_user_password)

    def logout_test_user(self):
        self.client.logout()

    def test_homepage(self):
        self.assert_url('', 200)
        self.assert_url('/', 200)

    def test_games(self):
        self.assert_url('/games/', 200)
        self.assert_url('/games/', 200)
        self.assert_url('/games/developers/', 200)
        self.assert_url('/games/categories/', 200)

    def test_logins(self):
        pass
        

#class TestModels(unittest.TestCase):
#    pass

if __name__ == '__main__':
    unittest.main()
