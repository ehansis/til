# Accelerating DataFrame.to_sql 10x when storing to PostgreSQL

In a [previous post](pydataglobal2020_2.md) I wrote about storing data from Pandas DataFrames
to an SQL database and why/how this could be accelerated.

Today's post includes a simple recipe for a large speed improvement when storing to a PostgreSQL DB.
To be clear: I didn't come up with this, the core code is from
[the Pandas docs](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql-method).
I'd still like to show how you can use this method and the benefits it brings.


## A custom storage method

Pandas allows you to provide a custom SQL clause when storing with `DataFrame.to_sql`,
see [the docs](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql-method).

The example given there leverages the CSV copy functionality of the Postgres database
to do fast inserts of large tables:

```python
import csv
import io

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
```

What's happening here? After establishing a database cursor `cur`, we open a file-like
buffer `s_buf`. Into this buffer we write the contents of our dataframe as CSV.
Then we pipe that into an SQL `COPY` command.
This is equivalent to exporting our DataFrame as a CSV file and then `COPY`ing that
CSV file into the Postgres DB, but we avoid actually writing the file.  

With this way of inserting the data, we take advantage of the highly performant,
built-in Postgres `COPY` command for CSV data.


## Simple benchmarks

Let's set up some infrastructure for generating test data and timing the DB insertion:
```python
import os
from datetime import datetime

import numpy as np
import pandas as pd
import sqlalchemy as sa
from pandas.io import sql as psql

# connect to the local test db
engine = sa.create_engine(
    f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@localhost:5432/dev"
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


test_table_name = "insert_benchmarks"


def clear_test_table():
    """Delete our test table"""
    psql.execute(f"DROP TABLE IF EXISTS {test_table_name}", engine)


def get_test_table(n_rows=50_000, n_cols=10):
    """Generate a simple test table"""
    return pd.DataFrame(
        np.random.random((n_rows, n_cols)), columns=[f"col{i}" for i in range(n_cols)]
    )
```

Now let's compare the standard `DataFrame.to_sql` to using our `psql_insert_copy` method:
```python
def simple_to_sql(df: pd.DataFrame):
    df.to_sql(test_table_name, con=engine, index=False)


def with_insert_copy(df: pd.DataFrame, chunksize=None):
    df.to_sql(test_table_name, con=engine, method=psql_insert_copy, index=False, chunksize=chunksize)

    
if __name__ == "__main__":
    t = run_and_time(run_and_time
        store_func=simple_to_sql,
        pre=clear_test_table,
        post=clear_test_table,
        data_func=get_test_table,
    )
    print(f"Simple pandas to_sql:   {t:5.2f} seconds")

    t = run_and_time(
        store_func=with_insert_copy,
        pre=clear_test_table,
        post=clear_test_table,
        data_func=get_test_table,
    )
    print(f"With psql_insert_copy:  {t:5.2f} seconds")
```

This yields:
```
Simple pandas to_sql:    8.08 seconds
With psql_insert_copy:   0.86 seconds
```

So the improved insertion method, using the Postgres CSV `COPY` command, resulted in about 10x speedup.


## Chunky data

There is one more variable to optimize: The `DataFrame.to_sql` method has a `chunksize` parameter.
This specifies how many rows of the DataFrame should be stored per transaction/batch.
In its default setting, with `chunksize=None`, the whole DataFrame is written in a single batch.

Let's vary the `chunksize` and see what happens. Here we use a DataFrame with 1 Mio rows
(above we used 50k). The calls look like this:
```python
t = run_and_time(
    store_func=partial(with_insert_copy, chunksize=100_000),
    pre=clear_test_table,
    post=clear_test_table,
    data_func=partial(get_test_table, n_rows=1_000_000),
)
print(f"1 Mio rows, psql_insert_copy, chunksize = 100_000:  {t:5.2f} seconds")
```

We get the following timings:

```
1 Mio rows, psql_insert_copy, chunksize = 1000:  16.67 seconds
1 Mio rows, psql_insert_copy, chunksize = 10_000:  15.97 seconds
1 Mio rows, psql_insert_copy, chunksize = 100_000:  16.06 seconds
1 Mio rows, psql_insert_copy, chunksize = 1_000_000:  16.50 seconds
```

Using a large chunk size reduces the runtime, but just by a little.
Interestingly, the run time increases again when trying to write the whole table at once.
I haven't investigated yet, why that is.

As a guideline, using a large `chunk_size` helps performence, but for very large tables
you should probably specify an explicit `chunk_size` instead of trying to write
the whole table at once (which would be the default behavior).
The latter might lead to memory issues with very large datasets.

