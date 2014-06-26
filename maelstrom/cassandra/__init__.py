import lib.db_utils as db


def start(cass_ip, cass_kp):
    db.connect(cass_ip, cass_kp)

def stop():
    db.close()
