from maelstrom.data import Data
from maelstrom.lookup import LookUp
from maelstrom.search import Search
from maelstrom.tests.account import Account
import maelstrom
from time import sleep

maelstrom.start(['localhost'],'test')

print 'rebuilding users...'
Account.rebuild()
print 'rebuilding data...'
Data.rebuild()
print 'rebuilding lookup table...'
LookUp.rebuild()
print 'rebuilding search table...'
Search.rebuild()

maelstrom.stop()