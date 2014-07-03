from uuid import uuid4
from maelstrom.search import Search
from account import Account
from test import CassandraTestCase


class SearchUnitTests(CassandraTestCase):

    test_setup = False

    def setUp(self):
        #CassandraTestCase.setUp(self, ['192.241.181.163', '107.170.88.98'], 'gradfly')
        CassandraTestCase.setUp(self, ['127.0.0.1:9160'], 'test')
        Account.rebuild()
        Search.rebuild()
        #c.start(['192.241.181.163', '107.170.88.98'], 'gradfly')
        '''
        try:
            c.start(['192.241.181.163', '107.170.88.98'], 'gradfly')
        except Exception:
            from time import sleep
            print 'failed :('
            sleep(50000)
        finally:
            c.start(['192.241.181.163', '107.170.88.98'], 'gradfly')
        '''
        self.init_id = uuid4()
        self.account = Account(id=self.init_id, name='Matt Morse',
                               username='matt',
                               email='matt@gradf.ly',
                               login_count=80,
                               email_authorized=True,
                               grade='14',
                               city_name='Buffalo',
                               bio_text='THE MOST BADASS STEM STUDENT IN TOWN',
                               tags=[uuid4(), uuid4(), uuid4(), uuid4(),
                                     uuid4()],
                               subscribed=[uuid4(), uuid4()],
                               subscribers=[uuid4(), uuid4()],
                               projects=[uuid4()],
                               following_projects=[uuid4(), uuid4()],
                               trophies=[uuid4(), uuid4(), uuid4()])
        self.account.commit()

    def test_search_username(self):
        search = Search.get_by_id("matt")
        self.assertTrue(self.account.id in search.model_ids)

    def test_search_email(self):
        search = Search.get_by_id("matt@gradf.ly")
        self.assertTrue(self.account.id in search.model_ids)

    def test_search_username_substr(self):
        search = Search.get_by_id("ma")
        print self.account.id
        print search.model_ids
        self.assertTrue(self.account.id in search.model_ids)

    def test_search_email_substr(self):
        search = Search.get_by_id("matt@g")
        print self.account.id
        print search.model_ids
        self.assertTrue(self.account.id in search.model_ids)

    def test_search_refined(self):
        search_general = Search.get_by_id("m")
        search_username = Search.get_by_id("matt")
        search_email = Search.get_by_id("matt@gradf.ly")
        username_is_subset = search_username.model_ids.issubset(
            search_general.model_ids)
        email_is_subset = search_email.model_ids.issubset(
            search_general.model_ids)
        self.assertTrue(username_is_subset and email_is_subset)

    def tearDown(self):
        CassandraTestCase.tearDown(self)
        #c.stop()
