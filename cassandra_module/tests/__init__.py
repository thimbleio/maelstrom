import unittest
from test_db_utils import DBUnitTests
from test_search import SearchUnitTests


def run_suite():
    test_classes = [DBUnitTests, SearchUnitTests]
    loader = unittest.TestLoader()
    suite = unittest.TestSuite(
        [loader.loadTestsFromTestCase(test) for test in test_classes]
    )
    return suite
