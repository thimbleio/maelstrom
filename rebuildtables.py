from maelstrom.tests.account import Account
from maelstrom.data import Data
from maelstrom.lookup import LookUp
from maelstrom.search import Search
import maelstrom
from time import sleep

maelstrom.start(['127.0.0.1'],'test')

print 'rebuilding lookup table...'
LookUp.rebuild()
sleep(3)
print 'rebuilding users...'
Account.rebuild()
sleep(3)
print 'rebuilding data...'
Data.rebuild()
sleep(3)
print 'rebuilding search table...'
Search.rebuild()
sleep(3)
