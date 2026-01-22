import unittest
import requests as api

from api import Api

class TestApiFunction(unittest.TestCase):
    def test_api_connection(self):
        self.assertEqual(api.get("https://gamma-api.polymarket.com/markets").status_code, 200)
    
class TestApiGetMarketPrices(unittest.TestCase):
    def test_api_get_market(self):
        self.assertIsNotNone(Api.api_get_market("will-trump-acquire-greenland-before-2027"))
        self.assertIsInstance(Api.api_get_market("will-trump-acquire-greenland-before-2027"), list)

    def test_get_prices(self):
        api = Api
        self.assertGreater(float(api.api_get_market_prices(api, api.api_get_market("will-trump-acquire-greenland-before-2027"))[0]), 0)
        self.assertGreater(1, float(api.api_get_market_prices(api, api.api_get_market("will-trump-acquire-greenland-before-2027"))[0]))
        self.assertGreater(float(api.api_get_market_prices(api, api.api_get_market("will-trump-acquire-greenland-before-2027"))[1]), 0)
        self.assertGreater(1, float(api.api_get_market_prices(api, api.api_get_market("will-trump-acquire-greenland-before-2027"))[1]))