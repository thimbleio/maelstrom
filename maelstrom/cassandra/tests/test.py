import unittest
import maelstrom.cassandra as c

class CassandraTestCase(unittest.TestCase):

    def setUp(self, cass_ip, cass_kp):
        if not self.test_setup:
            c.start(cass_ip, cass_kp)
            self.__class__.test_setup = True

    def tearDown(self):
        pass