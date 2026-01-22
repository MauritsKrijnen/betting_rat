import sqlite3
import os.path
import datetime

class BettingRatDatabase():
    def __init__(self):
        try:
            if os.path.isfile("my.db")==False:
                with open('my.db', 'w') as file:
                    pass
                conn = sqlite3.connect('my.db')
                cur = conn.cursor()
                cur.execute('CREATE TABLE markets (name TEXT, link TEXT, interval TEXT, last_update TEXT, buy FLOAT, sell FLOAT)')
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
        
    def add_market(self, name, link, interval, yes, no):
        try:
            with sqlite3.connect("my.db") as conn:
                cur = conn.cursor()
                values = (name, link, interval, yes, no)
                cur.execute('INSERT INTO markets (name, link, interval, last_update, buy, sell) VALUES(?,?,?,datetime("now"),?,?) RETURNING *;', values)
                result = cur.fetchone()
                return result
        except():
            return None

    # not currently in use 
    def add_market_bulk(self, market_list):
        try:
            with sqlite3.connect("my.db") as conn:
                cur = conn.cursor()
                cur.executemany('INSERT INTO markets (name, link, interval, last_update, buy, sell) VALUES(?,?,?,datetime("now"),?,?)', market_list)
                result = cur.fetchall()
                return result
        except():
            return None

    def update_market_price(self, link, new_price):
        try:
            with sqlite3.connect("my.db") as conn:
                cur = conn.cursor()
                values = (new_price[0], new_price[1], link)
                cur.execute('UPDATE markets SET buy=?, sell=?, last_update=datetime("now") WHERE link=? RETURNING *;', values)
                result = cur.fetchall()
                return result
        except():
            return None

    def remove_market(self, link):
        try:
            with sqlite3.connect("my.db") as conn:
                cur = conn.cursor()
                values = (link,)
                cur.execute('DELETE FROM markets WHERE link=?', values)
                return "Finished"
        except():
            return None
        