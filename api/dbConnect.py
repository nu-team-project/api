import sqlite3
from sqlite3 import Error

class dbConnect:
    def __init__(this) -> None:
        this.__database="api/db/kew.db"

    def run_query(this, query):
        conn = None
        #check if the database can be connected to
        try:
            conn = sqlite3.connect(this.__database)
        except Error as e:
            print(e)
            return
        #connect to the database
        conn = sqlite3.connect(this.__database)
        cur = conn.cursor()
        cur.execute(query)
        #retrieve all the data
        rows = cur.fetchall()
        #close the connection to the database
        conn.close()
        return rows
    
    def run_no_return(this, query):
        conn = None
        #check if the database can be connected to
        try:
            conn = sqlite3.connect(this.__database)
        except Error as e:
            print(e)
        #execute the query on the database
        with conn:
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
        return

