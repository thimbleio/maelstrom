from cassandra.cluster import Cluster
from cassandra.decoder import dict_factory
import cassandra

CASSANDRA_KEYSPACE = 'gradfly'
CASSANDRA_IP = ['192.241.181.163', '107.170.88.98']

class CassandraConnection(object):

    def __init__(self):
        try:
            self.cluster = Cluster(contact_points=CASSANDRA_IP)#, control_connection_timeout=10000.0)
            self.session = self.cluster.connect(CASSANDRA_KEYSPACE)
            self.session.row_factory = dict_factory
            #self.session.default_timeout = 60.0
        except cassandra.cluster.NoHostAvailable:
            print "TimeoutError: Possibly a connection issue. If problem persists, contact admin."

    def destroy_cluster(self):
        self.cluster.shutdown()
        self.session.shutdown()

class TransactionManager:

    def __init__(self):
        pass
