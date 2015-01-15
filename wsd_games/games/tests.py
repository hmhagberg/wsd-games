from django.test import TestCase
from django.test import Client
import unittest

class TestBasicClient(unittest.TestCase):

	def setUp(self):
		self.client = Client()

	def test_client_homepage(self):
		response = self.client.get('/games/')
		self.assertEqual(response.status_code, 200, "200 on '/'")
		print('test works')

if __name__ == '__main__':
    unittest.main()