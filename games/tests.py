from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


class BasicClientTestCase(TestCase):
    fixtures = ['wsd-games-data.xml',] # Doesn't work!!

    def setUp(self):
        self.client = Client()
        
        
    def assert_url(self, url, expected_code):
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_code,
                        "url='"+url+"' responded: "+str(response.status_code)+
                        " --- "+str(expected_code)+" expected")

    def login_test_user(self):
        self.client.login(username=self.test_user_name, password=self.test_user_password)

    def logout_test_user(self):
        self.client.logout()


    def test_homepage(self):
        self.assert_url('', 200)
        self.assert_url('/', 200)

    def test_games_no_login(self):
        self.assert_url('/games/', 200)
        self.assert_url('/games/worm-game', 200)
        self.assert_url('/games/angry-birds', 200)

        self.assert_url('/games/developers/', 200)
        self.assert_url('/games/developers/rovio', 200)

        self.assert_url('/games/categories/', 200)
        self.assert_url('/games/categories/arcade', 200)

        #self.assert_url('/games/my_games', 404)

    def test_with_logins(self):
        self.client.login(username='pekkis', password='test')

        self.assert_url('/games/', 200)
        self.assert_url('/games/worm-game', 200)
        self.assert_url('/games/angry-birds', 200)

        self.assert_url('/games/developers/', 200)
        self.assert_url('/games/developers/rovio', 200)

        self.assert_url('/games/categories/', 200)
        self.assert_url('/games/categories/arcade', 200)
        self.assert_url('/games/my_games', 200)

        self.assert_url('/profiles/pekkis', 200)

        self.client.logout()
        self.assert_url('/games/', 200)


        

#class TestModels(unittest.TestCase):
#    pass

if __name__ == '__main__':
    unittest.main()
