import sqlite3
import os.path

class BettingRatDatabase():
    def __init__(self):
        if os.path.isfile("my.db")==False:
            conn = sqlite3.connect('my.db')
            cur = conn.cursor()
            cur.execute('CREATE TABLE markets (name TEXT, link TEXT, interval TEXT, buy FLOAT, sell FLOAT)')
            conn.commit()
            conn.close

    def get_markets(self):
        try:
            with sqlite3.connect("my.db") as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM markets')
                result = cur.fetchall()
                return result
        except():
            return None
