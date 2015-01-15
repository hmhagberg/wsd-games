from django.test import TestCase
from django.test import Client
import unittest


class TestBasicClient(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def assert_url(self, url, expected_code):
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_code,
                        "url='"+url+"' responded: "+str(response.status_code)+
                        " --- "+str(expected_code)+" expected")

    def test_homepage(self):
        self.assert_url('', 200)
        self.assert_url('/', 200)

    def test_games(self):
        #Not implemented yet
        #self.assert_url('games/', 200)
        self.assert_url('games/developers/', 200)
        self.assert_url('games/categories/', 200)



if __name__ == '__main__':
    unittest.main()