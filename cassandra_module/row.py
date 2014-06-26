from datetime import datetime
import db_utils as db


class Row(object):

    _get_row_by_id = staticmethod(db.get_row_by_id)
    _get_row_spec_prop = staticmethod(db.get_row_spec_prop)
    _get_rows_by_id = staticmethod(db.get_rows_by_id)
    _set_row = staticmethod(db.insert_row_data)
    _set_rows = staticmethod(db.set_rows_data)
    _build = staticmethod(db.create_column_family)
    _drop = staticmethod(db.drop_column_family)
    _delete = staticmethod(db.delete_row)
    _multi_delete = staticmethod(db.delete_rows)
    id = ''
    __tablename__ = ''
    defaults = {}

    def __init__(self, unique_id, *args, **kwargs):
        for k in kwargs:
            if k == 'id':continue
            if type(self.defaults[k]) != type(kwargs[k]):
                if type(kwargs[k]) == datetime:
                    kwargs[k] = db.to_epoch(kwargs[k])
                    continue
                kwargs[k] = type(self.defaults[k])(kwargs[k])
        self.__dict__.update(kwargs)
        self.id = unique_id

    def __getattr__(self, name):
        print name
        object.__getattr__(self, name)

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    def __repr__(self):
        s = '<'+str(self.__class__.__name__)+' '
        for k in sorted(self.__dict__.iterkeys()):
            if type(self.__dict__[k]) == datetime:
                continue
            s += str(k)+': '+str(self.__dict__[k])+', '
        return s[:-2]+'>'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    '''
    @classmethod
    def _query(cls, row_type, *rules, **kwargs):
        return Query(row_type, *rules, **kwargs)
    '''

    @classmethod
    def _multi_commit(cls, list_of_rows):
        ids = []
        kwargs = []
        for row in list_of_rows:
            ids.append(row.id)
            kwargs.append(row.__dict__)
        cls._set_rows(cls.__tablename__, ids, kwargs)

    @classmethod
    def build(cls):
        cls._build(cls.__tablename__, **cls.defaults)

    @classmethod
    def drop(cls):
        cls._drop(cls.__tablename__)

    @classmethod
    def rebuild(cls):
        try:
            cls.drop()
        except Exception as e:
            pass
        cls.build()

    def _update(self, **kwargs):
        self.__dict__.update(kwargs)

    def _commit(self):
        self._set_row(self.__tablename__, self.id, **self.__dict__)



