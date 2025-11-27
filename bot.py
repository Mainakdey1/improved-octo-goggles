from binance import Client
from binance.enums import *
import argparse
import logging
import sys


#note as 27/11: testnet.binancefuture.com does not work most times
#logging module is python-logger but can be done with basic logging class
logging.basicConfig(
    filename="trading_bot.log",
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com" 
        #big question here: if testnet is where i get my api keys, why does using official binance keys matter??

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side == "BUY" else SIDE_SELL,
                type=FUTURE_ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logging.info(f"Market Order: {order}")
            return order
        except Exception as e:
            logging.error(f"Error placing market order: {e}")
            print("Error:", e)

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side == "BUY" else SIDE_SELL,
                type=FUTURE_ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
            logging.info(f"Limit Order: {order}")
            return order
        except Exception as e:
            logging.error(f"Error placing limit order: {e}")
            print("Error:", e)

def main():
    parser = argparse.ArgumentParser(description="Simple Binance Futures Testnet Bot")

    parser.add_argument("--api-key", required=True)
    parser.add_argument("--api-secret", required=True)

    parser.add_argument("--symbol", required=True, help="e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"])
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", required=False, type=float)

    args = parser.parse_args()

    bot = BasicBot(args.api_key, args.api_secret)

    if args.type == "MARKET":
        result = bot.place_market_order(args.symbol, args.side, args.quantity)
    else:
        if args.price is None:
            print("Price required for LIMIT order")
            sys.exit(1)
        result = bot.place_limit_order(args.symbol, args.side, args.quantity, args.price)

    print("Order Result:", result)

if __name__ == "__main__":
    main()
# dont have time for TWAP

#note as of 27/11: testnet DOES NOT WORK
