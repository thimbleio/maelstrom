"""

Associated database objects and functions that are critical to
database interactions. Functions are defined here are used in
the generic data objects to improve the modularity of the sytem
and allow for easier future development. Classes defined here
are meant to be used only by the module's functions and should
not be instantiated client-side.

"""

from datetime import date, datetime
from uuid import UUID
from collections import OrderedDict
from decimal import Decimal
from cassandra import InvalidRequest, ConsistencyLevel
import cassandra
from cassandra.query import SimpleStatement
from itertools import izip
from time import time
from .exceptions import NoSuchIndexException, NoSuchColumnFamilyException
from .cass_conn import CassandraConnection


c = None
cass_keyspace = None


def connect(cass_ip, cass_kp):
    global c, cass_keyspace
    cass_keyspace = cass_kp
    c = CassandraConnection(cass_ip, cass_kp)


def close():
    c.destroy_cluster()


def get_type_map():
    return {None: 'Null',
            bool: 'boolean',
            float: 'double',
            int: 'bigint',
            long: 'bigint',
            Decimal: 'decimal',
            str: 'varchar',
            unicode: 'varchar',
            buffer: 'blob',
            bytearray: 'blob',
            date: 'timestamp',
            datetime: 'timestamp',
            list: 'list',
            tuple: 'list',
            set: 'set',
            dict: 'map',
            OrderedDict: 'map',
            UUID: 'uuid'}


def is_collection(v):
    return type(v) == list or type(v) == dict or type(v) == set


def get_time():
    """
    cassie-driver autoserializes timestamp columns into Python datetime
    objects datetime does not trivially translate into seconds from epoch,
    which is needed to guarantee uniqueness of objects. Subject to change at a
    later time.
    """
    return int(time() * 100)


def to_epoch(d_time):
    return int((d_time-datetime(1970, 1, 1)).total_seconds() * 1000)


def create_column_family(cf_name, **kwargs):
    type_map = get_type_map()
    build = "create table "+cass_keyspace+"."+cf_name+" ( "
    build += "id uuid PRIMARY KEY, "
    for k, v in kwargs.iteritems():
        if k == "id":
            continue
        if is_collection(v):
            if type(v) == dict:
                pass
                #typechecking
            else:
                #typechecking
                pass
            build += k+" "+type_map[type(v)]+'<'+type_map[type(v[0])]+">, "
        else:
            build += k+" "+type_map[type(v)]+", "
    build = build[:-2]+") with caching = \'all\'"
    c.session.execute(build)


def drop_column_family(cf_name):
    c.session.execute('drop table '+cass_keyspace+"."+cf_name)


def get_row_by_id(cf_name, row_id):
    query = SimpleStatement('select * from '+cf_name+' where id = %s')
                            #consistency_level=cassandra.ConsistencyLevel.QUORUM)
    try:
        print 'select * from '+cf_name+' where id =', row_id
        return c.session.execute(query, [row_id]).result()[0]
    except InvalidRequest:
        raise NoSuchColumnFamilyException(cf_name)
    except IndexError:
        raise NoSuchIndexException(row_id)


def get_rows_by_id(cf_name, row_ids):
    query = "select * from "+cf_name+" where id in ("
    for rid in row_ids:
        query += str(rid)+","
    query = query[:-1]+")"
    try:
        return c.session.execute(
            SimpleStatement(query)).result() #, consistency_level=ConsistencyLevel.QUORUM
    except InvalidRequest:
        raise NoSuchColumnFamilyException(cf_name)
    except IndexError:
        raise NoSuchIndexException(row_ids)


def build_insert_query(cf_name, unique_id, **kwargs):
    cols = kwargs.keys()
    vals = kwargs.values()
    query = "insert into "+cf_name+" ("
    for col in cols:
        query += str(col)+", "
    query = query[:-2]+") values ("
    for val in vals:
        if type(val) == list:
            query += ' ['
            for element in val:
                query += str(element)+', '
            query = query[:-2]+'], '
        elif type(val) == str or type(val) == datetime:
            query += '\''+str(val)+"', "
        elif type(val) == UUID:
            query += str(val)+", "

        else:
            query += str(val)+", "

    query = query[:-2]+")"
    return query


def insert_row_data(cf_name, unique_id, **kwargs):
    query = build_insert_query(cf_name, unique_id, **kwargs)
    try:
        return c.session.execute(
            SimpleStatement(query)).result() #, consistency_level=ConsistencyLevel.QUORUM)
    except InvalidRequest:
        print "ColumnFamilyError: no such column family exists."
    except InvalidRequest:
        raise NoSuchColumnFamilyException(cf_name)


def set_rows_data(cf_name, unique_ids, list_of_rows):
    list_of_kwargs = [r.__dict__ for r in list_of_rows]
    batch = "begin batch "
    for uuid, kwargs in izip(unique_ids, list_of_kwargs):
        batch += build_insert_query(cf_name, uuid, **kwargs)+" "
    batch += "apply batch"
    try:
        c.session.execute(
            SimpleStatement(batch) #, consistency_level=ConsistencyLevel.QUORUM
        ).result()
    except InvalidRequest:
        raise NoSuchColumnFamilyException(cf_name)


def get_row_spec_prop(cf_name, unique_id, cols):
    query = "select "
    for col in cols:
        query += col+", "
    query = query[:-2]+" where id=%s", (unique_id)
    try:
        return c.session.execute(
            SimpleStatement(query,))[0] #consistency_level=cassandra.ConsistencyLevel.QUORUM
    except cassandra.InvalidRequest:
        raise NoSuchColumnFamilyException(cf_name)
    except IndexError:
        raise NoSuchIndexException(unique_id)


def delete_row(cf_name, unique_id):
    query = "delete from "+cf_name+" where id="+str(unique_id)
    try:
        c.session.execute(
            SimpleStatement(query) #,consistency_level=cassandra.ConsistencyLevel.QUORUM
        )
    except cassandra.InvalidRequest:
        raise NoSuchColumnFamilyException(cf_name)
    except IndexError:
        raise NoSuchIndexException(unique_id)


def delete_rows(cf_name, unique_ids):
    batch = "begin batch "
    for id in unique_ids:
        batch += "delete from "+cf_name+" where id="+str(id)+" "
    batch += "apply batch"
    try:
        c.session.execute(
            SimpleStatement(batch)
        )
        #,  consistency_level=cassandra.ConsistencyLevel.QUORUM
    except cassandra.InvalidRequest:
        raise NoSuchColumnFamilyException(cf_name)
    except IndexError:
        raise NoSuchIndexException(unique_ids)

