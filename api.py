import requests as api

class Api():
    # Get market info
    def api_get_market(market_name):
        response = api.get(f"https://gamma-api.polymarket.com/markets?slug={market_name}")
        if  response.status_code == 200:
            market = response.json()
            return market
        else:
            return None

    # # Get current buy price
    # def api_get_market_buy(token):
    #     response = api.get(f"https://clob.polymarket.com/price?token_id={token}&side=buy")
    #     if  response.status_code == 200:
    #         price = response.json()
    #         return price
    #     else:
    #         return None
        
    # Get current sell price
    def api_get_market_sell(token):
        response = api.get(f"https://clob.polymarket.com/price?token_id={token}&side=sell")
        if  response.status_code == 200:
            price = response.json()
            return price
        else:
            return None
    ## Warning! api for some reason is mixed up and returns buy yes price as sell yes!!! sell yes instead returns the correct buy price    
    # Get both buy and sell price
    def api_get_market_prices(self, market):
        token = market[0]["clobTokenIds"].strip("\\").split('["')[1].split('"')[0]
        price = self.api_get_market_sell(token)['price']
        return [price, str(abs(float(price)-1))]