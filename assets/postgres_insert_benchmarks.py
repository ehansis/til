"""Benchmarks for various postgres insert methods"""

import csv
import io
import os
from datetime import datetime
import random
from functools import partial

import numpy as np
import pandas as pd
import sqlalchemy as sa
from pandas.io import sql as psql

# connect to the local test db
engine = sa.create_engine(
    f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_USER']}@localhost:5432/dev"
)


def run_and_time(store_func, data_func, pre, post, reps=5):
    """Run store_func N times to get avg run time, clear test table before and after"""
    total_time = 0

    for _ in range(reps):
        pre()
        start_time = datetime.now()
        store_func(data_func())
        total_time += (datetime.now() - start_time).total_seconds()
        post()

    return total_time / reps


#
# Storing a simple Pandas DataFrame
#

test_table_name = "insert_benchmarks"


def clear_test_table():
    """Delete our test table"""
    psql.execute(f"DROP TABLE IF EXISTS {test_table_name}", engine)


def get_test_table(n_rows=50_000, n_cols=10):
    """Generate a simple test table"""
    return pd.DataFrame(
        np.random.random((n_rows, n_cols)), columns=[f"col{i}" for i in range(n_cols)]
    )


def psql_insert_copy(table, conn, keys, data_iter):
    """
    Execute SQL statement inserting data

    Adapted from: https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql-method

    Use this as the 'method' parameter in pandas.to_sql().
    Don't forget to set a large chunksize!

    Args:
        table (pandas.io.sql.SQLTable): data table
        conn (sqlalchemy.engine.Engine or sqlalchemy.engine.Connection): DB connection
        keys (List[str]): column names
        data_iter (Iterable): iterates the values to be inserted
    """
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = io.StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ", ".join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = "{}.{}".format(table.schema, table.name)
        else:
            table_name = table.name

        sql = "COPY {} ({}) FROM STDIN WITH CSV".format(table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)


def disable_triggers(engn):
    with engn.connect() as con:
        con.execute("SET session_replication_role = 'replica';")


def enable_triggers(engn):
    with engn.connect() as con:
        con.execute("SET session_replication_role = 'origin';")


class DeferredTriggers:
    """Context manager for a DB operations with deferred triggers

    Disabling triggers like checking foreign key constraints can greatly improve DB insert operations.
    However, this doesn't seem to help much for bulk COPY.
    See: https://stackoverflow.com/a/49584660/5839193

    NOTE: This requires DB admin privileges!
    """

    def __init__(self, engn):
        self.engine = engn

    def __enter__(self):
        disable_triggers(self.engine)

    def __exit__(self, *args):
        enable_triggers(self.engine)


def simple_to_sql(df: pd.DataFrame):
    df.to_sql(test_table_name, con=engine, index=False)


def with_insert_copy(df: pd.DataFrame, chunksize=None):
    df.to_sql(
        test_table_name,
        con=engine,
        method=psql_insert_copy,
        index=False,
        chunksize=chunksize,
    )


def with_disabled_triggers(df: pd.DataFrame):
    with DeferredTriggers(engine):
        df.to_sql(test_table_name, con=engine, method=psql_insert_copy, index=False)


#
# Using SQLAlchemy ORM mappings
#

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, orm

# ORM base class
Base = declarative_base()

session_maker = orm.sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "benchmark_users"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Item(Base):
    __tablename__ = "benchmark_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    name = Column(String)
    price = Column(Float)


n_users = 10
n_items = 30_000


def get_objects():
    return (
        [User(name=f"User{i}") for i in range(n_users)],
        [
            Item(name=f"Item{i}", user_id=random.randint(1, 10), price=random.random())
            for i in range(n_items)
        ],
    )


def get_objects_as_dataframes():
    return (
        pd.DataFrame([dict(id=i + 1, name=f"User{i}") for i in range(n_users)]),
        pd.DataFrame(
            [
                dict(
                    id=i + 1,
                    name=f"Item{i}",
                    user_id=random.randint(1, 10),
                    price=random.random(),
                )
                for i in range(n_items)
            ]
        ),
    )


def drop_orm_tables():
    Base.metadata.drop_all(bind=engine)


def create_orm_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def orm_via_orm(objects):
    """Store ORM objects directly, via SQLAlchemy ORM"""
    session = session_maker()
    users, items = objects

    for obj in users:
        session.add(obj)
    session.commit()

    for obj in items:
        session.add(obj)
    session.commit()

    session.close()


def orm_via_to_sql(dfs):
    users, items = dfs
    users.to_sql(User.__tablename__, con=engine, index=False, if_exists="append")
    items.to_sql(Item.__tablename__, con=engine, index=False, if_exists="append")


def orm_via_to_sql_with_insert_copy(dfs):
    users, items = dfs
    users.to_sql(
        User.__tablename__,
        con=engine,
        index=False,
        method=psql_insert_copy,
        if_exists="append",
    )
    items.to_sql(
        Item.__tablename__,
        con=engine,
        index=False,
        method=psql_insert_copy,
        if_exists="append",
    )


def orm_via_sql_with_disabled_triggers(dfs):
    with DeferredTriggers(engine):
        orm_via_to_sql_with_insert_copy(dfs)


#
# Run the benchmarks
#

if __name__ == "__main__":
    # t = run_and_time(
    #     store_func=simple_to_sql,
    #     pre=clear_test_table,
    #     post=clear_test_table,
    #     data_func=get_test_table,
    # )
    # print(f"Simple pandas to_sql:   {t:5.2f} seconds")

    # t = run_and_time(
    #     store_func=with_insert_copy,
    #     pre=clear_test_table,
    #     post=clear_test_table,
    #     data_func=get_test_table,
    # )
    # print(f"With psql_insert_copy:  {t:5.2f} seconds")
    #
    # t = run_and_time(
    #     store_func=partial(with_insert_copy, chunksize=1000),
    #     pre=clear_test_table,
    #     post=clear_test_table,
    #     data_func=partial(get_test_table, n_rows=1_000_000),
    # )
    # print(f"1 Mio rows, psql_insert_copy, chunksize = 1000:  {t:5.2f} seconds")
    #
    # t = run_and_time(
    #     store_func=partial(with_insert_copy, chunksize=10_000),
    #     pre=clear_test_table,
    #     post=clear_test_table,
    #     data_func=partial(get_test_table, n_rows=1_000_000),
    # )
    # print(f"1 Mio rows, psql_insert_copy, chunksize = 10_000:  {t:5.2f} seconds")

    t = run_and_time(
        store_func=partial(with_insert_copy, chunksize=100_000),
        pre=clear_test_table,
        post=clear_test_table,
        data_func=partial(get_test_table, n_rows=1_000_000),
    )
    print(f"1 Mio rows, psql_insert_copy, chunksize = 100_000:  {t:5.2f} seconds")

    t = run_and_time(
        store_func=partial(with_insert_copy, chunksize=1_000_000),
        pre=clear_test_table,
        post=clear_test_table,
        data_func=partial(get_test_table, n_rows=1_000_000),
    )
    print(f"1 Mio rows, psql_insert_copy, chunksize = 1_000_000:  {t:5.2f} seconds")

    # t = run_and_time(
    #     store_func=with_disabled_triggers,
    #     pre=clear_test_table,
    #     post=clear_test_table,
    #     data_func=get_test_table,
    # )
    # print(f"With disabled triggers: {t:5.2f} seconds")
    #
    # t = run_and_time(
    #     store_func=orm_via_orm,
    #     pre=create_orm_tables,
    #     post=drop_orm_tables,
    #     data_func=get_objects,
    # )
    # print(f"ORM objects, stored via ORM:    {t:5.2f} seconds")
    #
    # t = run_and_time(
    #     store_func=orm_via_to_sql,
    #     pre=create_orm_tables,
    #     post=drop_orm_tables,
    #     data_func=get_objects_as_dataframes,
    # )
    # print(f"ORM objects, stored via pd.to_sql: {t:5.2f} seconds")
    #
    # t = run_and_time(
    #     store_func=orm_via_to_sql_with_insert_copy,
    #     pre=create_orm_tables,
    #     post=drop_orm_tables,
    #     data_func=get_objects_as_dataframes,
    # )
    # print(f"ORM objects, stored with psql_insert_copy: {t:5.2f} seconds")
    #
    # t = run_and_time(
    #     store_func=orm_via_sql_with_disabled_triggers,
    #     pre=create_orm_tables,
    #     post=drop_orm_tables,
    #     data_func=get_objects_as_dataframes,
    # )
    # print(f"ORM objects, stored with disabled triggers: {t:5.2f} seconds")


# Results:
# Simple pandas to_sql:    8.08 seconds
# With psql_insert_copy:   0.86 seconds
# With disabled triggers:  0.84 seconds
# 1 Mio rows, psql_insert_copy, chunksize = 1000:  16.67 seconds
# 1 Mio rows, psql_insert_copy, chunksize = 10_000:  15.97 seconds
# 1 Mio rows, psql_insert_copy, chunksize = 100_000:  16.06 seconds
# 1 Mio rows, psql_insert_copy, chunksize = 1_000_000:  16.50 seconds
# ORM objects, stored via ORM:     8.37 seconds
# ORM objects, stored via pd.to_sql:  4.35 seconds
# ORM objects, stored with psql_insert_copy:  0.83 seconds
# ORM objects, stored with disabled triggers:  1.37 seconds
