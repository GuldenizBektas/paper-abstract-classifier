"""
    This file will get paper abstracts from arxiv website.
    We will specify the tags for their categories.
    Fetch 2000 abstract each for 4 categories.
    Then it will send data to PostgreSQL database on my local.

    - Artificial Intelligence
    - Machine Learning
    - Computer Vision
    - Data Structures and Algorithms

    IMPORTANT: Create a DB, train and test tables and user with right privigelles before using this code.
"""

import arxiv
import psycopg2
import pandas as pd

# This part getting the data from arxiv API. If you do this once, you dont have to do it again.
def data_fetch():

    ai = [{
    'category': doc.categories,
    'category': 'ai',
    'text': doc.summary
    }
    for doc in arxiv.Search(query='cat:cs.AI', max_results=2000).results()]

    ml = [{
        'category': 'ml',
        'text': doc.summary
    }
    for doc in arxiv.Search(query='cat:cs.LG', max_results=2000).results()]

    cv = [{
        'category': 'cv',
        'text': doc.summary
    }
    for doc in arxiv.Search(query='cat:cs.CV', max_results=2000).results()]

    ds = [{
        'category': 'ds',
        'text': doc.summary
    }
    for doc in arxiv.Search(query='cat:cs.DS', max_results=2000).results()]

    return ai, ml, cv, ds


# split as train and set
def split(ai, ml, cv, ds, max_train=1500):
    train = (ai[0:max_train] + ml[0:max_train] + cv[0:max_train] + ds[0:max_train])
    test = (ai[max_train-1:-1] + ml[max_train-1:-1] +
       cv[max_train-1:-1] + ds[max_train-1:-1])
    return train, test

def sent_train_db(db, user, password, train_set):
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        database=db,
        user=user,
        password=password
    )

    # Create a cursor
    cursor = conn.cursor()

    # Iterate over the DataFrame rows and insert data into the table
    for index, row in pd.DataFrame(train_set).iterrows():
        cursor.execute("""
            INSERT INTO train (category, text)
            VALUES (%s, %s);
        """, (row['category'], row['text']))

    # Commit the changes
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()
    print("Done!")

def sent_test_db(db, user, password, test_set):
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        database=db,
        user=user,
        password=password
    )

    # Create a cursor
    cursor = conn.cursor()

    # Iterate over the DataFrame rows and insert data into the table
    for index, row in pd.DataFrame(test_set).iterrows():
        cursor.execute("""
            INSERT INTO test (category, text)
            VALUES (%s, %s);
        """, (row['category'], row['text']))

    # Commit the changes
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()
    print("Done!")

if __name__  ==  "__main__":
    ai, ml, cv, ds = data_fetch()
    train, test = split(ai, ml, cv, ds, 1500)
    sent_train_db("db", "user", "password", train) # change for your case
    sent_train_db("db", "user", "password", test) # change for your case