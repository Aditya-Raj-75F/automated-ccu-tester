import basic_utilities  # to support logging messages to stream and file

import sqlite3
import logging

# Function to read the database and find if the tables are empty or not
def read_db(path="."):
    logging.debug(f"Reading db from path: {path}")
    data_count = dict()
    try:
        conn = sqlite3.connect(f'{path}/renatusDb')
        c = conn.cursor()
        entity_count = c.execute('SELECT count(*) FROM entities').fetchall()[0][0]
        messages_count = c.execute('SELECT count(*) FROM messages').fetchall()[0][0]
        writable_array_count = c.execute('SELECT count(*) FROM writableArray').fetchall()[0][0]
        conn.close()
        data_count = dict()
        data_count["entities"] = entity_count
        data_count["messages"] = messages_count
        data_count["writable_array"] = writable_array_count
    except Exception as e:
        logging.debug(f"Error while reading db: {e}: {path}/renatusDb")
        data_count["entities"] = -1
        data_count["messages"] = -1
        data_count["writable_array"] = -1
    finally:
        return data_count
        