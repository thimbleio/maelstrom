class NoSuchIndexException(Exception):
    def __init__(self, key):
        self.key = key
        self.message = "No value with key "+str(key)+"exists."


class TimeoutException(Exception):
    def __init__(self):
        self.message = "Database timeout. "+ \
                       "If problem persists, contact admin."


class CassandraTypeException(Exception):
    def __init__(self, attempted_type, attempted_prop):
        self.type = attempted_type
        self.prop = attempted_prop
        self.message = "Type mismatch; Cassandra does not anticipate type "+ \
                       self.type+" for property "+self.prop


class NoSuchColumnFamilyException(Exception):
    def __init__(self, cf):
        self.cf = cf
        self.message = "No such column family "+self.cf+" exists. Try building it."


class NoSuchColumnException(Exception):
    def __init__(self, column):
        self.column = column
        self.message = "Column "+self.column+" does not exists."