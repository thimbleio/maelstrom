import db_utils as db


def connect(cass_ip, cass_kp):
    db.connect(cass_ip, cass_kp)


def close():
    db.close()