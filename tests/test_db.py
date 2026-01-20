import unittest
import requests as api

from db import BettingRatDatabase

rat_db = BettingRatDatabase()


class TestDbFunction(unittest.TestCase):
    def test_db_connection(self):
        self.assertTrue(rat_db.db_exist)
    
class TestDbGetData(unittest.TestCase):
    def test_api_get_market_ok(self):
        result = rat_db.get_markets()
        self.assertIsNotNone(result)

    def test_api_get_market_output(self):
        result = rat_db.get_markets()
        self.assertTrue(result, None)

class TestDbAddData(unittest.TestCase):
    def test_api_add_market_ok(self):
        result = rat_db.add_market("Trump Greenland", "will-trump-acquire-greenland-before-2027", "5min")
        self.assertIsNotNone(result)

    def test_api_add_market_output(self):
        result = rat_db.add_market_bulk([("Trump Greenland", "will-trump-acquire-greenland-before-2027", "5min"), ("Democrat nominee", "will-gavin-newsom-win-the-2028-democratic-presidential-nomination-568", "5min")])
        self.assertIsNotNone(result)
