import unittest
from uuid import uuid4
from cassandra_module.search import Search
from cassandra_module.account import Account
import cassandra_module as c


class SearchUnitTests(unittest.TestCase):

    def setUp(self):
        c.start(['192.241.181.163', '107.170.88.98'], 'gradfly')
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
        self.assertTrue(self.account.id in search.model_ids)

    def test_search_email_substr(self):
        search = Search.get_by_id("matt@g")
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
        c.stop()