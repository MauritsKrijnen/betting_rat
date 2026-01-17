import unittest
import requests as api

from api import Api

class TestApiFunction(unittest.TestCase):
    def test_api_connection(self):
        self.assertEqual(api.get("https://gamma-api.polymarket.com/markets").status_code, 200)
    
# find better test target; this one expires jan 20 2026
class TestApiGetMarketPrices(unittest.TestCase):
    def test_api_get_market(self):
        self.assertNotEqual(Api.api_get_market("elon-musk-of-tweets-january-13-january-20-520-539"), None)

    def test_get_prices(self):
        api = Api
        self.assertGreater(float(api.api_get_market_prices(api, api.api_get_market("elon-musk-of-tweets-january-13-january-20-520-539"))[0]), 0)
        self.assertGreater(1, float(api.api_get_market_prices(api, api.api_get_market("elon-musk-of-tweets-january-13-january-20-520-539"))[0]))