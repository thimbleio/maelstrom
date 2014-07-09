from maelstrom.tests.account import Account
from maelstrom.data import Data
from maelstrom.lookup import LookUp
from maelstrom.search import Search
import maelstrom

maelstrom.connect(['127.0.0.1'], 'test')

print 'rebuilding lookup table...'
LookUp.rebuild()
print 'rebuilding users...'
Account.rebuild()
print 'rebuilding data...'
Data.rebuild()
print 'rebuilding search table...'
Search.rebuild()

maelstrom.close()
