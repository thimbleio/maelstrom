from cassandra.cluster import Cluster
from cassandra.decoder import dict_factory
import cassandra

class CassandraConnection(object):
    ip = None
    kp = None

    def __init__(self, cass_ip, cass_kp):
        self.ip = cass_ip
        self.kp = cass_kp
        try:
            #self.cluster = Cluster(contact_points=self.ip, control_connection_timeout=10000.0)
            self.cluster = Cluster(self.ip)
            self.session = self.cluster.connect(self.kp)
            self.session.row_factory = dict_factory
            #self.session.default_timeout = 60.0
        except cassandra.cluster.NoHostAvailable:
            print "TimeoutError: Possibly a connection issue. If problem persists, contact admin."

    def destroy_cluster(self):
        ip = None
        kp = None
        self.cluster.shutdown()
        self.session.shutdown()

class TransactionManager:

    def __init__(self):
        pass
