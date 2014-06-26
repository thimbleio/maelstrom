from row import Row


class Base(Row):
    lookups = []
    search_terms = []

    def __init__(self, *args, **kwargs):
        if 'id' in kwargs.keys():
            unique_id = kwargs['id']
        else:
            unique_id = self.id
        try:
            Row.__init__(self, unique_id, *args, **kwargs)
        except KeyError as k:
            print "KeyError: Column", k, "does not exist."
        finally:
            return

    def __setattr__(self, name, value):
        super(Base, self).__setattr__(name, value)

    def __getattr__(self, name):
        super(Base, self).__getattr__(name)

    @classmethod
    def get_by_lookup(cls, string):
        from gf.lib.db.lookup import LookUp

        user_id = LookUp.get_by_id(string).model_id
        return cls.get_by_id(user_id)

    @classmethod
    def get_by_id(cls, req_id):
        data = cls._get_row_by_id(cls.__tablename__, req_id)
        return cls(**data)

    @classmethod
    def get_specific_props(cls, req_id, columns):
        data = cls._get_row_spec_prop(cls.__tablename__, req_id,
                                      columns+['id'])
        return cls(**data)

    @classmethod
    def multi_get_by_id(cls, req_ids):
        rows = cls._get_rows_by_id(cls.__tablename__, req_ids)
        objs = {}
        for row in rows:
            objs[row['id']] = cls(**row)
        return objs

    @classmethod
    def multi_update_data(cls, dict_of_sessions):
        uuids = dict_of_sessions.keys()
        list_of_sessions = dict_of_sessions.values()
        cls._set_rows(cls.__tablename__, uuids, list_of_sessions)

    @classmethod
    def delete(cls, id):
        cls._delete(cls.__tablename__, id)
        # TODO
        '''
        if cls.lookups:
            from gf.lib.db.lookup import LookUp
            cls._multi_delete(LookUp.__tablename__, cls.lookups)
        if cls.search_terms:
            from gf.lib.db.search import Search
            cls._multi_delete(Search.__tablename__, cls.search_terms)
        '''

    @classmethod
    def multi_delete(cls, ids):
        for id in ids:
            cls.delete(id)


    def update_data(self, **kwargs):
        self._update(**kwargs)

    def commit(self):
        from maelstrom.cassandra.lib.lookup import LookUp
        from maelstrom.cassandra.lib.search import Search
        to_lookups = {}
        to_search = {}
        if self.lookups:
            for lookup in self.lookups:
                lookup_id = self.__dict__[lookup]
                if lookup_id != "":
                    to_lookups[lookup_id] = LookUp(id=lookup_id, model=self.__tablename__, model_id=self.id)
            LookUp.multi_update_data(to_lookups)

        if self.search_terms:
            for term in self.search_terms:
                search_string = self.__dict__[term]
                if search_string != "":
                    substring = ""
                    for char in search_string:
                        substring += char
                        to_search[substring] = Search(id=substring, model_type=self.__tablename__, model_ids=set([self.id]))
                    #to_search[search_string] = Search(string=search_string, model_type=self.__tablename__, model_id=self.id)
                    #to_search[search_string] = Search(id=search_string, model_type=self.__tablename__, model_ids=set([self.id]))
                #print to_search
            print to_search
            Search.multi_update_data(to_search)

        self._commit()


