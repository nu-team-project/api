import sqlite3
from sqlite3 import Error

class dbConnect:
    def __init__(this) -> None:
        this.__database="kew.db"

    def run_query(this, query):
        conn = None
        try:
            conn = sqlite3.connect(this.__database)
        except Error as e:
            print(e)
        with conn:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        return rows

