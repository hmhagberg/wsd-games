from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import unittest


class TestBasicClient(unittest.TestCase):
    fixtures = ['wsd-games-data.xml']

    def setUp(self):
        self.client = Client()
        
        
    def assert_url(self, url, expected_code):
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_code,
                        "url='"+url+"' responded: "+str(response.status_code)+
                        " --- "+str(expected_code)+" expected")

    def set_testUser(self):
        self.user = User.objects.create_user('johnny', 'lennon@thebeatles.com', 'johnpassword')

    def test_homepage(self):
        print(self.client.login(username='johnny', password='johnpassword'))
        self.assert_url('', 200)
        self.assert_url('/', 200)

    def test_games(self):
        self.assert_url('/games/', 200)
        #self.assert_url('/games/worm-game', 200)
        response = self.client.get('/games/worm-game', follow=True)
        print(response.status_code)


        self.assert_url('/games/developers/', 200)
        self.assert_url('/games/categories/', 200)

    def test_logins(self):
        pass
        

#class TestModels(unittest.TestCase):
#    pass

if __name__ == '__main__':
    unittest.main()