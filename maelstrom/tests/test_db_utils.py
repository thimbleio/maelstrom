from uuid import uuid4
from maelstrom.data import Data
from test import CassandraTestCase


class DBUnitTests(CassandraTestCase):
    """
    The Data class is the generic protoype for the database models. As such,
    correct testing database functionality on it will test database
    transactions, while other model-specific tests should be written
    in a separate testing class.
    """
    test_setup = False

    def setUp(self):
        self.ids_used = []
        CassandraTestCase.setUp(self, ['127.0.0.1'], 'test')
        #c.start(['192.241.181.163', '107.170.88.98'], 'gradfly')
        '''
        try:
            c.start(['192.241.181.163', '107.170.88.98'], 'gradfly')
        except Exception:
            from time import sleep
            print 'failed'
            sleep(50000)
        finally:
            c.start(['192.241.181.163', '107.170.88.98'], 'gradfly')
        '''
    def test_get_and_put_by_id(self):
        init_id = uuid4()
        self.ids_used.append(init_id)
        data = Data(id=init_id, contents="john ")
        data.commit()
        test_data = Data.get_by_id(init_id)
        #for i,j in zip(user_1.__dict__.values(), test_user_1.__dict__.values()):
        #	print i,j, i == j
        self.assertEqual(data, test_data)

    def test_batch_and_get(self):
        ids = [uuid4(), uuid4(), uuid4()]
        self.ids_used += list(ids)
        names = ['bob', 'joe', 'sara']
        datum = [Data(id=i, contents=name) for i, name in zip(ids, names)]
        datum = {a.id: a for a in datum}

        Data.multi_update_data(datum)
        datum_test = Data.multi_get_by_id(ids).values()

        #no order is guaranteed by Cassandra so we sort it
        datum_test.sort(key=(lambda a: a.id))
        datum_true = sorted(datum.values(), key=lambda a: a.id)

        if len(ids) != len(datum):
            self.assertTrue(False)
        print datum_true
        print datum_test
        is_equal = True
        for a, a_test in zip(datum_true, datum_test):
            is_equal = is_equal and (a == a_test)
        self.assertTrue(is_equal)

    def test_batch_vs_iter_single(self):
        ids = [uuid4(), uuid4(), uuid4()]
        self.ids_used += list(ids)
        names = ['bob', 'joe', 'sara']
        datum = [Data(id=i, contents=name) for i, name in zip(ids, names)]
        datum = {a.id: a for a in datum}

        Data.multi_update_data(datum)
        datum_batch = Data.multi_get_by_id(ids).values()
        datum_single = []

        for i in ids:
            datum_single.append(Data.get_by_id(i))
        datum_batch.sort(key=(lambda a: a.id))
        datum_single.sort(key=(lambda a: a.id))
        print datum_single
        print datum_batch
        self.assertTrue(datum_batch == datum_single)

    def test_delete(self):
        init_id = uuid4()
        self.ids_used.append(init_id)
        data = Data(id=init_id, contents="testtesttest")
        data.commit()
        data.delete(init_id)
        if not Data.get_by_id(init_id):
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def tearDown(self):
        Data.multi_delete(self.ids_used)
        CassandraTestCase.tearDown(self)
        #c.stop()

