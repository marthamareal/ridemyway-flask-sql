import unittest
import database_config


class DataBaseTest(unittest.TestCase):

    def test_connection_pass(self):

        self.assertEqual(database_config.start_connection(), True)
