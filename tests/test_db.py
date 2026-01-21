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
        self.assertIsInstance(result, list)

class TestDbAddData(unittest.TestCase):
    def test_api_add_market_ok(self):
        result = rat_db.add_market("Trump Greenland", "will-trump-acquire-greenland-before-2027", "5min")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], str)

    def test_api_add_market_bulk_ok(self):
        result = rat_db.add_market_bulk([("Trump Greenland", "will-trump-acquire-greenland-before-2027", "5min"), ("Democrat nominee", "will-gavin-newsom-win-the-2028-democratic-presidential-nomination-568", "5min")])
        self.assertIsNotNone(result)
        # This does not actually check the insert but instead checks if the expected result of a executemany is correct(empty list)
        self.assertIsInstance(result, list)

class TestDbDeleteData(unittest.TestCase):
    def test_api_delete_market_ok(self):
        result = rat_db.remove_market("will-trump-acquire-greenland-before-2027")
        self.assertIsNotNone(result)
        result = rat_db.remove_market("will-gavin-newsom-win-the-2028-democratic-presidential-nomination-568")

