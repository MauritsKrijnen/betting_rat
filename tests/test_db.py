import unittest
import requests as api

from db import BettingRatDatabase

class TestApiFunction(unittest.TestCase):
    def test_db_connection(self):
        rat_db = BettingRatDatabase
    
class TestApiGetMarketPrices(unittest.TestCase):
    def test_api_get_market(self):
        pass