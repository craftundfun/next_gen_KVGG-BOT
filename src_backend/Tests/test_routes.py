import unittest

from src_backend import createApp


class BasicTests(unittest.TestCase):

    # Set up test client
    def setUp(self):
        app = createApp()
        app.testing = True
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
