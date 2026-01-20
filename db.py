import sqlite3
import os.path

class BettingRatDatabase():
    def __init__(self):
        try:
            if os.path.isfile("my.db")==False:
                with open('my.db', 'w') as file:
                    pass
                conn = sqlite3.connect('my.db')
                cur = conn.cursor()
                cur.execute('CREATE TABLE markets (name TEXT, link TEXT, interval TEXT, buy FLOAT, sell FLOAT)')
                conn.commit()
                conn.close
                self.db_exist = True
                return
            else:
                self.db_exist = True
                return
        except:
            self.db_exist = False

    def get_markets(self):
        try:
            with sqlite3.connect("my.db") as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM markets')
                result = cur.fetchall()
                return result
        except():
            return None
        
    def add_market(self, name, link, interval):
        try:
            with sqlite3.connect("my.db") as conn:
                cur = conn.cursor()
                values = (name, link, interval)
                cur.execute('INSERT INTO markets (name, link, interval) VALUES(?,?,?)', values)
                result = cur.fetchone()
                return result
        except():
            return None

    def add_market_bulk(self, market_list):
        try:
            with sqlite3.connect("my.db") as conn:
                cur = conn.cursor()
                cur.executemany('INSERT INTO markets (name, link, interval) VALUES(?,?,?)', market_list)
                result = cur.fetchall()
                return result
        except():
            return None
        
    def remove_market(name, link):
        pass
        