from gf.models.account import Account
from time import time
from uuid import uuid4
import multiprocessing as mp
import gf.lib.db.db_utils as db

#db.get_row_by_id("users", uuid4())
#db.get_row_by_id("shit", uuid4())
Account(id=uuid4(), username= "hello", name="John", email="shit").commit()
quit()
init_id = uuid4()
acc = Account(id=init_id, name='Matt Morse',
                username='matt',
                email='matt@gradf.ly',
                login_count=80,
                email_authorized=True,
                grade='14',
                city_name='Buffalo',
                bio_text='THE MOST BADASS STEM STUDENT IN TOWN',
                tags=[uuid4(), uuid4(), uuid4(), uuid4(), uuid4()],
                subscribed=[uuid4(), uuid4()],
                subscribers=[uuid4(), uuid4()],
                projects=[uuid4()],
                following_projects=[uuid4(),uuid4()],
                trophies=[uuid4(),uuid4(),uuid4()])
acc.commit()
quit()
n = 100
avg_write = 0.0
avg_read = 0.0
for i in range(n):
    start = time()
    acc.commit()
    avg_write += time() - start
    start = time()
    Account.get_by_lookup('matt')
    avg_read += time() - start
avg_read /= float(n)
avg_write /= float(n)
print "serial test:"
print "Average read speed:", avg_read
print "Average write speed:", avg_write
def threaded_test(filler):
    print 'starting'
    n = 100
    avg_write = 0.0
    avg_read = 0.0
    for i in range(n):
        print 'commiting'
        start = time()
        acc.commit()
        avg_write += time() - start
        print 'commited!'
        print 'looking up'
        start = time()
        Account.get_by_lookup('matt')
        avg_read += time() - start
        print 'looked up!'
    avg_read /= float(n)
    avg_write /= float(n)
    return avg_read, avg_write

num_threads = 4
pool = mp.Pool(num_threads)
results =  pool.map(threaded_test, [1,1,1,1])
avg_write = 0.0
avg_read = 0.0
for read, write in results:
    avg_write += write
    avg_read += read
avg_read /= float(num_threads)
avg_write /= float(num_threads)
print "parallel test:"
print "Average read speed:", avg_read
print "Average write speed:", avg_write




