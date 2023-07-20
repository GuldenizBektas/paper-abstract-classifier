"""
    This file will read data from PSQL database.
"""

import psycopg2
import pandas as pd
import pandas.io.sql as psql


def read_data(db, user , password):
    conn = psycopg2.connect(
    database=db,
    user=user,
    password=password
    )

    cursor = conn.cursor()

    train = pd.read_sql_query("SELECT * FROM train;", conn)
    test = pd.read_sql_query("SELECT * FROM test;", conn)

    cursor.close()
    conn.close()
    return train, test