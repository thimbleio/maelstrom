from cassandra.cluster import Cluster, NoHostAvailable
from cassandra.decoder import dict_factory


class CassandraConnection(object):

    ip = None
    kp = None

    def __init__(self, cass_ip, cass_kp):
        self.ip = cass_ip
        self.kp = cass_kp
        try:
            self.cluster = Cluster(self.ip)
            self.session = self.cluster.connect(self.kp)
            self.session.row_factory = dict_factory
        except NoHostAvailable:
            print "TimeoutError: Possibly a connection issue."

    def destroy_cluster(self):
        ip = None
        kp = None
        self.cluster.shutdown()
        self.session.shutdown()


class TransactionManager:
    def __init__(self):
        pass
