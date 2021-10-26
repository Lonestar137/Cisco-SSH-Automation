from Mass_push import Site
from dotenv import dotenv_values
import unittest

class TestMassPush(unittest.TestCase):

    def setUp(self):
        credentials = dotenv_values('creds.env')
        self.username=credentials['USER']
        self.password=credentials['PASSWORD']
        self.secret=credentials['SECRET']

        self.device = Site(self.username, self.password, self.secret)

    def tearDown(self):
        pass

    def test_connect(self):
        print('\nTesting connection. . .')
        self.device.Mass_push([48], 'sh run | i hostname', '10.251.11')
        self.assertEqual(self.device.response, 'hostname test-3560CX')

        self.device.Mass_push([38], 'sh run | i hostname', '10.251.11')
        self.assertEqual(self.device.response, 'hostname test-Garrett2960')

    def test_CLI(self):
        pass
        #self.device.Enter_cli()
    



if __name__ == "__main__":
    unittest.main()
    











