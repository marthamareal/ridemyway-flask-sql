import unittest
import configs


class DataBaseTest(unittest.TestCase):

    def test_connection_pass(self):

        self.assertEqual(configs.start_connection(), True)
