import sqlite3
from sqlite3 import Error

class dbConnect:
    def __init__(this) -> None:
        this.__database="api/db/kew.db"

    def run_query(this, query):
        conn = None
        try:
            conn = sqlite3.connect(this.__database)
        except Error as e:
            print(e)
            return
        conn = sqlite3.connect(this.__database)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows
    
    def run_insert(this, query): #maybe rename to run_command or run_no_return ?
        conn = None
        try:
            conn = sqlite3.connect(this.__database)
        except Error as e:
            print(e)
        with conn:
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
        return

