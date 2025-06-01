import requests
from dotenv import load_dotenv
import os

class CoinGecko:
    def __init__(self):
        coingecko_api_key = os.getenv('COIN_GECKO_API')
        if coingecko_api_key:
            print(f"COINGECKO API Key exists and begins {coingecko_api_key[:8]}")
        else:
            print("COINGECKO API Key not set")
        self.API_KEY = coingecko_api_key

    def getPrice(self, symbol):

        url = f"https://api.coingecko.com/api/v3/simple/price?x_cg_demo_api_key={self.API_KEY}&symbols={str(symbol).lower()}&vs_currencies=usd"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

        return response.text
    
    def getCoinInfobyExchange(self, coin_id, exchange):
        url = f"https://api.coingecko.com/api/v3/exchanges/{exchange}/tickers?x_cg_demo_api_key=CG-sCWdovuYxQoqm9fyRt3RAMF8&coin_ids={coin_id}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

        return response.text
    
