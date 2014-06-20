from base import Base
import db_utils as db
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel
import cassandra
from uuid import uuid4
from itertools import izip

CASSANDRA_KEYSPACE = 'gradfly'
CASSANDRA_IP = ['192.241.181.163', '107.170.88.98']

class Search(Base):
    __tablename__ = "search"

    defaults = {
        "id" : "",
        "model_type" : "",
        "model_ids" : set([uuid4()])
    }


    def __init__(self, *args, **kwargs):
        self.model_ids = set()
        self.update_data(**self.defaults)
        Base.__init__(self, *args, **kwargs)

    @staticmethod
    def _build(__tablename__):
        build = "create table "+CASSANDRA_KEYSPACE+"."+__tablename__
        build += " ( id varchar PRIMARY KEY, model_type varchar, model_ids set<uuid> ) with caching = \'all\'"
        db.c.session.execute(build)
        db.c.session.execute("create index model_type on "
                +CASSANDRA_KEYSPACE+"."+__tablename__+" (model_type)")

    @classmethod
    def build(cls):
        cls._build(cls.__tablename__)

    @classmethod
    def drop(cls):
        cls._drop(cls.__tablename__)

    @classmethod
    def rebuild(cls):
        try:
            cls.drop()
        except Exception:
            pass
        cls.build()

    @staticmethod
    def _build_insert_query(__tablename__, id, **kwargs):
        query = "update "+CASSANDRA_KEYSPACE+"."+__tablename__
        query += " set model_type=\'"+kwargs['model_type']+"\'"
        query += ", model_ids = model_ids + { "
        for model_id in kwargs['model_ids']:
            query += str(model_id)+", " 
        query = query[:-2] + "} where id=\'"+id+"\'"
        return query

    @staticmethod
    def _set_row(__tablename__, id, **kwargs):
        query = _build_insert_query(__tablename__, id, **kwargs)
        return db.c.session.execute(
            SimpleStatement(query, consistency_level=ConsistencyLevel.QUORUM))

    @staticmethod
    def _set_rows(__tablename__, ids, rows):

        list_of_kwargs = [r.__dict__ for r in rows]
        #typechecking   
        batch = "begin batch "
        for uuid, kwargs in izip(ids, list_of_kwargs):
            batch += Search._build_insert_query(__tablename__, **kwargs)+" "
        batch += "apply batch"
        try:
            db.c.session.execute(
                SimpleStatement(batch, consistency_level=ConsistencyLevel.QUORUM)
            )
        except cassandra.InvalidRequest:
            print "ColumnFamilyError: no such column family exists."

    @classmethod
    def _multi_commit(cls, list_of_rows):
        ids = []
        kwargs = []
        for row in list_of_rows:
            ids.append(row.id)
            kwargs.append(row.__dict__)
        cls._set_rows(cls.__tablename__, ids, kwargs)

    def _commit(self):
        self._set_row(self.__tablename__, **self.__dict__)
