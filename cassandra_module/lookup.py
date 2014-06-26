from uuid import uuid4
from base import Base
import db_utils as db

CASSANDRA_KEYSPACE = 'gradfly'
CASSANDRA_IP = ['192.241.181.163', '107.170.88.98']


class LookUp(Base):
    __tablename__ = "lookuptable"

    defaults = {
        "id": "",
        "model": "",
        "model_id": uuid4()
    }

    def __init__(self, *args, **kwargs):
        self.update_data(**self.defaults)
        Base.__init__(self, *args, **kwargs)

    @staticmethod
    def _build(__tablename__):
        build = "create table "+CASSANDRA_KEYSPACE+"."+__tablename__
        build += " ( id varchar PRIMARY KEY, model varchar, model_id uuid ) with caching = \'all\'"
        db.c.session.execute(build)
        db.c.session.execute("create index model on "
                             +CASSANDRA_KEYSPACE+"."+__tablename__+" (model)")

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
