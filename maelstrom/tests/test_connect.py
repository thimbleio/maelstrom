import unittest
import maelstrom

__author__ = 'joe'


class TestConnection(unittest.TestCase):

    local_ip = "127.0.0.1"
    local_port = "9160"
    test_keyspace = "test"

    def test_connection(self):
        maelstrom.db_utils.connect([self.local_ip], self.test_keyspace)

    def test_close(self):
        maelstrom.close()
