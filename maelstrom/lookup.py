from uuid import uuid4
from base import Base
import db_utils as db

class LookUp(Base):
    __tablename__ = "lookup"

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
        build = "create table "+db.cass_keyspace+"."+__tablename__
        build += " ( id varchar PRIMARY KEY, model varchar, model_id uuid ) with caching = \'all\'"
        db.c.session.execute(build)
        db.c.session.execute("create index model on "
                             +db.cass_keyspace+"."+__tablename__+" (model)")

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
