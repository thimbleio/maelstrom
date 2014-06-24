import lib.db_utils as db

def start():
    db.connect()

def stop():
    db.close()