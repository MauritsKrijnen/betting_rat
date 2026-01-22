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
        result = rat_db.add_market("Trump Greenland", "will-trump-acquire-greenland-before-2027", "5", 0.117, 0.883)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], str)

    def test_api_add_market_bulk_ok(self):
        result = rat_db.add_market_bulk([("Trump Greenland", "will-trump-acquire-greenland-before-2027", "1", 0.117, 0.883), ("Democrat nominee", "will-gavin-newsom-win-the-2028-democratic-presidential-nomination-568", "5", 0.117, 0.883)])
        self.assertIsNotNone(result)
        # This does not actually check the insert but instead checks if the expected result of a executemany is correct(empty list)
        self.assertIsInstance(result, list)

class TestDbUpdatedData(unittest.TestCase):
    def test_api_update_market_ok(self):
        result = rat_db.add_market("Trump Greenland", "will-trump-acquire-greenland-before-2027", "5", 0.117, 0.883)
        result = rat_db.update_market_price(link="will-trump-acquire-greenland-before-2027", new_price=(0.1, 0.9))
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], tuple)

class TestDbDeleteData(unittest.TestCase):
    def test_api_delete_market_ok(self):
        result = rat_db.remove_market("will-trump-acquire-greenland-before-2027")
        self.assertIsNotNone(result)
        # remove other markets as well
        result = rat_db.remove_market("will-gavin-newsom-win-the-2028-democratic-presidential-nomination-568")

