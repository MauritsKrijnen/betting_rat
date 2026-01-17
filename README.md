# betting_rat
Local discord bot that keeps track of polymarket movements (WIP)
Requires a .env file containing a discord bot app token

## Functionality
### api_get_market
Requires the name of a market as input.  
Returns json object used for other functions.

### api_get_market_buy
Requires a "clobTokenIds".  
Returns json object with the parameter 'price' which holds price of the yes/buy option.

### api_get_market_prices
Same as api_get_market_buy but for no/sell price.

### api_get_market_prices
Requires market json object including a "clobTokenIds".  
returns price values from the output of api_get_market_buy and api_get_market_sell as a string.
